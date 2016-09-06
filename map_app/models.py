#!/usr/bin/env python

from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120)), unique=True)
    pwdhash = db.Column(db.String(54))


    def __init__(Self, firstname, lastname, email, password):
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
