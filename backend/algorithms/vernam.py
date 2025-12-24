def vernam_encrypt(text, key):
    text = text.upper()
    key = (key * (len(text)//len(key) + 1))[:len(text)].upper()
    res = ""
    for t, k in zip(text, key):
        if t.isalpha():
            res += chr((ord(t) - 65 + ord(k) - 65) % 26 + 65)
        else:
            res += t
    return res

def vernam_decrypt(text, key):
    text = text.upper()
    key = (key * (len(text)//len(key) + 1))[:len(text)].upper()
    res = ""
    for t, k in zip(text, key):
        if t.isalpha():
            res += chr((ord(t) - 65 - (ord(k) - 65)) % 26 + 65)
        else:
            res += t
    return res