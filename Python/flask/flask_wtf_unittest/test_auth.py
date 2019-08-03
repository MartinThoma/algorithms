#!/usr/bin/env python

# core modules
import logging

# 3rd party modules
import pytest

# internal modules
import app

logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    """Start with a blank database."""
    app_obj = app.app
    client = app_obj.test_client()
    yield client


def test_login_succeeds(client):
    resp = login(client, "foo@example.com", "bar")
    assert "Invalid" not in resp.data.decode("utf-8")


def test_login_fails(client):
    resp = login(client, "foo@example.com", "wrong")
    assert "Invalid" in resp.data.decode("utf-8")


def login(client, email, password):
    return client.post(
        "/login",
        data=dict(submit="Log In", email=email, password=password, csrf_token="foo"),
        follow_redirects=True,
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
