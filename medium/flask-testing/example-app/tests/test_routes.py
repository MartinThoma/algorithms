import pytest


@pytest.mark.parametrize("route", ["/square?number=8", "/author/1", "/"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200
