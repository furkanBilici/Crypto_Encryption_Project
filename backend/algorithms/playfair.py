def prepare_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'X'
        if a == b:
            result += a + 'X'
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += 'X'
    return result

def create_matrix(key):
    key = key.upper().replace("J", "I") + "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    seen = set()
    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_loc(matrix, char):
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == char: return r, c
    return 0, 0

def playfair_encrypt(text, key):
    matrix = create_matrix(key)
    text = prepare_text(text)
    cipher = ""
    for i in range(0, len(text), 2):
        r1, c1 = find_loc(matrix, text[i])
        r2, c2 = find_loc(matrix, text[i+1])
        if r1 == r2:
            cipher += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2: 
            cipher += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else: 
            cipher += matrix[r1][c2] + matrix[r2][c1]
    return cipher

def playfair_decrypt(text, key):
    matrix = create_matrix(key)
    plain = ""
    for i in range(0, len(text), 2):
        r1, c1 = find_loc(matrix, text[i])
        r2, c2 = find_loc(matrix, text[i+1])
        if r1 == r2:
            plain += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            plain += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            plain += matrix[r1][c2] + matrix[r2][c1]
    return plain