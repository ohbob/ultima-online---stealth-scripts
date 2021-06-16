from __future__ import print_function

import platform
import sys
import struct
import socket
import threading
import types
import time

from .config import DEBUG, HOST, PORT, MSG_TIMEOUT, SOCK_TIMEOUT, \
    GET_PORT_ATTEMPT_COUNT
from ._datatypes import *
from .utils import convert_packet_data, show_error_message

EVENTS_NAMES = (
    'eviteminfo', 'evitemdeleted', 'evspeech', 'evdrawgameplayer',
    'evmoverejection', 'evdrawcontainer', 'evadditemtocontainer',
    'evaddmultipleitemsincont', 'evrejectmoveitem', 'evupdatechar',
    'evdrawobject', 'evmenu', 'evmapmessage', 'evallowrefuseattack',
    'evclilocspeech', 'evclilocspeechaffix', 'evunicodespeech',
    'evbuffdebuffsystem', 'evclientsendresync', 'evcharanimation',
    'evicqdisconnect', 'evicqconnect', 'evicqincomingtext', 'evicqerror',
    'evincominggump', 'evtimer1', 'evtimer2', 'evwindowsmessage', 'evsound',
    'evdeath', 'evquestarrow', 'evpartyinvite', 'evmappin', 'evgumptextentry',
    'evgraphicaleffect', 'evircincomingtext', 'evmessengerevent',
    'evsetglobalvar', 'evupdateobjstats', 'evglobalchat'
)

EVENTS_ARGTYPES = _str, _uint, _int, _ushort, _short, _ubyte, _byte, _bool
VERSION = 2, 2, 0, 1


class Connection:
    port = None
    port_lock = threading.Lock()

    def __init__(self):
        self._sock = socket.socket()

        self._id = 0
        self._buffer = bytes()
        self.pause = False
        self.results = {}
        self.callbacks = {}
        self._handlers = []
        for i in range(len(EVENTS_NAMES)):
            self.callbacks[i] = None

    @property
    def method_id(self):
        self._id += 1
        if self._id >= 65535:
            self._id = 0
        return self._id

    def connect(self, host=None, port=None):
        if host is None:
            host = HOST
        if port is None:
            if self.port is None:
                port = get_port()
                self.__class__.port = port
            else:
                port = self.port
        self._sock.settimeout(SOCK_TIMEOUT)
        self._sock.connect((host, port))
        self._sock.setblocking(False)

        # SCLangVersion
        # send language type and protocol version to stealth (data type - 5)
        # python - 1; delphi - 2; c# - 3; other - 255
        data = struct.pack('<HH5B', 5, 0, 1, *VERSION)
        size = struct.pack('<I', len(data))
        self.send(size + data)

    def close(self):
        self._sock.close()

    def receive(self, size=4096):
        # try to get a new data from socket
        data = b''
        try:
            data += self._sock.recv(size)
            if not data:
                error = 'Connection to Stealth was lost.'
                show_error_message(error)
                exit(1)
        except socket.error as err:
            # TODO: Linux error code
            if platform.system() == 'Windows' and err.errno == 10054:
                exit(1)
            return
        if DEBUG:
            print('Data received: {}'.format(convert_packet_data(data)))
        # parse data
        offset = 0
        while 1:
            if self._buffer:  # if some data was already stored
                data = self._buffer + data
                self._buffer = bytes()
            # parse packet header
            if len(data) - offset < 4:
                self._buffer += data[offset:]
                break
            size, = struct.unpack_from('<I', data, offset)
            offset += 4
            if size > len(data) - offset:
                self._buffer += data[offset - 4:]
                break
            type_, = struct.unpack_from('<H', data, offset)
            offset += 2
            # packet type is 1 (a returned value)
            if type_ == 1:
                id_, = struct.unpack_from('<H', data, offset)
                self.results[id_] = data[offset + 2:offset + size - 2]
                offset += size - 2  # - type_
            # packet type is 3 (an event callback)
            elif type_ == 3:
                index, count = struct.unpack_from('<2B', data, offset)
                offset += 2
                # parse args
                args = []
                for i in range(count):
                    argtype = EVENTS_ARGTYPES[struct.unpack_from('<B', data,
                                                                 offset)[0]]
                    offset += 1
                    arg = argtype.from_buffer(data, offset)
                    offset += struct.calcsize(arg.fmt)
                    args.append(arg.value)
                # save handler
                handler = {
                    'handler': self.callbacks[index],
                    'args': args
                }
                self._handlers.append(handler)
            # packet type is 4 (a pause script packet)
            elif type_ == 4:
                self.pause = True if not self.pause else False
                offset += size - 2  # - type_
            # packet type is 2 (terminate script)
            elif type_ == 2:
                exit(0)
            if offset >= len(data):
                break

        # run event handlers
        while len(self._handlers):
            handler = self._handlers.pop(0)
            handler['handler'](*handler['args'])

    def send(self, data):
        if DEBUG:
            print('Packet sent: {}'.format(convert_packet_data(data)))
        self._sock.send(data)


