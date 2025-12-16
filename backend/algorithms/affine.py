def mod_inverse(a, m):
    for i in range(26):
        if (a * i) % m == 1:
            return i
    raise ValueError("No modular inverse for given 'a'.")

def affine_encrypt(text, a, b):
    result = ""
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            result += chr(((a * (ord(char) - ord(base)) + b) % 26) + ord(base))
        else:
            result += char
    return result

def affine_decrypt(text, a, b):
    result = ""
    a_inv = mod_inverse(a, 26)
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            result += chr((a_inv * ((ord(char) - ord(base)) - b)) % 26 + ord(base))
        else:
            result += char
    return result
