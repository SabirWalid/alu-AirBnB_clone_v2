#!/usr/bin/python3
"""Start a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /: Display "Hello HBNB!"
    /hbnb: Display "HBNB"
    /c/<text>: Display "C followed by number of characters in <text>"
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display "Hello HBNB!"."""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display "HBNB"."""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def C(text):
    """Display "C followed by number of characters in <text>"""
    text = text.replace('_', ' ')
    return "c {}" .format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
