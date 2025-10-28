def polybius_encrypt(text):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    table = {}
    index = 0
    for i in range(1, 6):
        for j in range(1, 6):
            table[alphabet[index]] = (i, j)
            index += 1

    sifre = []
    for c in text.upper():
        if c == 'J':
            c = 'I'
        if c in table:
            i, j = table[c]
            sifre.append(str(i) + str(j))
        elif c == ' ':
            sifre.append(' ')
    return ''.join(sifre)


def polybius_decrypt(cipher):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    reverse_table = {}
    index = 0
    for i in range(1, 6):
        for j in range(1, 6):
            reverse_table[str(i) + str(j)] = alphabet[index]
            index += 1

    text = ""
    i = 0
    while i < len(cipher):
        if cipher[i] == ' ':
            text += ' '
            i += 1
        else:
            pair = cipher[i:i+2]
            if pair in reverse_table:
                text += reverse_table[pair]
            else:
                text += '?'
            i += 2
    return text
