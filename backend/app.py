from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import json

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
except ImportError:
    print("Algoritma dosyaları bulunamadı!")

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'chat.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False) 

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)
    encrypted_content = db.Column(db.Text, nullable=False)
    method = db.Column(db.String(20), nullable=False)
    params = db.Column(db.String(500), default="{}")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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
    return text

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Bu kullanıcı adı zaten alınmış!"}), 400
    
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Kayıt başarılı! Şimdi giriş yapabilirsiniz."})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "Giriş başarılı", "user_id": user.id, "username": user.username})
    else:
        return jsonify({"error": "Kullanıcı adı veya şifre hatalı!"}), 401


@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        sender = data.get('sender')
        receiver = data.get('receiver')
        
        recipient_user = User.query.filter_by(username=receiver).first()
        
        if not recipient_user:
            return jsonify({"status": "error", "error": f"'{receiver}' adında bir kullanıcı bulunamadı! Mesaj gönderilmedi."}), 404

        text = data.get('text')
        method = data.get('method')
        
        params = {
            'shift': data.get('shift'),
            'key': data.get('key'),
            'a': data.get('a'),
            'b': data.get('b'),
            'x': data.get('x'),
            'ro': data.get('ro'),
            'kontrol': data.get('kontrol')
        }

        encrypted_text = run_encryption(method, text, "encrypt", **params)

        db_params = params.copy()
        if 'key' in db_params: del db_params['key']
        
        new_msg = Message(
            sender=sender, 
            receiver=receiver, 
            encrypted_content=encrypted_text, 
            method=method,
            params=json.dumps(db_params)
        )
        db.session.add(new_msg)
        db.session.commit()

        return jsonify({"status": "success", "message": "Mesaj şifrelendi ve gönderildi."})

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/get_inbox/<username>', methods=['GET'])
def get_inbox(username):
    messages = Message.query.filter_by(receiver=username).order_by(Message.timestamp.desc()).all()
    inbox_data = []
    for msg in messages:
        inbox_data.append({
            "id": msg.id,
            "sender": msg.sender,
            "content": msg.encrypted_content,
            "method": msg.method,
            "params": msg.params,
            "timestamp": msg.timestamp.strftime("%H:%M")
        })
    return jsonify(inbox_data)

@app.route('/decrypt_message', methods=['POST'])
def decrypt_message_endpoint():
    try:
        data = request.json
        cipher_text = data.get('cipher_text')
        method = data.get('method')
        user_key = data.get('key')
        stored_params = data.get('params', {}) 
        if isinstance(stored_params, str): stored_params = json.loads(stored_params)
        
        stored_params['key'] = user_key
        decrypted_text = run_encryption(method, cipher_text, "decrypt", **stored_params)
        
        return jsonify({"status": "success", "plaintext": decrypted_text})
    except Exception as e:
        return jsonify({"status": "error", "error": "Şifre çözülemedi."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)