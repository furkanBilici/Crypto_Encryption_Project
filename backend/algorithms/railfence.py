def rail_fence_cipher(text, rails):
    fence = [['\n' for _ in range(len(text))] for _ in range(rails)]
    dir_down, row, col = False, 0, 0
    for c in text:
        if row == 0 or row == rails - 1:
            dir_down = not dir_down
        fence[row][col] = c
        col += 1
        row += 1 if dir_down else -1
    result = []
    for i in range(rails):
        for j in range(len(text)):
            if fence[i][j] != '\n':
                result.append(fence[i][j])
    return "".join(result)

def railfence_decrypt(cipher, rails):
    fence = [['\n' for _ in range(len(cipher))] for _ in range(rails)]
    dir_down, row, col = None, 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == rails - 1:
            dir_down = False
        fence[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1
    index = 0
    for i in range(rails):
        for j in range(len(cipher)):
            if fence[i][j] == '*' and index < len(cipher):
                fence[i][j] = cipher[index]
                index += 1
    result, row, col = [], 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == rails - 1:
            dir_down = False
        if fence[row][col] != '\n':
            result.append(fence[row][col])
            col += 1
        row += 1 if dir_down else -1
    return "".join(result)
