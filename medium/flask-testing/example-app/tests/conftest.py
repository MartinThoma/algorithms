# Core Library modules
import os
import tempfile

# Third party modules
import pytest

# First party modules
from mini_app.app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.testing = True
    app.before_request_funcs[None] = []

    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])
