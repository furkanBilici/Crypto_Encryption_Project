import math

def route_cipher(text, n, clockwise=True):
    rows = math.ceil(len(text) / n)
    matrix = [['' for _ in range(n)] for _ in range(rows)]
    idx = 0
    for i in range(rows):
        for j in range(n):
            matrix[i][j] = text[idx] if idx < len(text) else 'X'
            idx += 1
    res = []
    left, right, top, bottom = 0, n - 1, 0, rows - 1
    while left <= right and top <= bottom:
        if clockwise:
            for i in range(left, right + 1):
                res.append(matrix[top][i])
            top += 1
            for i in range(top, bottom + 1):
                res.append(matrix[i][right])
            right -= 1
            for i in range(right, left - 1, -1):
                res.append(matrix[bottom][i])
            bottom -= 1
            for i in range(bottom, top - 1, -1):
                res.append(matrix[i][left])
            left += 1
        else:
            for i in range(top, bottom + 1):
                res.append(matrix[i][left])
            left += 1
            for i in range(left, right + 1):
                res.append(matrix[bottom][i])
            bottom -= 1
            for i in range(bottom, top - 1, -1):
                res.append(matrix[i][right])
            right -= 1
            for i in range(right, left - 1, -1):
                res.append(matrix[top][i])
            top += 1
    return "".join(res)

def route_decrypt(cipher, n, clockwise=True):
    rows = math.ceil(len(cipher) / n)
    matrix = [['' for _ in range(n)] for _ in range(rows)]
    res, left, right, top, bottom, idx = [], n - 1, 0, 0, rows - 1, 0
    result = [['' for _ in range(n)] for _ in range(rows)]
    text = list(cipher)
    left, right, top, bottom = 0, n - 1, 0, rows - 1
    while left <= right and top <= bottom:
        if clockwise:
            for i in range(left, right + 1):
                if idx < len(text): result[top][i] = text[idx]; idx += 1
            top += 1
            for i in range(top, bottom + 1):
                if idx < len(text): result[i][right] = text[idx]; idx += 1
            right -= 1
            for i in range(right, left - 1, -1):
                if idx < len(text): result[bottom][i] = text[idx]; idx += 1
            bottom -= 1
            for i in range(bottom, top - 1, -1):
                if idx < len(text): result[i][left] = text[idx]; idx += 1
            left += 1
        else:
            pass
    return "".join("".join(row) for row in result)
