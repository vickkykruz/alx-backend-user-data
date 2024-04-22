#!/usr/bin/env python3
""" This is a module that handle the Flask app """


from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=["GET"], strict_slashes=False)
def index_page() -> str:
    """ This GET the route index page

    Return:
        str: json {'message': 'Bienvenue'}
    """
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
