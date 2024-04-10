#!/usr/bin/env python3
""" This is a module that handke encryption """


import bcrypt


def hash_password(password: str) -> bytes:
    """ This returns a salted, hashed password.
    which is a byte string """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Thia function checks if a password is valid """
    return bcrypt.checkpw(password.encode(), hashed_password)
