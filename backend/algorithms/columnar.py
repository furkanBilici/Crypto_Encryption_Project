def columnar_encrypt(text, key):
    while len(text) % len(key) != 0:
        text += '*'
    columns = {char: [] for char in key}
    for i, char in enumerate(text):
        column_key = key[i % len(key)]
        columns[column_key].append(char)
    sorted_key = sorted(key)
    encrypted = []
    for k in sorted_key:
        encrypted.extend(columns[k])
    return ''.join(encrypted)


def columnar_decrypt(cipher, key):
    n_cols = len(key)
    n_rows = len(cipher) // n_cols
    sorted_key = sorted(key)
    
    # Hangi sütun hangi sırada geldiğini bulalım
    order = {char: i for i, char in enumerate(sorted_key)}
    reverse_order = sorted(range(n_cols), key=lambda i: order[key[i]])
    
    # Her sütun için karakterleri ayıralım
    col_length = n_rows
    columns = {}
    index = 0
    for char in sorted_key:
        columns[char] = list(cipher[index:index + col_length])
        index += col_length
    
    # Çözülmüş metni sırayla oluştur
    plain = ''
    for i in range(n_rows):
        for char in key:
            plain += columns[char][i]
    return plain.replace('*', '')
