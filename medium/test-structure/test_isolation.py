import pytest


@pytest.fixture
def show_isolation():
    a = 42
    yield a
    a += 1


def test_foo(show_isolation):
    assert show_isolation == 42


def test_bar(show_isolation):
    assert show_isolation == 42
