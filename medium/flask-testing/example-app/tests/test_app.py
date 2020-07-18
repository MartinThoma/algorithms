# Third party modules
import pytest

# First party modules
from mini_app.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_square(client) -> None:
    rv = client.get("/square?number=8")
    assert b"64" == rv.data
