import logging

from flask import Flask, current_app

app = Flask(__name__)

# Normal Python logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

# Flasks app logger
app.logger.setLevel(logging.DEBUG)


@app.route("/")
def index():
    current_app.logger.info("flask-app logger info-msg")
    logger.info("base-logger infomsg")
    return "foo"


if __name__ == "__main__":
    app.run()
