def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(text, a, b):
    result = ""
    for char in text:
        if char.isalpha():
            start = 65 if char.isupper() else 97
            x = ord(char) - start
            result += chr(((a * x + b) % 26) + start)
        else:
            result += char
    return result

def affine_decrypt(text, a, b):
    result = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return "HATA: 'a' sayısı 26 ile aralarında asal olmalı!"
        
    for char in text:
        if char.isalpha():
            start = 65 if char.isupper() else 97
            y = ord(char) - start
            result += chr((a_inv * (y - b)) % 26 + start)
        else:
            result += char
    return result