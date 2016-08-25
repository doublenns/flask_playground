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

@app.route("/hello/<name>")
def hello_name(name):
    return "Hey {}! How ya doin today, buddy?".format(name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
