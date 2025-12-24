import base64

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def expand_key(key):
    key_bytes = key.encode('utf-8')
    while len(key_bytes) < 16: key_bytes += key_bytes
    return key_bytes[:16]

def aes_manual_encrypt(text, key):
    key_bytes = expand_key(key)
    text_bytes = text.encode('utf-8')
    pad_len = 16 - (len(text_bytes) % 16)
    text_bytes += bytes([pad_len] * pad_len)
    
    encrypted = b""
    for i in range(0, len(text_bytes), 16):
        block = text_bytes[i:i+16]
        encrypted += xor_bytes(block, key_bytes)
    return base64.b64encode(encrypted).decode('utf-8')

def aes_manual_decrypt(text, key):
    try:
        key_bytes = expand_key(key)
        encrypted_bytes = base64.b64decode(text)
        decrypted = b""
        for i in range(0, len(encrypted_bytes), 16):
            block = encrypted_bytes[i:i+16]
            decrypted += xor_bytes(block, key_bytes)
            
        pad_len = decrypted[-1]
        if pad_len < 1 or pad_len > 16: return "Padding Hatası"
        return decrypted[:-pad_len].decode('utf-8')
    except:
        return "Hata"