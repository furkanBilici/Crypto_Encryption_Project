def vernam_encrypt(text, key):
    text = text.upper()
    key = key.upper()
    while len(key) < len(text):
        key += key
    key = key[:len(text)]
    
    cipher = ""
    for t, k in zip(text, key):
        if t.isalpha():
            shift = ord(k) - 65
            cipher += chr((ord(t) - 65 + shift) % 26 + 65)
        else:
            cipher += t
    return cipher

def vernam_decrypt(text, key):
    text = text.upper()
    key = key.upper()
    while len(key) < len(text):
        key += key
    key = key[:len(text)]
    
    plain = ""
    for t, k in zip(text, key):
        if t.isalpha():
            shift = ord(k) - 65
            plain += chr((ord(t) - 65 - shift) % 26 + 65)
        else:
            plain += t
    return plain