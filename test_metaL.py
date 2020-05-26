
from metaL import *

class TestPrimitive:

    def test_hex(self):
        x = Hex('0xDeadBeef')
        assert x.test() == '\n<hex:0xdeadbeef>'
        assert x.val == 3735928559

    def test_bin(self):
        x = Bin('0b1101')
        assert x.test() == '\n<bin:0b1101>'
        assert x.val == 13
