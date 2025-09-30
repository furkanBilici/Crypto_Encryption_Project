from flask import request, jsonify
from .algorithms.caesar import caesar_cipher
from .algorithms.rot13 import rot13_cipher

def register_routes(app):
    @app.route("/encrypt", methods=["POST"])
    def encrypt():
        data = request.json or {}
        text = data.get("text", "")
        method = data.get("method", "")
        shift = int(data.get("shift", 3))

        if method == "caesar":
            encrypted = caesar_cipher(text, shift)
        elif method == "rot13":
            encrypted = rot13_cipher(text)
        else:
            return jsonify({"error": "Invalid method"}), 400

        return jsonify({"encrypted": encrypted})
