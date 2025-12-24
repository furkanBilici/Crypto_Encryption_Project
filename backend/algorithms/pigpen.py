
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
symbols = ["ᒧ", "⊔", "ᒪ", "⊐", "□", "⊏", "¬", "⊓", "Г", 
           "ᒧ·", "⊔·", "ᒪ·", "⊐·", "□·", "⊏·", "¬·", "⊓·", "Г·", 
           "V", "<", ">", "^", "V·", "<·", ">·", "^·"] 

def pigpen_encrypt(text):
    text = text.upper()
    res = ""
    for char in text:
        if char in chars:
            res += symbols[chars.index(char)] + " "
        else:
            res += char
    return res

def pigpen_decrypt(text):
    tokens = text.split(" ")
    res = ""
    for t in tokens:
        if t in symbols:
            res += chars[symbols.index(t)]
        else:
            res += "" 
    return res