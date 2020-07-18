def test_square(client) -> None:
    rv = client.get("/square?number=8")
    assert rv.data == b"64"


def test_author(client) -> None:
    rv = client.get("/author/1")
    assert rv.json == {"id": 1, "first_name": "foo", "last_name": "bar"}
