import unittest

from flexstack.geonet.common_header import CommonHeader, CommonNH, HeaderType, HeaderSubType, TrafficClass


class TestCommonHeader(unittest.TestCase):
    def test_encode_to_bytes(self):
        ch = CommonHeader()
        self.assertEqual(ch.encode_to_bytes(),
                         b'\x00\x00\x00\x00\x00\x00\x00\x00')
        ch.nh = CommonNH.BTP_A
        ch.ht = HeaderType.BEACON
        ch.hst = HeaderSubType.UNSPECIFIED
        tcp = TrafficClass()
        tcp.set_tc_id(0x1)
        tcp.set_scf(True)
        tcp.set_channel_offload(True)
        ch.tc = tcp
        ch.pl = 300
        ch.mhl = 1
        self.assertEqual(ch.encode_to_bytes(),
                         b'\x10\x10\xc1\x00\x01,\x01\x00')

    def test_decode_from_bytes(self):
        ch = CommonHeader()
        ch.nh = CommonNH.BTP_A
        ch.ht = HeaderType.BEACON
        ch.hst = HeaderSubType.UNSPECIFIED
        tcp = TrafficClass()
        tcp.set_tc_id(0x1)
        tcp.set_scf(True)
        tcp.set_channel_offload(True)
        ch.tc = tcp
        ch.pl = 300
        ch.mhl = 1
        ch2 = CommonHeader()
        ch2.decode_from_bytes(ch.encode_to_bytes())
        self.assertEqual(ch.nh, ch2.nh)
        self.assertEqual(ch.ht, ch2.ht)
        self.assertEqual(ch.hst, ch2.hst)
        self.assertEqual(ch.tc, ch2.tc)
        self.assertEqual(ch.flags, ch2.flags)
        self.assertEqual(ch.pl, ch2.pl)
        self.assertEqual(ch.mhl, ch2.mhl)


if __name__ == '__main__':
    unittest.main()
