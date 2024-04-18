#!/usr/bin/env python3
"""
This is a module that handle the authenication of every user
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ This is a class that handle the user Authenication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[:1]):
                    return False
        return False if path in excluded_paths else True

    def authorization_header(self, request=None) -> str:
        """
        Get the Authorization header from the request.
        """
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user based on the request.
        """
        return None

    def session_cookie(self, request=None):
        """ This is a  method that return a cookie value from a request
        """
        if request:
            return request.cookies.get(getenv('SESSION_NAME'))
