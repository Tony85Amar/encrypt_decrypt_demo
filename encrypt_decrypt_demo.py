from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
import os

print("=== AES ===")
key = os.urandom(32)
iv = os.urandom(16)
msg = b"Hello from Tony Whitelow"

print("Key:", key)
print("IV:", iv)
print("Input:", msg)

cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
enc = cipher.encryptor()

pad = padding.PKCS7(128).padder()
padded = pad.update(msg) + pad.finalize()

aes_out = enc.update(padded) + enc.finalize()
print("Encrypted:", aes_out)

dec = cipher.decryptor()
unpadded = dec.update(aes_out) + dec.finalize()

unpad = padding.PKCS7(128).unpadder()
aes_plain = unpad.update(unpadded) + unpad.finalize()

print("Decrypted:", aes_plain)

print("\n=== RSA ===")
priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pub = priv.public_key()

pub_pem = pub.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
priv_pem = priv.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

print("Public Key:\n", pub_pem.decode())
print("Private Key:\n", priv_pem.decode())

rsa_msg = b"Hello from Tony Whitelow"
print("Input:", rsa_msg)

rsa_out = pub.encrypt(
    rsa_msg,
    rsa_padding.OAEP(
        mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Encrypted:", rsa_out)

rsa_plain = priv.decrypt(
    rsa_out,
    rsa_padding.OAEP(
        mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Decrypted:", rsa_plain)
