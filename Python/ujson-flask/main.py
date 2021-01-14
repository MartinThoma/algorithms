from uuid import UUID, uuid4

import ujson as json
from flask import Flask, jsonify
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return JSONEncoder.default(self, obj)

    def encode(self, o):
        return json.dumps(o)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder


@app.route("/")
def index():
    return jsonify({"foo": uuid4()})


app.run()
