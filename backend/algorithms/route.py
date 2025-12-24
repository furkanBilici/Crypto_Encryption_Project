import math

def route_cipher(text, cols, spiral=False):
    text = text.replace(" ", "")
    rows = math.ceil(len(text) / cols)
    grid = [['X' for _ in range(cols)] for _ in range(rows)]
    
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
    
    cipher = ""
    for c in range(cols):
        for r in range(rows):
            cipher += grid[r][c]
    return cipher

def route_decrypt(text, cols, spiral=False):
    rows = math.ceil(len(text) / cols)
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    
    idx = 0
    for c in range(cols):
        for r in range(rows):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
                
    plain = ""
    for r in range(rows):
        for c in range(cols):
            plain += grid[r][c]
    return plain.replace("X", "")