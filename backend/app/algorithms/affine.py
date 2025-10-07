def affine_encrypt(text, a=5, b=8):
    result = ""
    for char in text.upper():
        if char.isalpha():
            x = ord(char) - ord('A')
            result += chr(((a * x + b) % 26) + ord('A'))
        else:
            result += char
    return result
