# Third party modules
import pytest

# First party modules
from mini_app.app import create_app, db
from mini_app.models import Author


@pytest.fixture
def client():
    app = create_app()

    app.config["TESTING"] = True
    app.testing = True

    # This creates an in-memory sqlite db
    # See https://martin-thoma.com/sql-connection-strings/
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db.create_all()
        author1 = Author(id=1, first_name="foo", last_name="bar")
        db.session.add(author1)
        db.session.commit()
    yield client
