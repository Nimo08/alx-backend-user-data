#!/usr/bin/env python3
"""Basic Flask app"""


from flask import Flask, jsonify, Response, request, abort, make_response
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


@app.route("/sessions", methods=['POST'])
def login():
    """Log in"""
    try:
        email = request.form["email"]
        password = request.form["password"]
        session_id = AUTH.create_session(email, password)
        user = AUTH._db.find_user_by(email=email)
        payload = {"email": user.email, "message": "logged in"}
        response = make_response(jsonify(payload))
        response.set_cookie("session_id", session_id)
        return response
    except Exception:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
