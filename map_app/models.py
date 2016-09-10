#!/usr/bin/env python

from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import geocoder
import urllib2
import json


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        # What happens if the user's name has multiple capital letters?
        # i.e. "LaShonda McDowell"
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


# p = Place()
# places = p.query("1600 Amphitheatre Parkway Mountain View CA")
class Place(object):
    def meters_to_walking_time(self, meters):
        # 80 meters is one minute walking time
        return int(meters / 80)

    def address_to_latlng(self, address):
        g = geocoder.google(address)
        return (g.lat, g.lng)

    def query(self, address):
        lat, lng = self.address_to_latlng(address)
        print lat, lng

        query_url = ("https://en.wikipedia.org/w/api.php?action=query&list=" +
                    "geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&" +
                    "format=json").format(lat, lng)
        g = urllib2.urlopen(query_url)
        results = g.read()
        g.close()

        data = jsno.loads(results)
        print data

        places = []
        for place in data["query"]["geosearch"]:
            name = place["title"]
            meters = place["dist"]
            lat = place["lat"]
            lng = place["lon"]
            wiki_url = self.wiki_path(name)
            walkingtime = self.meters_to_walking_time(meters)

            d = {
                "name": name,
                "url": wiki_url,
                "time": walking_time,
                "lat": lat,
                "lng": lng
            }

            places.append(d)

        return places
