import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_square(client):
    rv = client.get("/square?number=8")
    assert b"64" == rv.data
