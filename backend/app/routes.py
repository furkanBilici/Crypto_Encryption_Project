from flask import request, jsonify
from .algorithms.caesar import caesar_cipher
from .algorithms.vigenere import vigenere_encrypt
from .algorithms.substitution import substitution_encrypt
from .algorithms.affine import affine_encrypt
from .algorithms.railfence import rail_fence_cipher
from .algorithms.route import route_cipher

def register_routes(app):
    @app.route("/encrypt", methods=["POST"])
    def encrypt():
        data = request.get_json()
        text = data.get("text", "")
        method = data.get("method", "")
        shift = data.get("shift", 3)
        key = data.get("key", "KEY")  # vigenere için
        a = data.get("a", 5)          # affine için
        b = data.get("b", 8)
        x=data.get("x",3)#railfnce icin
        ro=data.get("ro",5)#route için
        kontrol=data.get("kontrol",True)

        if method == "caesar":
            encrypted = caesar_cipher(text, shift)
        elif method == "vigenere":
            encrypted = vigenere_encrypt(text, key)
        elif method == "substitution":
            encrypted = substitution_encrypt(text)
        elif method == "affine":
            encrypted = affine_encrypt(text, a, b)
        elif method== "railfence":
            encrypted= rail_fence_cipher(text, x)
        elif method== "route":
            encrypted= route_cipher(text, ro, kontrol)
        else:
            return jsonify({"error": "Unknown encryption method"}), 400

        return jsonify({"encrypted": encrypted})
