import string

def substitution_encrypt(text, mapping=None):
    alphabet = string.ascii_uppercase
    if mapping is None:
        mapping = "QWERTYUIOPASDFGHJKLZXCVBNM"  # örnek mapping
    table = str.maketrans(alphabet, mapping)
    return text.upper().translate(table)
