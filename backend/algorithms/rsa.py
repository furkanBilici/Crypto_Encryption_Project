from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def generate_rsa_keypair():
    key = RSA.generate(2048)
    return key.export_key().decode(), key.publickey().export_key().decode()

def rsa_hybrid_encrypt(text, pub_key_pem):
    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    ct_bytes = cipher_aes.encrypt(pad(text.encode(), AES.block_size))
    
    rsa_key = RSA.import_key(pub_key_pem)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    
    packet = enc_session_key + cipher_aes.iv + ct_bytes
    return base64.b64encode(packet).decode()

def rsa_hybrid_decrypt(packet_b64, priv_key_pem):
    try:
        packet = base64.b64decode(packet_b64)
        rsa_key = RSA.import_key(priv_key_pem)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        
        enc_session_key = packet[:256] 
        iv = packet[256:256+16]
        ct = packet[256+16:]
        
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
        return unpad(cipher_aes.decrypt(ct), AES.block_size).decode()
    except Exception as e:
        return f"RSA Error: {e}"