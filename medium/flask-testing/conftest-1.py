# Third party modules
import pytest


@pytest.fixture
def client():
    # Prepare before your test
    flaskr.app.config["TESTING"] = True
    with flaskr.app.test_client() as client:
        # Give control to your test
        yield client
    # Cleanup after the test run.
    # ... nothing here, for this simple example
