#!/usr/bin/env python3
""" This is a module that handke encryption """


import bcrypt


def hash_password(password: str) -> bytes:
    """ This returns a salted, hashed password.
    which is a byte string """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
