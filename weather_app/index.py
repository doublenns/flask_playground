#!/usr/bin/env python

from flask import Flask
import os
import urllib2

app = Flask(__name__)


def get_api_key():
    '''
    Function reads API key from user's home directory.
    File must be named "openweathermap.api_key"
    '''
    homedir = os.path.expanduser("~")
    with open(homedir+"/openweathermap.api_key", "r") as f:
        api_key = f.read()
    return api_key

def get_weather():
    api_key = get_api_key()
    url = ("http://api.openweathermap.org/data/2.5/weather?q=charlotte,"
        "&mode=json&units=imperial&APPID=" + api_key)
    response = urllib2.urlopen(url).read()
    return response


@app.route("/")
def index():
    return get_weather()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
