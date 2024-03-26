#!/usr/bin/env python3
"""End-to-end integration test"""


import requests
from app import AUTH

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user"""
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt login with wrong password"""
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in and return session ID"""
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    if response.status_code == 401:
        return "Invalid login credentials"
    assert response.status_code == 200
    assert "email" in response.json()
    assert "message" in response.json()
    session_id = response.cookies.get("session_id")
    return session_id


def profile_unlogged() -> None:
    """Check profile while unlogged"""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Check profile while logged in"""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    user = AUTH.get_user_from_session_id(session_id)
    assert user.email == data["email"]


def log_out(session_id: str) -> None:
    """Log out"""
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200, "Failed to log out"
    print("Successfully logged out.")


def reset_password_token(email: str) -> str:
    """Get reset password token"""
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "email" in data
    assert response.json()["email"] == email
    token = response.json()["reset_token"]
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password"""
    url = f"{BASE_URL}/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated"
    assert response.json()["email"] == email


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
