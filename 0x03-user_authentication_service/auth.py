#!/usr/bin/env python3
""" This is a module that handle the authenication of the user """


from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """ Generate a salt and hash the password with bcrypt """

    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password
