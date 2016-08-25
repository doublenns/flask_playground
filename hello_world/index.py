#!/usr/bin/env python

from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, wonderful world!"

@app.route("/goodbye")
def goodbye():
    return "Goodbye, cruel world!"

# If age isn't an int, server simply returns a 404 status code
@app.route("/hello/<name>/<int:age>")
def hello_name(name, age):
    return "Hey {}! How is like being {} years old?".format(name, age)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
