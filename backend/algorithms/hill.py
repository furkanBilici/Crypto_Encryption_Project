import numpy as np

def text_to_numbers(text):
    return [ord(char) - 65 for char in text.upper() if char.isalpha()]

def numbers_to_text(numbers):
    return "".join([chr(int(num) + 65) for num in numbers])

def get_key_matrix(key, n):
    key_nums = text_to_numbers(key)
    if len(key_nums) != n*n:
        raise ValueError(f"Key uzunluğu {n*n} olmalı (Örn: 2x2 için 4 harf)")
    return np.array(key_nums).reshape(n, n)

def matrix_mod_inv(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = pow(det, -1, modulus)
    matrix_modulus_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )
    return matrix_modulus_inv

def hill_encrypt(text, key):
    n = int(len(key)**0.5) 
    key_matrix = get_key_matrix(key, n)
    nums = text_to_numbers(text)
    
    while len(nums) % n != 0:
        nums.append(23)
        
    encrypted_nums = []
    for i in range(0, len(nums), n):
        vector = np.array(nums[i:i+n])
        res = np.dot(key_matrix, vector) % 26
        encrypted_nums.extend(res)
        
    return numbers_to_text(encrypted_nums)

def hill_decrypt(text, key):
    n = int(len(key)**0.5)
    key_matrix = get_key_matrix(key, n)
    
    try:
        inv_key_matrix = matrix_mod_inv(key_matrix, 26)
    except:
        return "HATA: Bu anahtarın tersi alınamaz (Determinant mod 26 ile uyumsuz)."

    nums = text_to_numbers(text)
    decrypted_nums = []
    for i in range(0, len(nums), n):
        vector = np.array(nums[i:i+n])
        res = np.dot(inv_key_matrix, vector) % 26
        decrypted_nums.extend(res)
        
    return numbers_to_text(decrypted_nums)