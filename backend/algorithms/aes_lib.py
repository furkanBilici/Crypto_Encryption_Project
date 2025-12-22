from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

def get_key_iv(key_text):
    key = hashlib.sha256(key_text.encode()).digest()[:16] 
    iv = hashlib.md5(key_text.encode()).digest() 
    return key, iv

def aes_lib_encrypt(text, key_text):
    key, iv = get_key_iv(key_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    return base64.b64encode(ct_bytes).decode('utf-8')

def aes_lib_decrypt(cipher_text, key_text):
    try:
        key, iv = get_key_iv(key_text)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct = base64.b64decode(cipher_text)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    except:
        return "Şifre Çözme Hatası (Key yanlış veya veri bozuk)"