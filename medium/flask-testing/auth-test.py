# Core Library modules
from base64 import b64encode


def test_protected_route(client):
    credentials = b64encode(b"user:password").decode("utf-8")
    route = "protected/route"
    rv = client.get(route, headers={"Authorization": "Basic " + credentials})
    assert rv.status_code == 200
