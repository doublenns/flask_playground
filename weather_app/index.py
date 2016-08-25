#!/usr/bin/env python

from flask import Flask
import os
import urllib2

app = Flask(__name__)

# Need to create an API key to see results
def get_weather():
    url = ("http://api.openweathermap.org/data/2.5/weather?q=charlotte,"
        "&units=imperial")
    response = urllib2.urlopen(url).read()
    return response


@app.route("/")
def index():
    return get_weather()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
