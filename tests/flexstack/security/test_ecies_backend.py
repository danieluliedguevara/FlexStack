"""
# Now the ECIES Backend testing is just to get some notes:

# Ieee1609Dot2Data
data = {
    "protocolVersion" : 3,
    "content" : ("encryptedData", {
        "recipients" : [
            ("certRecipInfo", {
                "recipientId": b'', # HashedId8 of the certificate containing the public key
                "encKey": ("eciesNistP256", {
                    "v" : {},
                    "c" : b'',
                    "t" : b''
                })
            })
        ],
        "ciphertext" : ("aes128ccm", {
            "nonce" : b'', # 12 bytes
            "ccmCiphertext" : b'', # 16 bytes
        })
    })
}

# Note: ECIES is just used to encrypt the AES key, which is used to encrypt the data.
# The AES key is encrypted with the public key of the recipient.


# An example code to use aes128ccm (encrypt):
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b'Sixteen byte key'
nonce = b'Nonce'
plaintext = b'Hello World'

cipher = AES.new(key, AES.MODE_CCM, nonce=nonce)
cipher.update(b'additional data')
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

print(ciphertext)

# An example code to use aes128ccm (decrypt):
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b'Sixteen byte key'
nonce = b'Nonce'
ciphertext = b'\x9d\x8a\x1b\x9f\x1d\x8f\x1e\x0f'

cipher = AES.new(key, AES.MODE_CCM, nonce=nonce)
cipher.update(b'additional data')
plaintext = cipher.decrypt(ciphertext)

print(plaintext)


# Public key encryption algorithm
"""
