from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/square")
def square():
    number = int(request.args.get("number", 0))
    return str(number ** 2)


if __name__ == "__main__":
    app.run()
