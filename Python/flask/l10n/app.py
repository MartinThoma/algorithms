#!/usr/bin/env python

# core modules
import datetime

import flask_babel
# 3rd party modules
from flask import Flask, flash, render_template
from flask_babel import Babel, _


def format_datetime(value, format="medium"):
    import flask_babel

    if format == "full":
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == "medium":
        format = "EE dd.MM.y HH:mm"
    elif format == "date":
        format = "dd.MM.y"
    elif format == "isoformat":
        return value.isoformat()
    return flask_babel.dates.format_datetime(value, format)


app = Flask(__name__)
app.config["SECRET_KEY"] = "foo"
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "./translations"
app.jinja_env.filters["datetime"] = format_datetime
babel = Babel(app)


@app.route("/")
def index():
    print(_("Hello World!"))
    flash(_("Hello World!"))
    pubdate = datetime.datetime.now()
    return render_template(
        "main.html",
        pubdate=pubdate,
        author="John Smith",
        date_localized=flask_babel.dates.format_date(pubdate),
    )


@babel.localeselector
def get_locale():
    print("foo")
    return "de"  # request.accept_languages.best_match(app.config["LANGUAGES"])


if __name__ == "__main__":
    app.run(port=5000)
