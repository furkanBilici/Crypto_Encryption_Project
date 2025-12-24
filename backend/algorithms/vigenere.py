def vigenere_encrypt(text, key):
    key = key.upper()
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            start = 65 if char.isupper() else 97
            result += chr((ord(char) - start + shift) % 26 + start)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    key = key.upper()
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            start = 65 if char.isupper() else 97
            result += chr((ord(char) - start - shift) % 26 + start)
            key_index += 1
        else:
            result += char
    return result