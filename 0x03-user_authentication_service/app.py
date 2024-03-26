#!/usr/bin/env python3
"""Basic Flask app"""


from flask import Flask, jsonify, Response, request, abort, redirect, url_for
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
    email = request.form["email"]
    password = request.form["password"]
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=['DELETE'])
def logout():
    """ Log out"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for("index"))
    else:
        abort(403)


@app.route("/profile", methods=['GET'])
def profile():
    """User profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
