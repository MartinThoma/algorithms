import time

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    time.sleep(1)
    return "hello world!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
