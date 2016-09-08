#!/usr/bin/env python

from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class SignupForm(Form):
    first_name = StringField("First name",
                             validators=[
                                 DataRequired("Please enter your first name.")
                                 ])
    last_name = StringField("Last name",
                            validators=[
                                DataRequired("Please enter your last name.")
                                ])
    email = StringField("Email",
                        validators=[
                            DataRequired("Please enter your email.")
                            ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired("Please enter a password.")
                                 ])
    submit = SubmitField("Sign Up")
