
import datetime
import errno
import platform
import socket
import threading


__all__ = ['convert_packet_data',
           'show_error_message',
           'get_main_thread',
           'ddt2pdt',
           'pdt2ddt',
           'iterable',
           'is_socket_alive']


PY2 = b'' == ''


def convert_packet_data(data):
    return ' '.join(['{x:02X}'.format(x=x) for x in data])


def show_error_message(msg):
    system = platform.system()
    if system == 'Windows':
        from py_stealth import py_stealth_winapi as _winapi
        title = 'Error'
        if PY2:  # py2
            msg = msg.decode()
            title = title.decode()
        _winapi.MessageBox(0, msg, title, 0)
    elif system == 'Linux':
        import subprocess
        path = '/usr/bin/notify-send'
        options = ['--icon=error', '--urgency=critical']
        subprocess.call([path] + options + [msg])


def get_main_thread():  # py2
    try:
        return threading.main_thread()
    except AttributeError:
        for thread in threading.enumerate():
            if isinstance(thread, threading._MainThread):
                return thread


def ddt2pdt(ddt):  # delphi time into py datetime
    epoch = datetime.datetime(1899, 12, 30)
    return epoch + datetime.timedelta(days=ddt)


def pdt2ddt(pydt):  # py datetime into delphi time
    epoch = datetime.datetime(1899, 12, 30)
    delta = pydt - epoch
    seconds = (delta.seconds + delta.microseconds / 1000000)
    return delta.days + (seconds / 3600 / 24)


def iterable(obj):
    try:
        for _ in obj:
            return True
    except TypeError:
        return False


def is_socket_alive(sock):
    if not sock:
        return False
    try:
        sock.getsockname()
        sock.getpeername()
    except socket.error as exc:
        error = exc.args[0]
        if error == errno.EBADF or error == errno.ENOTCONN:
            return False
        raise
    return True
