#!/usr/bin/env python3
""" This is a module that manages the API authenications """


from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ This is a session auth class that handle the given methods """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ This is a method that creates the session ID for the user_id """

        if isinstance(user_id, str):
            session_id = str(uuid.uuid4())
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ This is a method that gets the session id """

        if isinstance(session_id, str):
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ This is a method that return a User instance based on
            a cookie value
        """
        return User.get(
            self.user_id_for_session_id(self.session_cookie(request)))

    def destroy_session(self, request=None):
        """ This is a method that delete the user session / log out
        """
        if request:
            session_id = self.session_cookie(request)
            if not session_id:
                return False
            if not self.user_id_for_session_id(session_id):
                return False
            self.user_id_by_session_id.pop(session_id)
            return True
