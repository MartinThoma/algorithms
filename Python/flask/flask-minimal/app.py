from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    name = "world"
    return render_template("hello.html", name=name)


@app.route("/user/<username>")
def show_user_profile(username):
    # show the user profile for that user
    return f"User {escape(username)}"


@app.route("/post/<int:post_id>")
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f"Post {post_id}"
