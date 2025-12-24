def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = 65 if char.isupper() else 97
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_cipher(text, -shift)