class ScriptMethod:
    argtypes = []
    restype = None

    def __init__(self, index):
        self.index = index

    def __call__(self, *args):
        conn = get_connection()
        conn.receive()  # check pause or events
        while conn.pause:
            conn.receive()
            time.sleep(.01)
        if not self.index:  # wait
            return
        # pack args
        data = bytes()
        for cls, val in zip(self.argtypes, args):
            data += cls(val).serialize()
        # form packet
        id_ = conn.method_id if self.restype else 0
        header = struct.pack('<2H', self.index, id_)
        packet = header + data
        size = struct.pack('<I', len(packet))
        # send to the stealth
        conn.send(size + packet)
        # wait for a result if required
        while self.restype is not None:
            conn.receive()
            try:
                result = self.restype.from_buffer(conn.results.pop(id_))
                return result.value
            except KeyError:
                pass


def get_port():
    def win():
        import os
        from . import py_stealth_winapi as _winapi
        wnd = 'TStealthForm'.decode() if b'' == '' else 'TStealthForm'  # py2
        hwnd = _winapi.FindWindow(wnd, None)
        if not hwnd:
            error = 'Can not find Stealth window.'
            _winapi.MessageBox(0, error.decode() if b'' == '' else error,  # py2
                               'Error'.decode() if b'' == '' else 'Error', 0)
            exit(1)
        # form copydata
        pid = '{pid:08X}'.format(pid=os.getpid())
        lp = (pid + os.path.basename(sys.argv[0])).encode() + b'\x00'
        cb = len(lp)
        dw = _winapi.GetCurrentThreadId()
        copydata = _winapi.COPYDATA(dw, cb, lp)
        # send message
        _winapi.SetLastError(0)
        if not _winapi.SendMessage(hwnd, _winapi.WM_COPYDATA, 0,
                                   copydata.pointer):
            error = 'Can not send message. ErrNo: {}'.format(
                _winapi.GetLastError())
            _winapi.MessageBox(0, error.decode() if b'' == '' else error,  # py2
                               'Error'.decode() if b'' == '' else 'Error', 0)
            exit(1)
        # wait for an answer
        msg = _winapi.MSG()
        now = time.time()
        while now + MSG_TIMEOUT > time.time():
            if _winapi.PeekMessage(msg, 0, _winapi.FM_GETFOCUS,
                                   _winapi.FM_GETFOCUS, _winapi.PM_REMOVE):
                while len(sys.argv) < 3:
                    sys.argv.append('')
                sys.argv[2] = str(msg.wParam)
                return msg.wParam
            else:
                time.sleep(0.005)
        error = 'PeekMessage timeout'
        _winapi.MessageBox(0, error.decode() if b'' == '' else error,  # py2
                           'Error'.decode() if b'' == '' else 'Error', 0)  # py2
        exit(1)

    def unix():
        # attempt to connect to Stealth
        sock = socket.socket()
        sock.settimeout(SOCK_TIMEOUT)
        if DEBUG:
            print('connecting to {0}:{1}'.format(HOST, PORT))
        try:
            sock.connect((HOST, PORT))
        except socket.error:
            show_error_message('Stealth not found. Port: {}'.format(PORT))
            exit(1)
        sock.setblocking(False)
        if DEBUG:
            print('connected')
        # attempts to get a port number
        for i in range(GET_PORT_ATTEMPT_COUNT):
            if DEBUG:
                print('attempt №' + str(i + 1))
            packet = struct.pack('<HI', 4, 0xDEADBEEF)
            sock.send(packet)
            if DEBUG:
                print('packet sent: {}'.format(convert_packet_data(packet)))
            timer = time.time()
            buffer = bytearray()
            while timer + SOCK_TIMEOUT > time.time():
                try:
                    data = sock.recv(4096)
                    buffer += data
                    if DEBUG:
                        print('received: {}'.format(convert_packet_data(data)))
                except socket.error:
                    continue
                if len(buffer) > 2:
                    length = struct.unpack_from('<H', buffer)[0]
                    if DEBUG:
                        print('length: {}'.format(length))
                    if len(buffer[2:]) < length:
                        continue
                    port = struct.unpack_from('<H', buffer, 2)[0]
                    if DEBUG:
                        print('port: {}'.format(port))
                    sock.close()
                    if DEBUG:
                        print('socket closed')
                    return port
            else:
                error = 'Connection to Stealth was lost.'
                show_error_message(error)
                exit(1)

    with Connection.port_lock:
        # Zero way - if we already got the port
        if Connection.port:
            return Connection.port
        # First way - get port from cmd parameters.
        # If script was launched as internal script from Stealth.
        if len(sys.argv) >= 3 and sys.argv[2].isalnum():
            Connection.port = int(sys.argv[2])
        # Second way - ask Stealth for a port number via socket connection or
        # windows messages. If script was launched as external script.
        elif platform.system() == 'Windows':
            Connection.port = win()
        elif platform.system() == 'Linux':
            Connection.port = unix()
        else:
            raise Exception('Can not to get port from Stealth.')
        if DEBUG:
            print('Port number: {0}'.format(Connection.port))
        return Connection.port


def get_connection():
    def join(self, timeout=None):
        self.connection.close()
        self.__class__.join(self, timeout)

    thread = threading.current_thread()
    if hasattr(thread, 'connection'):
        return thread.connection
    thread.connection = Connection()
    thread.connection.connect()
    thread.join = types.MethodType(join, thread)  # close socket for each one
    return thread.connection
