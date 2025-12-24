from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

def aes_lib_encrypt(text, key):
    k = hashlib.sha256(key.encode()).digest()[:16]
    cipher = AES.new(k, AES.MODE_ECB)
    ct = cipher.encrypt(pad(text.encode(), AES.block_size))
    return base64.b64encode(ct).decode()

def aes_lib_decrypt(text, key):
    try:
        k = hashlib.sha256(key.encode()).digest()[:16]
        cipher = AES.new(k, AES.MODE_ECB)
        pt = unpad(cipher.decrypt(base64.b64decode(text)), AES.block_size)
        return pt.decode()
    except:
        return "Decryption Error"