import base64

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def aes_manual_encrypt(text, key):
    key_bytes = key.encode()
    while len(key_bytes) < 16: key_bytes += key_bytes
    key_bytes = key_bytes[:16]
    
    text_bytes = text.encode()
    pad_len = 16 - (len(text_bytes) % 16)
    text_bytes += bytes([pad_len] * pad_len)
    
    encrypted = b""
    for i in range(0, len(text_bytes), 16):
        block = text_bytes[i:i+16]
        encrypted_block = xor_bytes(block, key_bytes)
        encrypted += encrypted_block
        
    return base64.b64encode(encrypted).decode()

def aes_manual_decrypt(text, key):
    try:
        key_bytes = key.encode()
        while len(key_bytes) < 16: key_bytes += key_bytes
        key_bytes = key_bytes[:16]
        
        encrypted_bytes = base64.b64decode(text)
        decrypted = b""
        
        for i in range(0, len(encrypted_bytes), 16):
            block = encrypted_bytes[i:i+16]
            decrypted_block = xor_bytes(block, key_bytes)
            decrypted += decrypted_block
            
        # Unpadding
        pad_len = decrypted[-1]
        return decrypted[:-pad_len].decode()
    except:
        return "Manual AES Error"