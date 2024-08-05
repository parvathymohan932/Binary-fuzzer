# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Example(KaitaiStruct):

    class IpProtocol(Enum):
        icmp = 1
        tcp = 6
        udp = 17
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(2)
        if not self.magic == b"\x0C\x16":
            raise kaitaistruct.ValidationNotEqualError(b"\x0C\x16", self.magic, self._io, u"/seq/0")
        self.attribute10 = Example.Type1(self._io, self, self._root)
        self.attribute11 = Example.Attribute3Type(self._io, self, self._root)
        self.protocol = KaitaiStream.resolve_enum(Example.IpProtocol, self._io.read_u2be())
        self.creator = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")
        self.length_in_feet = self._io.read_u2be()
        self.body = self._io.read_bytes(20)
        self.rec_type = self._io.read_u1()
        self.chunks = []
        i = 0
        while True:
            _ = Example.Chunk(self._io, self, self._root)
            self.chunks.append(_)
            if _.type == u"PLTE":
                break
            i += 1

    class Chunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u2be()
            self.type = (self._io.read_bytes(6)).decode(u"UTF-8")
            _on = self.type
            if _on == u"PLTE":
                self.body = self._io.read_u1()
            elif _on == u"cHRM":
                self.body = self._io.read_u2be()
            elif _on == u"gAMA":
                self.body = self._io.read_u4be()


    class BufferWithLen(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_value = self._io.read_u2be()
            if not self.len_value >= 1:
                raise kaitaistruct.ValidationLessThanError(1, self.len_value, self._io, u"/types/buffer_with_len/seq/0")
            if not self.len_value <= 4:
                raise kaitaistruct.ValidationGreaterThanError(4, self.len_value, self._io, u"/types/buffer_with_len/seq/0")
            self.value = self._io.read_bytes(self.len_value)


    class Attribute3Type(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.attribute12 = self._io.read_u2be()
            self.attribute13 = self._io.read_u1()
            self.attribute14 = self._io.read_u2be()


    class Type1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.attribute15 = self._io.read_u1()
            self.attribute16 = Example.Type1.Type3(self._io, self, self._root)

        class Type3(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.attribute17 = Example.Type1.Type2(self._io, self, self._root)


        class Type2(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.attribute18 = Example.Type1.Type2.Type4(self._io, self, self._root)

            class Type4(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.attribute19 = Example.Attribute3Type(self._io, self, self._root)




    @property
    def some_integer(self):
        if hasattr(self, '_m_some_integer'):
            return self._m_some_integer

        _pos = self._io.pos()
        self._io.seek(5246960)
        self._m_some_integer = Example.Attribute3Type(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_some_integer', None)

    @property
    def a_string(self):
        if hasattr(self, '_m_a_string'):
            return self._m_a_string

        _pos = self._io.pos()
        self._io.seek(5246975)
        self._m_a_string = (self._io.read_bytes(17)).decode(u"ASCII")
        self._io.seek(_pos)
        return getattr(self, '_m_a_string', None)


