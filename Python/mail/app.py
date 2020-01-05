from flask import Flask
from flask_mail import Mail, Message

mail = Mail()

app = Flask(__name__)
mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "your_user@gmail.com",
    "MAIL_PASSWORD": "your_pw",
}

app.config.update(mail_settings)
mail.init_app(app)


@app.route("/")
def index():
    msg = Message(
        "Flask mail test", sender="from@example.com", recipients=["to@example.com"]
    )
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    status = mail.send(msg)
    return str(status)


if __name__ == "__main__":
    app.run()
