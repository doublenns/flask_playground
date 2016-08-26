#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import os
import urllib2
import json
import time
import datetime

'''
TO-DO: Input validation. (Only alpha. Strip white spaces)
'''


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
def index():
    searchcity = request.args.get("searchcity")
    if not searchcity:
        searchcity = request.cookies.get("last_city")
    if not searchcity:
        searchcity = "Charlotte"

    data = json.loads(get_weather(searchcity))
    try:
        city = data["city"]["name"]
    except KeyError:
        return render_template("invalid_city.html", user_input = searchcity)
    country = data["city"]["country"]

    forecast_list = []
    for d in data.get("list"):
        day = time.strftime('%d %B', time.localtime(d.get("dt")))
        mini = d.get("temp").get("min")
        maxi = d.get("temp").get("max")
        description = d.get("weather")[0].get("description")
        forecast_list.append((day, mini, maxi, description))

    response = make_response(render_template("index.html", city=city,
        country=country, forecast_list=forecast_list))
    #Cookie won't be deleted for a year since their last visit
    response.set_cookie("last_city","{},{}".format(city, country),
        expires=datetime.datetime.today() + datetime.timedelta(days=365))
    return response


#Need to make code more DRY
@app.route("/secure")
def secure():
    searchcity = request.args.get("searchcity")
    if not searchcity:
        searchcity = "Charlotte"

    data = json.loads(get_weather(searchcity))
    try:
        city = data["city"]["name"]
    except KeyError:
        return render_template("invalid_city.html", user_input = searchcity)
    country = data["city"]["country"]
    forecast_list = []

    for d in data.get("list"):
        day = time.strftime('%d %B', time.localtime(d.get("dt")))
        mini = d.get("temp").get("min")
        maxi = d.get("temp").get("max")
        description = d.get("weather")[0].get("description")
        forecast_list.append((day, mini, maxi, description))

    return render_template("secure.html", city=city, country=country,
        forecast_list=forecast_list)


#Need to explicitly allow route to accept post requests
@app.route("/weather", methods=["POST"])
def weather():
    #request.form instead of request.args
    searchcity = request.form.get("searchcity")
    if not searchcity:
        searchcity = "Charlotte"

    data = json.loads(get_weather(searchcity))
    try:
        city = data["city"]["name"]
    except KeyError:
        return render_template("sc_invalid_city.html", user_input = searchcity)
    country = data["city"]["country"]
    forecast_list = []

    for d in data.get("list"):
        day = time.strftime('%d %B', time.localtime(d.get("dt")))
        mini = d.get("temp").get("min")
        maxi = d.get("temp").get("max")
        description = d.get("weather")[0].get("description")
        forecast_list.append((day, mini, maxi, description))

    return render_template("secure.html", city=city, country=country,
        forecast_list=forecast_list)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
