# import unittest
# from flexstack.security.verify_service import VerifyService
# from flexstack.security.security_coder import SecurityCoder

# class TestVerifyService(unittest.TestCase):
#     pass


# sigend_data_dict = {
#             "protocolVersion": 3,
#             "content": ("signedData", {
#                 "hashId": "sha256",
#                 "tbsData": {
#                     "payload": {
#                         "data": {
#                             "protocolVersion": 3,
#                             "content": ("unsecuredData", b'something')
#                         }
#                     },
#                     "headerInfo": {
#                         "psid": 12,
#                         # "generationTime": 0,
#                         # "expireTime": 0
#                     }
#                 },
#                 "signer": ("certificate", [{
#             "version": 3,
#             "type": "explicit",
#             "issuer": ("sha256AndDigest", (0xa495991b7852b855).to_bytes(8, byteorder='big')),
#             "toBeSigned": {
#                 "id": ("name", "i2cat.net"),
#                 "cracaId": (0xa49599).to_bytes(3, byteorder='big'),
#                 "crlSeries": 0,
#                 "validityPeriod": {
#                     "start": 0,
#                     "duration": ("seconds", 30)
#                 },
#                 "appPermissions": [{
#                     "psid": 0,
#                 }],
#                 "certIssuePermissions": [
#                     {
#                         "subjectPermissions": ("all", None),
#                         "minChainLength": 1,
#                         "chainLengthRange": 0,
#                         "eeType": (b'\x00', 1)
#                     }
#                 ],
#                 "verifyKeyIndicator": ("verificationKey", ("ecdsaNistP256", ("fill", None)))
#             },
#             "signature": ("ecdsaNistP256Signature", {
#                 "rSig": ("fill", None),
#                 "sSig": (0xa495991b7852b855).to_bytes(32, byteorder='big')
#             })
#         }]),
#                 "signature": ("ecdsaNistP256Signature", {
#                     "rSig": ("fill", None),
#                     "sSig": (0xa495991b7852b855).to_bytes(32, byteorder='big')

#                 })
#             })
#         }
# coder = SecurityCoder()

# encoded = coder.encode_EtsiTs103097DataSigned(sigend_data_dict)
# decoded = coder.decode_EtsiTs103097DataSigned(encoded)
# print(decoded)
