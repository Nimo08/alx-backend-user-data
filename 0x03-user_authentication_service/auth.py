#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt
from db import DB
from user import User


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Take mandatory email and password string arguments
        and return a User object
        """
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists")
        hashed_pwd = _hash_password(password)
        user_obj = self._db.add_user(email, hashed_pwd)
        return user_obj


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string arguments and returns bytes
    """
    decoded_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    result = bcrypt.hashpw(decoded_bytes, salt)
    return result
