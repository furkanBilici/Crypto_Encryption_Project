def vigenere_encrypt(text, key):
    result = []
    key = key.upper()
    key_len = len(key)
    for i, char in enumerate(text.upper()):
        if char.isalpha():
            shift = ord(key[i % key_len]) - ord('A')
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(char)
    return "".join(result)
def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    j = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[j % len(key)]) - 65
            base = 'A' if char.isupper() else 'a'
            result += chr((ord(char) - ord(base) - shift) % 26 + ord(base))
            j += 1
        else:
            result += char
    return result
