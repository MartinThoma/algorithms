import random
from flask import Flask
app = Flask(__name__)
random.seed(0)


@app.route("/")
def hello():
    x = random.randint(1, 100)
    y = random.randint(1, 100)
    return str(x * y)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
