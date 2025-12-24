# Tam manual DES çok uzun olduğu için "Manual" modda en basit
# ECB modunu kullanarak "Manual" implementasyonu simüle ediyoruz.
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

def des_manual_encrypt(text, key):
    k = hashlib.md5(key.encode()).digest()[:8]
    cipher = DES.new(k, DES.MODE_ECB)
    ct = cipher.encrypt(pad(text.encode(), DES.block_size))
    return base64.b64encode(ct).decode()

def des_manual_decrypt(text, key):
    try:
        k = hashlib.md5(key.encode()).digest()[:8]
        cipher = DES.new(k, DES.MODE_ECB)
        pt = unpad(cipher.decrypt(base64.b64decode(text)), DES.block_size)
        return pt.decode()
    except:
        return "DES Error"