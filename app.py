from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import json

app = Flask(__name__)

with open("config.json", "r") as c:
    params = json.load(c)["params"]

app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(80), nullable=False)
    upass = db.Column(db.String(80), nullable=False)


@app.route("/", methods=["GET", "POST"])
def login_user():
    if "user" in session and session["user"] == params["user_name"]:
        return render_template("home.html", params=params)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == params["user_name"] and password == params["user_pass"]:
            session["user"] = username
            return render_template("home.html", params=params)
    else:
        return render_template("login.html")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)
