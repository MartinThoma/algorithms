# Core Library modules
import logging

# Third party modules
import pytest
from flask import template_rendered
# First party modules
from mini_app.app import create_app, db
from mini_app.models import Author


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app()
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    _app.config["TESTING"] = True
    _app.testing = True

    # This creates an in-memory sqlite db
    # See https://martin-thoma.com/sql-connection-strings/
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        db.create_all()
        author1 = Author(id=1, first_name="foo", last_name="bar")
        db.session.add(author1)
        db.session.commit()

    yield _app
    ctx.pop()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
