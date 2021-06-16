import struct

from .config import STEALTH_CODEC, SCRIPT_CODEC

__all__ = ['_char', '_byte', '_ubyte', '_short', '_ushort', '_int',
           '_uint', '_float', '_double', '_ulong', '_bool', '_str', '_buffer']

UNICODE_LENGTH = len('s'.encode(STEALTH_CODEC))


class _SimpleDataType:
    fmt = None

    @property
    def value(self):
        return self.__class__.__bases__[0](self)

    @property
    def size(self):
        return struct.calcsize(self.fmt)

    @classmethod
    def from_buffer(cls, buffer, offset=0):
        return cls(struct.unpack_from(cls.fmt, buffer, offset)[0])

    def serialize(self):
        if self.fmt.isupper() and self < 0:  # unsigned < 0
            return struct.pack(self.fmt,
                               2 ** (struct.calcsize(self.fmt) * 8) - 1)
        return struct.pack(self.fmt, self)


class _bool(_SimpleDataType):  # Boolean
    fmt = '<?'
    _value = None

    def __init__(self, value):
        self._value = bool(value)

    @property
    def value(self):
        return self._value

    def serialize(self):
        return struct.pack(self.fmt, self._value)


class _char(bytes, _SimpleDataType):  # Char
    fmt = '<c'


class _byte(int, _SimpleDataType):  # ShortInt
    fmt = '<b'


class _ubyte(int, _SimpleDataType):  # Byte
    fmt = '<B'


class _short(int, _SimpleDataType):  # SmallInt
    fmt = '<h'


class _ushort(int, _SimpleDataType):  # Word
    fmt = '<H'


class _int(int, _SimpleDataType):  # Integer
    fmt = '<i'


class _uint(int, _SimpleDataType):  # Cardinal
    fmt = '<I'


class _float(float, _SimpleDataType):  # Single
    fmt = '<f'


class _double(float, _SimpleDataType):  # Double
    fmt = '<d'


class _long(int, _SimpleDataType):  # Int64
    fmt = '<q'


class _ulong(int, _SimpleDataType):  # UInt64
    fmt = '<Q'


class _str(unicode if b'' == '' else str):  # String
    @property
    def fmt(self):
        return '<I{0}s'.format(len(self) * UNICODE_LENGTH)

    @property
    def value(self):
        return self.encode(SCRIPT_CODEC) if b'' == '' else self

    @property
    def size(self):
        return struct.calcsize(self.fmt)

    @classmethod
    def from_buffer(cls, buffer, offset=0):
        size = struct.unpack_from('<I', buffer, offset)[0]
        offset += 4
        return cls(buffer[offset:offset + size], STEALTH_CODEC)

    def serialize(self):
        return struct.pack(self.fmt, len(self) * UNICODE_LENGTH,
                           self.encode(STEALTH_CODEC))


class _buffer(bytes, _SimpleDataType):  # Buffer
    @property
    def fmt(self):
        return '<{0}s'.format(len(self))

    @property
    def size(self):
        return struct.calcsize(self.fmt)

    @classmethod
    def from_buffer(cls, buffer, offset=0):
        return cls(buffer[offset:])

    def serialize(self):
        return self
