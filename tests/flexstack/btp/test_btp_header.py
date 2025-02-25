import unittest

from flexstack.btp.btp_header import BTPAHeader, BTPBHeader
from flexstack.btp.service_access_point import BTPDataRequest


class TestBTPAHeader(unittest.TestCase):

    def test_initialize_with_request(self):
        btp_data_request = BTPDataRequest()
        btp_data_request.destination_port = 1
        btp_data_request.source_port = 2
        btp_a_header = BTPAHeader()
        btp_a_header.initialize_with_request(btp_data_request)
        self.assertEqual(btp_a_header.destination_port,
                         btp_data_request.destination_port)
        self.assertEqual(btp_a_header.source_port,
                         btp_data_request.source_port)

    def test_encode_to_int(self):
        btp_a_header = BTPAHeader()
        btp_a_header.destination_port = 1
        btp_a_header.source_port = 2
        self.assertEqual(btp_a_header.encode_to_int(), 65538)

    def test_encode(self):
        btp_a_header = BTPAHeader()
        btp_a_header.destination_port = 1
        btp_a_header.source_port = 2
        self.assertEqual(btp_a_header.encode(), b'\x00\x01\x00\x02')

    def test_decode(self):
        btp_a_header = BTPAHeader()
        btp_a_header.decode(b'\x00\x01\x00\x02')
        self.assertEqual(btp_a_header.destination_port, 1)
        self.assertEqual(btp_a_header.source_port, 2)


class TestBTPBHeader(unittest.TestCase):

    def test_initialize_with_request(self):
        btp_data_request = BTPDataRequest()
        btp_data_request.destination_port = 1
        btp_data_request.destinaion_port_info = 2
        btp_b_header = BTPBHeader()
        btp_b_header.initialize_with_request(btp_data_request)
        self.assertEqual(btp_b_header.destination_port,
                         btp_data_request.destination_port)
        self.assertEqual(btp_b_header.destination_port_info,
                         btp_data_request.destinaion_port_info)

    def test_encode_to_int(self):
        btp_b_header = BTPBHeader()
        btp_b_header.destination_port = 1
        btp_b_header.destination_port_info = 2
        self.assertEqual(btp_b_header.encode_to_int(), 65538)

    def test_encode(self):
        btp_b_header = BTPBHeader()
        btp_b_header.destination_port = 1
        btp_b_header.destination_port_info = 2
        self.assertEqual(btp_b_header.encode(), b'\x00\x01\x00\x02')

    def test_decode(self):
        btp_b_header = BTPBHeader()
        btp_b_header.decode(b'\x00\x01\x00\x02')
        self.assertEqual(btp_b_header.destination_port, 1)
        self.assertEqual(btp_b_header.destination_port_info, 2)


if __name__ == '__main__':
    unittest.main()
