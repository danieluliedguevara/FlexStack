import unittest

from flexstack.geonet.basic_header import BasicHeader, BasicNH, LT, LTbase


class TestLT(unittest.TestCase):

    def test_set_value_in_milis(self):
        lt = LT()
        lt.set_value_in_millis(50)
        self.assertEqual(lt.multiplier, 1)
        self.assertEqual(lt.base, LTbase.FIFTY_MILLISECONDS)
        lt.set_value_in_millis(100)
        self.assertEqual(lt.multiplier, 2)
        self.assertEqual(lt.base, LTbase.FIFTY_MILLISECONDS)
        lt.set_value_in_millis(1000)
        self.assertEqual(lt.multiplier, 1)
        self.assertEqual(lt.base, LTbase.ONE_SECOND)
        lt.set_value_in_millis(10000)
        self.assertEqual(lt.multiplier, 1)
        self.assertEqual(lt.base, LTbase.TEN_SECONDS)
        lt.set_value_in_millis(100000)
        self.assertEqual(lt.multiplier, 1)
        self.assertEqual(lt.base, LTbase.ONE_HUNDRED_SECONDS)
        lt.set_value_in_millis(1000000)
        self.assertEqual(lt.multiplier, 0)
        self.assertEqual(lt.base, LTbase.ONE_HUNDRED_SECONDS)
        lt.set_value_in_millis(10000000)
        self.assertEqual(lt.multiplier, 0)
        self.assertEqual(lt.base, LTbase.ONE_HUNDRED_SECONDS)

    def test_set_value_in_seconds(self):
        lt = LT()
        lt.set_value_in_seconds(0)
        self.assertEqual(lt.multiplier, 0)
        self.assertEqual(lt.base, LTbase.FIFTY_MILLISECONDS)
        lt.set_value_in_seconds(1)
        self.assertEqual(lt.multiplier, 1)
        self.assertEqual(lt.base, LTbase.ONE_SECOND)
        lt.set_value_in_seconds(10)
        self.assertEqual(lt.multiplier, 1)
        self.assertEqual(lt.base, LTbase.TEN_SECONDS)
        lt.set_value_in_seconds(100)
        self.assertEqual(lt.multiplier, 1)
        self.assertEqual(lt.base, LTbase.ONE_HUNDRED_SECONDS)
        lt.set_value_in_seconds(1000)
        self.assertEqual(lt.multiplier, 0)
        self.assertEqual(lt.base, LTbase.ONE_HUNDRED_SECONDS)
        lt.set_value_in_seconds(10000)
        self.assertEqual(lt.multiplier, 0)
        self.assertEqual(lt.base, LTbase.ONE_HUNDRED_SECONDS)

    def test_get_value_in_millis(self):
        lt = LT()
        lt.set_value_in_millis(50)
        self.assertEqual(lt.get_value_in_millis(), 50)
        lt.set_value_in_millis(100)
        self.assertEqual(lt.get_value_in_millis(), 100)
        lt.set_value_in_millis(1000)
        self.assertEqual(lt.get_value_in_millis(), 1000)
        lt.set_value_in_millis(10000)
        self.assertEqual(lt.get_value_in_millis(), 10000)
        lt.set_value_in_millis(100000)
        self.assertEqual(lt.get_value_in_millis(), 100000)

    def test_get_value_in_seconds(self):
        lt = LT()
        lt.set_value_in_millis(50)
        self.assertEqual(lt.get_value_in_seconds(), 0)
        lt.set_value_in_millis(100)
        self.assertEqual(lt.get_value_in_seconds(), 0)
        lt.set_value_in_millis(1000)
        self.assertEqual(lt.get_value_in_seconds(), 1)
        lt.set_value_in_millis(10000)
        self.assertEqual(lt.get_value_in_seconds(), 10)
        lt.set_value_in_millis(100000)
        self.assertEqual(lt.get_value_in_seconds(), 100)

    def test_lt_to_bytes(self):
        lt = LT()
        lt.set_value_in_millis(50)
        self.assertEqual(lt.encode_to_bytes(), b'\x04')
        lt.set_value_in_millis(100)
        self.assertEqual(lt.encode_to_bytes(), b'\x08')
        lt.set_value_in_millis(1000)
        self.assertEqual(lt.encode_to_bytes(), b'\x05')
        lt.set_value_in_millis(10000)
        self.assertEqual(lt.encode_to_bytes(), b'\x06')
        lt.set_value_in_millis(100000)
        self.assertEqual(lt.encode_to_bytes(), b'\x07')


class TestBasicHeader(unittest.TestCase):

    def test_encode_to_bytes(self):
        bh = BasicHeader()
        lt = LT()
        lt.set_value_in_millis(50)
        bh.set_lt(lt)
        bh.set_version(1)
        bh.set_nh(BasicNH.ANY)
        bh.set_rhl(1)
        self.assertEqual(bh.encode_to_bytes(), b'\x10\x00\x04\x01')
        bh = BasicHeader()
        self.assertEqual(bh.encode_to_bytes(), b'\x11\x00\x00\x00')

    def test_decode_from_bytes(self):
        bh = BasicHeader()
        lt = LT()
        lt.set_value_in_millis(50)
        bh.set_lt(lt)
        bh.set_version(1)
        bh.set_nh(BasicNH.ANY)
        bh.set_rhl(1)
        encoded = bh.encode_to_bytes()
        bh = BasicHeader()
        bh.decode_from_bytes(encoded)
        self.assertEqual(bh.lt.base, LTbase.FIFTY_MILLISECONDS)
        self.assertEqual(bh.lt.multiplier, 1)
        self.assertEqual(bh.lt.get_value_in_millis(), 50)
        self.assertEqual(bh.version, 1)
        self.assertEqual(bh.nh, BasicNH.ANY)
        self.assertEqual(bh.rhl, 1)


if __name__ == '__main__':
    unittest.main()
