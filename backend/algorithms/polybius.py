def polybius_encrypt(text):
    text = text.upper().replace("J", "I")
    grid = [
        ['A','B','C','D','E'],
        ['F','G','H','I','K'],
        ['L','M','N','O','P'],
        ['Q','R','S','T','U'],
        ['V','W','X','Y','Z']
    ]
    res = ""
    for char in text:
        if not char.isalpha(): continue
        for r in range(5):
            for c in range(5):
                if grid[r][c] == char:
                    res += f"{r+1}{c+1} "
    return res.strip()

def polybius_decrypt(text):
    text = text.replace(" ", "")
    grid = [
        ['A','B','C','D','E'],
        ['F','G','H','I','K'],
        ['L','M','N','O','P'],
        ['Q','R','S','T','U'],
        ['V','W','X','Y','Z']
    ]
    res = ""
    for i in range(0, len(text), 2):
        r = int(text[i]) - 1
        c = int(text[i+1]) - 1
        res += grid[r][c]
    return res