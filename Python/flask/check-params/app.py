from functools import wraps

from flask import Flask, jsonify


def validated_content(func):
    @wraps(func)
    def wrapper(**kwargs):
        try:
            content = get_content(kwargs["content_id"])
        except:
            return (
                jsonify(
                    {
                        "status": 404,
                        "error": "not found",
                        "content_id": kwargs["content_id"],
                    }
                ),
                404,
            )
        del kwargs["content_id"]
        kwargs["content"] = content
        return func(**kwargs)

    return wrapper


def get_content(content_id):
    if content_id == "123":
        return "bar"
    raise Exception(f"Could not find content_id={content_id}")


app = Flask("foo")


@app.route("/<string:content_id>")
@validated_content
def index(content):
    return f"content={content}"


app.run()
