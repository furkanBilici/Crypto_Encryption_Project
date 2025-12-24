import numpy as np

def text_to_nums(text):
    return [ord(c)-65 for c in text.upper() if c.isalpha()]

def nums_to_text(nums):
    return "".join([chr(int(n)+65) for n in nums])

def get_matrix(key, n):
    nums = text_to_nums(key)
    if len(nums) < n*n: nums += [0]*(n*n - len(nums)) 
    return np.array(nums[:n*n]).reshape(n,n)

def matrix_mod_inv(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = pow(det, -1, modulus)
    matrix_inv = (det_inv * np.round(det * np.linalg.inv(matrix)).astype(int)) % modulus
    return matrix_inv

def hill_encrypt(text, key):
    n = 2 if len(key) <= 4 else 3
    key_matrix = get_matrix(key, n)
    nums = text_to_nums(text)
    while len(nums) % n != 0: nums.append(23) 
    
    cipher_nums = []
    for i in range(0, len(nums), n):
        vec = np.array(nums[i:i+n])
        res = np.dot(key_matrix, vec) % 26
        cipher_nums.extend(res)
    return nums_to_text(cipher_nums)

def hill_decrypt(text, key):
    try:
        n = 2 if len(key) <= 4 else 3
        key_matrix = get_matrix(key, n)
        inv_matrix = matrix_mod_inv(key_matrix, 26)
        
        nums = text_to_nums(text)
        plain_nums = []
        for i in range(0, len(nums), n):
            vec = np.array(nums[i:i+n])
            res = np.dot(inv_matrix, vec) % 26
            plain_nums.extend(res)
        return nums_to_text(plain_nums)
    except:
        return "HATA: Anahtarın tersi alınamadı."