#!/usr/bin/env python3
"""Basic Flask app"""

from flask import Flask, jsonify, Response, request
from auth import Auth
AUTH = Auth()


app = Flask(__name__)


@app.route("/")
def index() -> Response:
    """
    GET route
    Return a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """POST /users"""
    try:
        email = request.form["email"]
        password = request.form["password"]
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
