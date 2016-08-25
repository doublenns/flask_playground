#!/usr/bin/env python

from flask import Flask
from flask import render_template
import os
import urllib2
import json
import time


app = Flask(__name__)


def get_api_key():
    '''
    Function reads API key from user's home directory.
    File must be named ".openweathermap.api_key"
    '''
    homedir = os.path.expanduser("~")
    with open(homedir+"/.openweathermap.api_key", "r") as f:
        api_key = f.read()
    return api_key

def get_weather(city):
    '''
    Makes a web query against openweathermap API for weather in Charlotte
    '''
    api_key = get_api_key()
    url = ("http://api.openweathermap.org/data/2.5/forecast/daily?"
        "q={}&mode=json&units=imperial&APPID=".format(city) + api_key)
    response = urllib2.urlopen(url).read()
    return response


@app.route("/")
@app.route("/<searchcity>")
def index(searchcity="Charlotte"):
    data = json.loads(get_weather(searchcity))
    city = data["city"]["name"]
    country = data["city"]["country"]
    forecast_list = []

    for d in data.get("list"):
        day = time.strftime('%d %B', time.localtime(d.get("dt")))
        mini = d.get("temp").get("min")
        maxi = d.get("temp").get("max")
        description = d.get("weather")[0].get("description")
        forecast_list.append((day, mini, maxi, description))

    return render_template("index.html", city=city, country=country,
        forecast_list=forecast_list)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
