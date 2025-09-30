from .caesar import caesar_cipher

def rot13_cipher(text):
    return caesar_cipher(text, 13)
