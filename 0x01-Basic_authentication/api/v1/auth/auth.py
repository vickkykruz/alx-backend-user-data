#!/usr/bin/env python3
"""
This is a module that handle the authenication of every user
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ This is a class that handle the user Authenication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Get the Authorization header from the request.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user based on the request.
        """
        return None
