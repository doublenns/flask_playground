#!/usr/bin/env python

import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from models import db
from models import User
from forms import SignupForm
from forms import LoginForm

app = Flask(__name__)


def get_psql_pw():
    '''
    Function reads PSQL user password from user's home dir.
    '''
    homedir = os.path.expanduser("~")
    psql_pw_file = "/access_tokens/map_app_postgresql/map_app.password"
    with open(homedir + psql_pw_file, "r") as f:
        psql_pw = f.read().strip()
    return psql_pw


psql_user = "map_app"
psql_pw = get_psql_pw()
psql_port = 5432
psql_db = "map_app"

psql_db_uri = "postgresql://{}:{}@localhost:{}/{}"
psql_db_uri = psql_db_uri.format(psql_user, psql_pw, psql_port, psql_db)


# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/map_app"
# Instead of above, using username/password in the URL
app.config['SQLALCHEMY_DATABASE_URI'] = psql_db_uri
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
db.init_app(app)

app.secret_key = "development-key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == "POST":
        if form.validate() is False:
            return render_template("signup.html", form=form)
        else:
            new_user = User(form.first_name.data, form.last_name.data,
                            form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()

            session["email"] = new_user.email
            return redirect(url_for("home"))

    elif request.method == "GET":
        return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" in session:
        return redirect(url_for("home"))

    form = LoginForm()

    if request.method == "POST":
        if form.validate() is FALSE:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session["email"] = form.email.data
                return redirect(url_for("home"))
            else:
                return redirect(url_for("login"))

    elif request.method == "GET":
        return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    if "email" in session:
        return redirect(url_for("home"))

    session.pop("email", None)
    return redirect(url_for("index"))


@app.route("/home")
def home():
    if "email" not in session:
        return redirect(url_for("login.html"))

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)

