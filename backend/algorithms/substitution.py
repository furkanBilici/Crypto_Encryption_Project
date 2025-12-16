import string

def substitution_encrypt(text, mapping=None):
    alphabet = string.ascii_uppercase
    if mapping is None:
        mapping = "QWERTYUIOPASDFGHJKLZXCVBNM"  # örnek mapping
    table = str.maketrans(alphabet, mapping)
    return text.upper().translate(table)
def substitution_decrypt(text, key_map="QWERTYUIOPASDFGHJKLZXCVBNM"):
    alphabet = string.ascii_uppercase
    table = str.maketrans(key_map.upper(), alphabet)
    return text.upper().translate(table)