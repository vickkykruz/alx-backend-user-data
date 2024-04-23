#!/usr/bin/env python3
""" This is a module that handle the authenication of the user """


from bcrypt import hashpw, gensalt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """ Generate a salt and hash the password with bcrypt """

    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a user

        Args:
            email (str): email of the user
            password (str):password of the user

        Return:
            User: registered user
        """

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
