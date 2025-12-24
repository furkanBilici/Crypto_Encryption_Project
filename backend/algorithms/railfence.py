def rail_fence_cipher(text, key):
    if key <= 1: return text
    fence = [[] for _ in range(key)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == key - 1 or rail == 0:
            direction *= -1

    return "".join("".join(row) for row in fence)

def railfence_decrypt(text, key):
    if key <= 1: return text
    fence = [['\n' for _ in range(len(text))] for _ in range(key)]
    direction, row, col = None, 0, 0

    for i in range(len(text)):
        if row == 0: direction = True
        if row == key - 1: direction = False
        fence[row][col] = '*'
        col += 1
        row += 1 if direction else -1
  
    index = 0
    for i in range(key):
        for j in range(len(text)):
            if (fence[i][j] == '*') and (index < len(text)):
                fence[i][j] = text[index]
                index += 1
      
    result = []
    row, col = 0, 0
    for i in range(len(text)):
        if row == 0: direction = True
        if row == key - 1: direction = False
        if fence[row][col] != '\n':
            result.append(fence[row][col])
            col += 1
        row += 1 if direction else -1
    return "".join(result)