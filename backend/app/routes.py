from flask import request, jsonify
from .algorithms.caesar import caesar_cipher

def register_routes(app):
    @app.route("/encrypt", methods=["POST"])
    def encrypt():
        data = request.json or {}
        text = data.get("text", "")
        method = data.get("method", "")
        shift = int(data.get("shift", 3))

        if method == "caesar":
            encrypted = caesar_cipher(text, shift)
        elif method == "furkan":
            encrypted = "300-500-300-500"
        else:
            return jsonify({"error": "Invalid method"}), 400

        return jsonify({"encrypted": encrypted})
