#!/usr/bin/env python3
""" This is a module that handle the authenication of the user """


from bcrypt import hashpw, gensalt, checkpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ Generate a salt and hash the password with bcrypt """

    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """ Generate a new UUID
    Args:
        None
    Return:
        A string representation
    """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ validates the user credentials

        Args:
            email (str): email of the user
            password (str): password of the user

        Return:
            True: valid user
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False

        return checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """ creates a session id for a user
        Args:
            email (str): user's email address

        Return:
            A string representation of the session id
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Get the user object
        Args:
            session_id (str): the string representation of the session_id
        Returns:
            User object or None
        """
        if session_id:
            try:
                return self._db.find_user_by(session_id=session_id)
            except Exception:
                return None

    def destroy_session(self, user_id: int) -> None:
        """ destroys a user session
        Args:
            user_id (int): This user id
        Return:
            Update User object
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """get reset password token

        Args:
            email (str): user email address

        Raises:
            ValueError: if the user is not found

        Returns:
            str: A string representation of a reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update password

        Args:
            reset_token (str): the reset token
            password (str): the user password

        Raises:
            ValueError: if not found user

        Return:
            Update User Object
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
