#!/usr/bin/env python

from flask import Flask
import os
import urllib2
import json
import time


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
    '''
    Makes a web query against openweathermap API for weather in Charlotte
    '''
    api_key = get_api_key()
    url = ("http://api.openweathermap.org/data/2.5/daily?q=Charlotte,"
        "&cnt=10&mode=json&units=imperial&APPID=" + api_key)
    response = urllib2.urlopen(url).read()
    return response


@app.route("/")
def index():
    data = json.loads(get_weather())
    page = "<html><head><title>My Weather</title></head><body>"
    page += "<h1>Weather for {}, {}</h1>".format(data.get("city").get("name"),
            data.get("city").get("county"))
    for day in data.get("list"):
        page += ("<b>date:</b> {} <b>min:</b> {} <b>max:</b> {}"
                "<b>description</b> {} <br /> ").format(
                        time.strftime('%d %B', time.localtime(day.get("dt"))),
                        (day.get("temp").get("min")),
                        day.get("temp").get("max"),
                        day.get("weather")[0].get("description"))
    page += "</body></html>"
    return page


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
