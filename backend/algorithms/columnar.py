import math

def get_key_order(key):
    return sorted(list(range(len(key))), key=lambda k: key[k])

def columnar_encrypt(text, key):
    order = get_key_order(key)
    col_count = len(key)
    row_count = math.ceil(len(text) / col_count)
    
    padded_text = text + "_" * (row_count * col_count - len(text))
    grid = [padded_text[i:i+col_count] for i in range(0, len(padded_text), col_count)]
    
    cipher = ""
    for index in order:
        for row in grid:
            cipher += row[index]
    return cipher

def columnar_decrypt(text, key):
    order = get_key_order(key)
    col_count = len(key)
    row_count = math.ceil(len(text) / col_count)
    
    grid = [['' for _ in range(col_count)] for _ in range(row_count)]
    idx = 0
    for index in order:
        for r in range(row_count):
            if idx < len(text):
                grid[r][index] = text[idx]
                idx += 1
                
    return "".join("".join(row) for row in grid).replace("_", "")