from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import json
import time
import secrets

try:
    from algorithms.caesar import caesar_cipher, caesar_decrypt
    from algorithms.vigenere import vigenere_encrypt, vigenere_decrypt
    from algorithms.substitution import substitution_encrypt, substitution_decrypt
    from algorithms.affine import affine_encrypt, affine_decrypt
    from algorithms.railfence import rail_fence_cipher, railfence_decrypt
    from algorithms.route import route_cipher, route_decrypt
    from algorithms.columnar import columnar_encrypt, columnar_decrypt
    from algorithms.polybius import polybius_encrypt, polybius_decrypt
    from algorithms.pigpen import pigpen_encrypt, pigpen_decrypt
    from algorithms.playfair import playfair_encrypt, playfair_decrypt
    from algorithms.hill import hill_encrypt, hill_decrypt
    from algorithms.vernam import vernam_encrypt, vernam_decrypt
    from algorithms.aes_lib import aes_lib_encrypt, aes_lib_decrypt
    from algorithms.aes_manual import aes_manual_encrypt, aes_manual_decrypt
    from algorithms.des_manual import des_manual_encrypt, des_manual_decrypt
    from algorithms.rsa import generate_rsa_keypair, rsa_hybrid_encrypt, rsa_hybrid_decrypt
except ImportError:
    pass

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'chat.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    public_key = db.Column(db.Text, nullable=True)
    private_key = db.Column(db.Text, nullable=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)
    encrypted_content = db.Column(db.Text, nullable=False)
    method = db.Column(db.String(20), nullable=False)
    params = db.Column(db.String(500), default="{}")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    process_time = db.Column(db.Float, default=0.0)
    is_file = db.Column(db.Boolean, default=False)
    filename = db.Column(db.String(100), nullable=True)

with app.app_context():
    db.create_all()

def run_encryption(method, text, action, **kwargs):
    shift = int(kwargs.get('shift', 3) or 3)
    key = kwargs.get('key', 'KEY')
    a = int(kwargs.get('a', 5) or 5)
    b = int(kwargs.get('b', 8) or 8)
    x = int(kwargs.get('x', 3) or 3)
    ro = int(kwargs.get('ro', 5) or 5)
    kontrol = kwargs.get('kontrol', True)

    if method == "caesar":
        return caesar_cipher(text, shift) if action == "encrypt" else caesar_decrypt(text, shift)
    elif method == "vigenere":
        return vigenere_encrypt(text, key) if action == "encrypt" else vigenere_decrypt(text, key)
    elif method == "substitution":
        return substitution_encrypt(text) if action == "encrypt" else substitution_decrypt(text)
    elif method == "affine":
        return affine_encrypt(text, a, b) if action == "encrypt" else affine_decrypt(text, a, b)
    elif method == "railfence":
        return rail_fence_cipher(text, x) if action == "encrypt" else railfence_decrypt(text, x)
    elif method == "route":
        return route_cipher(text, ro, kontrol) if action == "encrypt" else route_decrypt(text, ro, kontrol)
    elif method == "columnar":
        return columnar_encrypt(text, key) if action == "encrypt" else columnar_decrypt(text, key)
    elif method == "polybius":
        return polybius_encrypt(text) if action == "encrypt" else polybius_decrypt(text)
    elif method == "pigpen":
        return pigpen_encrypt(text) if action == "encrypt" else pigpen_decrypt(text)
    elif method == "playfair":
        return playfair_encrypt(text, key) if action == "encrypt" else playfair_decrypt(text, key)
    elif method == "hill":
        return hill_encrypt(text, key) if action == "encrypt" else hill_decrypt(text, key)
    elif method == "vernam":
        return vernam_encrypt(text, key) if action == "encrypt" else vernam_decrypt(text, key)
    elif method == "aes_lib":
        return aes_lib_encrypt(text, key) if action == "encrypt" else aes_lib_decrypt(text, key)
    elif method == "aes_manual":
        return aes_manual_encrypt(text, key) if action == "encrypt" else aes_manual_decrypt(text, key)
    elif method == "des_manual":
        return des_manual_encrypt(text, key) if action == "encrypt" else des_manual_decrypt(text, key)

    return text

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Kullanıcı adı alınmış"}), 400
    priv, pub = generate_rsa_keypair()
    new_user = User(username=username, password=password, public_key=pub, private_key=priv)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Kayıt başarılı!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username'), password=data.get('password')).first()
    if user:
        return jsonify({"message": "Giriş başarılı", "user_id": user.id, "username": user.username})
    return jsonify({"error": "Hatalı giriş"}), 401

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        start_time = time.time()

        data = request.json
        sender = data.get('sender')
        receiver = data.get('receiver')
        text = data.get('text')
        method = data.get('method')
        is_file = data.get('is_file', False)
        filename = data.get('filename', None)

        recipient_user = User.query.filter_by(username=receiver).first()
        if not recipient_user:
            return jsonify({"status": "error", "error": "Alıcı bulunamadı"}), 404

        params = {
            'shift': data.get('shift'),
            'key': data.get('key'),
            'a': data.get('a'),
            'b': data.get('b'),
            'x': data.get('x'),
            'ro': data.get('ro'),
            'kontrol': data.get('kontrol')
        }

        if method == "rsa_hybrid":
            if not recipient_user.public_key:
                return jsonify({"status": "error", "error": "Public Key yok"}), 400
            encrypted_text = rsa_hybrid_encrypt(text, recipient_user.public_key)
        else:
            encrypted_text = run_encryption(method, text, "encrypt", **params)

        duration = time.time() - start_time

        db_params = params.copy()
        db_params.pop('key', None)

        new_msg = Message(
            sender=sender,
            receiver=receiver,
            encrypted_content=encrypted_text,
            method=method,
            params=json.dumps(db_params),
            process_time=duration,
            is_file=is_file,
            filename=filename
        )

        db.session.add(new_msg)
        db.session.commit()

        return jsonify({"status": "success", "time": duration})

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/get_inbox/<username>', methods=['GET'])
def get_inbox(username):
    messages = Message.query.filter_by(receiver=username).order_by(Message.timestamp.desc()).all()
    return jsonify([
        {
            "id": msg.id,
            "sender": msg.sender,
            "content": msg.encrypted_content,
            "method": msg.method,
            "params": msg.params,
            "timestamp": msg.timestamp.strftime("%H:%M"),
            "process_time": msg.process_time,
            "is_file": msg.is_file,
            "filename": msg.filename
        } for msg in messages
    ])

@app.route('/decrypt_message', methods=['POST'])
def decrypt_message_endpoint():
    try:
        start_time = time.time()

        data = request.json
        cipher_text = data.get('cipher_text')
        method = data.get('method')
        user_key = data.get('key')
        requesting_user = data.get('username')

        if method == "rsa_hybrid":
            user = User.query.filter_by(username=requesting_user).first()
            if not user or not user.private_key:
                return jsonify({"error": "Private key yok"}), 400
            decrypted_text = rsa_hybrid_decrypt(cipher_text, user.private_key)
        else:
            stored_params = data.get('params', {})
            if isinstance(stored_params, str):
                stored_params = json.loads(stored_params)
            stored_params['key'] = user_key
            decrypted_text = run_encryption(method, cipher_text, "decrypt", **stored_params)

        return jsonify({
            "status": "success",
            "plaintext": decrypted_text,
            "time": time.time() - start_time
        })

    except Exception:
        return jsonify({"status": "error", "error": "Çözülemedi"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
