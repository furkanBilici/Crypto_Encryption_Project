from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

def des_manual_encrypt(text, key):
    try:
        k = hashlib.md5(key.encode('utf-8')).digest()[:8]
        
        cipher = DES.new(k, DES.MODE_ECB)
        
        raw_bytes = text.encode('utf-8')
        padded_text = pad(raw_bytes, DES.block_size)
        
        encrypted_bytes = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        print(f"DES Encrypt Hatası: {e}")
        return f"DES Hata: {str(e)}"

def des_manual_decrypt(cipher_text, key):
    try:
        k = hashlib.md5(key.encode('utf-8')).digest()[:8]
        
        cipher = DES.new(k, DES.MODE_ECB)
        
        encrypted_bytes = base64.b64decode(cipher_text)
        decrypted_padded = cipher.decrypt(encrypted_bytes)
        decrypted_bytes = unpad(decrypted_padded, DES.block_size)
        
        return decrypted_bytes.decode('utf-8')
    except ValueError:
        print("DES Decrypt Hatası: Padding bozuk (Yanlış Anahtar)")
        return "Hata: Anahtar yanlış!"
    except Exception as e:
        print(f"DES Decrypt Genel Hata: {e}")
        return f"DES Hata: {str(e)}"