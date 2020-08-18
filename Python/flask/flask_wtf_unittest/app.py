#!/usr/bin/env python

# 3rd party modules
from flask import Flask, flash, redirect, render_template, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField

app = Flask(__name__)
app.secret_key = b"secret"
app.config["WTF_CSRF_ENABLED"] = False
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User()


class User(UserMixin):
    id = "foobar"


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("success"))
    form = LoginForm()
    if form.validate_on_submit():
        invalid_email = form.email.data != "foo@example.com"
        invalid_password = form.password.data != "bar"
        if invalid_email or invalid_password:
            flash("Invalid email or password", "error")
            return redirect(url_for("login"))
        user = User()
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("success"))
    else:
        print("Form was not submitted or validated.")
        print("DEGUG: Form errors:")
        print(form.errors)
    return render_template("login.html", form=form), 203


@app.route("/success")
@login_required
def success():
    return "You are logged in!"


if __name__ == "__main__":
    app.run(port=5000)
