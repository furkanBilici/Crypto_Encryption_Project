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
