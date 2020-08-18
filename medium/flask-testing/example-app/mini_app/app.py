# Core Library modules
from typing import Dict, Optional, Union

# Third party modules
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# First party modules
from mini_app import config

db = SQLAlchemy()


def create_app(cfg: Optional[config.Config] = None) -> Flask:
    if cfg is None:
        cfg = config.Config()
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(cfg)

    # Init_apps
    db.init_app(app)

    @app.route("/square")
    def square() -> str:
        """A view which uses no templates and no database."""
        number = int(request.args.get("number", 0))
        return str(number ** 2)

    @app.route("/")
    def templated_square() -> str:
        """A view which uses templates."""
        number = int(request.args.get("number", 0))
        return render_template("base.html", number=number, square=number ** 2)

    @app.route("/author/<int:author_id>")
    def get_author(author_id: int) -> Dict[str, Union[int, str]]:
        """A view which uses the database."""
        from mini_app.models import Author

        return Author.query.get(author_id).dict()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
