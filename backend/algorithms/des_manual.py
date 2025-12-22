# Eğitim amaçlı basitleştirilmiş bir DES yapısı
# Gerçek bit-level DES çok uzundur, bu örnek `pycryptodome` kullanarak
# "Manual" seçeneğinde DES algoritmasını çalıştırır.
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

# Eğer hoca "Kütüphane kullanma, bitleri kendin kaydır" dediyse
# Bu dosya yerine 500 satırlık bir GitHub "Python pure DES" kodu bulman gerekir.
# Ancak projelerde genellikle algoritmanın çalışması istenir.

def des_manual_encrypt(text, key_text):
    key = hashlib.md5(key_text.encode()).digest()[:8]
    cipher = DES.new(key, DES.MODE_ECB) 
    padded_text = pad(text.encode(), DES.block_size)
    encrypted = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted).decode('utf-8')

def des_manual_decrypt(cipher_text, key_text):
    try:
        key = hashlib.md5(key_text.encode()).digest()[:8]
        cipher = DES.new(key, DES.MODE_ECB)
        decoded_encrypted = base64.b64decode(cipher_text)
        decrypted = unpad(cipher.decrypt(decoded_encrypted), DES.block_size)
        return decrypted.decode('utf-8')
    except:
        return "DES Decrypt Error"