from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

def aes_lib_encrypt(text, key):
    try:
        k = hashlib.sha256(key.encode('utf-8')).digest()[:16]
        
        cipher = AES.new(k, AES.MODE_ECB) 
        raw_bytes = text.encode('utf-8')
        padded_text = pad(raw_bytes, AES.block_size)
        
        encrypted_bytes = cipher.encrypt(padded_text)
        
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        print(f"AES Lib Encrypt Hatası: {e}")
        return f"Hata: {str(e)}"

def aes_lib_decrypt(cipher_text, key):
    try:
        k = hashlib.sha256(key.encode('utf-8')).digest()[:16]
        
        cipher = AES.new(k, AES.MODE_ECB)
        encrypted_bytes = base64.b64decode(cipher_text)
        decrypted_padded = cipher.decrypt(encrypted_bytes)
        decrypted_bytes = unpad(decrypted_padded, AES.block_size)
        
        return decrypted_bytes.decode('utf-8')
        
    except ValueError as e:
        print(f"AES Lib Decrypt Hatası (Muhtemelen Yanlış Anahtar): {e}")
        return "Hata: Anahtar yanlış veya veri bozuk (Padding Error)"
    except Exception as e:
        print(f"AES Lib Decrypt Genel Hata: {e}")
        return f"Çözme Hatası: {str(e)}"