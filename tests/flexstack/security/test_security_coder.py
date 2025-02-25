import unittest
from flexstack.security.security_coder import SecurityCoder


class TestSecurityCoder(unittest.TestCase):
    """
    Testing Case for the Security Coder.
    """

    def setUp(self) -> None:
        self.security_coder = SecurityCoder()

    def test__init__(self):
        """
        Tests the init of the Security Coder.
        """
        self.assertIsNotNone(self.security_coder.asn_coder)

    def test_encode_EtsiTs103097Certificate(self):
        """
        Tests the encode_EtsiTs103097Certificate of the Security Coder.
        """
        white_certificate = {
            "version": 3,
            "type": "explicit",
            "issuer": ("sha256AndDigest", (0xa495991b7852b855).to_bytes(8, byteorder='big')),
            "toBeSigned": {
                "id": ("name", "i2cat.net"),
                "cracaId": (0xa49599).to_bytes(3, byteorder='big'),
                "crlSeries": 0,
                "validityPeriod": {
                    "start": 0,
                    "duration": ("seconds", 30)
                },
                "appPermissions": [{
                    "psid": 0,
                }],
                "certIssuePermissions": [
                    {
                        "subjectPermissions": ("all", None),
                        "minChainLength": 1,
                        "chainLengthRange": 0,
                        "eeType": (b'\x00', 1)
                    }
                ],
                "verifyKeyIndicator": ("verificationKey", ("ecdsaNistP256", ("fill", None)))
            },
            "signature": ("ecdsaNistP256Signature", {
                "rSig": ("fill", None),
                "sSig": (0xa495991b7852b855).to_bytes(32, byteorder='big')
            })
        }
        encoded_certificate = self.security_coder.encode_etsi_ts_103097_certificate(
            white_certificate)

        self.assertEqual(encoded_certificate,
                         b'\x80\x03\x00\x80\xa4\x95\x99\x1bxR\xb8U\x18\x81\ti2cat.net\xa4\x95\x99\x00\x00\x00\x00\x00\x00\x82\x00\x1e\x01\x01\x00\x01\x00\x01\x01 \x81\x00\x80\x80\x81\x80\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x95\x99\x1bxR\xb8U')

    def test_decode_EtsiTs103097Certificate(self):
        """
        Tests the decode_EtsiTs103097Certificate of the Security Coder.
        """
        encoded_certificate = b'\x80\x03\x00\x80\xa4\x95\x99\x1bxR\xb8U\x18\x81\ti2cat.net\xa4\x95\x99\x00\x00\x00\x00\x00\x00\x82\x00\x1e\x01\x01\x00\x01\x00\x01\x01 \x81\x00\x80\x80\x81\x80\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x95\x99\x1bxR\xb8U'
        decoded_certificate = self.security_coder.decode_etsi_ts_103097_certificate(
            encoded_certificate)
        self.assertEqual(decoded_certificate["signature"][1]["sSig"], (
            0xa495991b7852b855).to_bytes(32, byteorder='big'))

    def test_encode_EtsiTs103097DataSigned(self):
        """
        Tests the encode_EtsiTs103097DataSigned of the Security Coder.
        """
        white_data_signed = {
            "protocolVersion": 3,
            "content": ("signedData", {
                "hashId": "sha256",
                "tbsData": {
                    "payload": {
                        "data": {
                            "protocolVersion": 3,
                            "content": ("unsecuredData", b'adsfag')
                        }
                    },
                    "headerInfo": {
                        "psid": 0,
                        "generationTime": 0,
                        "expireTime": 0
                    }
                },
                "signer": ("digest", b'\x00\x00\x00\x00\x00\x00\x00\x00'),
                # ("certificate", []),
                "signature": ("ecdsaNistP256Signature", {
                    "rSig": ("fill", None),
                    "sSig": (0xa495991b7852b855).to_bytes(32, byteorder='big')

                })
            })
        }
        encoded_data_signed = self.security_coder.encode_etsi_ts_103097_data_signed(
            white_data_signed)
        self.assertEqual(encoded_data_signed,
                         b'\x03\x81\x00@\x03\x80\x06adsfag@\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x80\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x95\x99\x1bxR\xb8U')

    def test_decode_EtsiTs103097DataSigned(self):
        """
        Tests the decode_EtsiTs103097DataSigned of the Security Coder.
        """
        encoded_data_signed = b'\x03\x81\x00@\x03\x80\x06adsfag@\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x80\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x95\x99\x1bxR\xb8U'
        decoded_data_signed = self.security_coder.decode_etsi_ts_103097_data_signed(
            encoded_data_signed)
        self.assertEqual(decoded_data_signed["content"][1]["signature"][1]["sSig"], (
            0xa495991b7852b855).to_bytes(32, byteorder='big'))

    def test_encode_ToBeSignedData(self):
        """
        Tests the encode_ToBeSignedData of the Security Coder.
        """
        to_be_signed_data = {
            "payload": {
                "data": {
                    "protocolVersion": 3,
                    "content": ("unsecuredData", b'adsfag')
                }
            },
            "headerInfo": {
                "psid": 0,
                "generationTime": 0,
                "expireTime": 0
            }
        }
        encoded_to_be_signed_data = self.security_coder.encode_to_be_signed_data(
            to_be_signed_data)
        self.assertEqual(encoded_to_be_signed_data,
                         b'@\x03\x80\x06adsfag@\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_encode_ToBeSignedCertificate(self):
        """
        Tests the encode_ToBeSignedCertificate of the Security Coder.
        """
        to_be_signed_certificate = {
            "id": ("name", "i2cat.net"),
            "cracaId": (0xa49599).to_bytes(3, byteorder='big'),
            "crlSeries": 0,
            "validityPeriod": {
                "start": 0,
                "duration": ("seconds", 30)
            },
            "appPermissions": [{
                "psid": 0,
            }],
            "certIssuePermissions": [
                {
                    "subjectPermissions": ("all", None),
                    "minChainLength": 1,
                    "chainLengthRange": 0,
                    "eeType": (b'\x00', 1)
                }
            ],
            "verifyKeyIndicator": ("verificationKey", ("ecdsaNistP256", ("fill", None)))
        }
        encoded_to_be_signed_certificate = self.security_coder.encode_ToBeSignedCertificate(
            to_be_signed_certificate)
        self.assertEqual(encoded_to_be_signed_certificate,
                         b'\x18\x81\ti2cat.net\xa4\x95\x99\x00\x00\x00\x00\x00\x00\x82\x00\x1e\x01\x01\x00\x01\x00\x01\x01 \x81\x00\x80\x80\x81')
