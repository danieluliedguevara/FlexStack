import unittest
from unittest.mock import patch, MagicMock

from flexstack.facilities.vru_awareness_service.vam_coder import VAMCoder


class TestCoder(unittest.TestCase):
    @patch("asn1tools.compile_string")
    def setUp(self, mock_asn1tools) -> None:
        compile_string_mock = MagicMock()
        encode_mock = MagicMock(return_value="test")
        decode_mock = MagicMock(return_value="test")
        compile_string_mock.encode = encode_mock
        compile_string_mock.decode = decode_mock
        mock_asn1tools.return_value = compile_string_mock

        self.VAMCoder = VAMCoder()

    def test_encode(self):
        self.assertEqual(self.VAMCoder.encode({}), "test")

    def test_decode(self):
        self.assertEqual(self.VAMCoder.decode({}), "test")


if __name__ == '__main__':
    unittest.main()
