#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


if getenv('AUTH_TYPE') == 'auth':
    auth = Auth()
elif getenv('AUTH_TYPE') == 'basic_auth':
    auth = BasicAuth()
elif getenv('AUTH_TYPE') == 'session_auth':
    auth = SessionAuth()
elif getenv('AUTH_TYPE') == 'session_exp_auth':
    auth = SessionExpAuth()
elif getenv('AUTH_TYPE') == 'session_db_auth':
    auth = SessionDBAuth()


@app.before_request
def before_request_handler():
    """ This is a function that handle the request before sending
    """

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login'
    ]

    if auth and auth.require_auth(request.path, excluded_paths):
        if (not auth.authorization_header(request) and
                not auth.session_cookie(request)):
            abort(401)
        if not auth.current_user(request):
            abort(403)
        request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ This function handle unauthozie error """
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response


@app.errorhandler(403)
def forbidden(error) -> str:
    """ This is a function that handle forbidden error """
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
