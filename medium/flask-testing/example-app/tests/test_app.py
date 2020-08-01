def test_square(client) -> None:
    rv = client.get("/square?number=8")
    assert rv.data == b"64"


def test_author(client) -> None:
    rv = client.get("/author/1")
    assert rv.status_code == 200
    assert rv.json == {"id": 1, "first_name": "foo", "last_name": "bar"}


def test_main_route_status_code(client, captured_templates) -> None:
    route = "/"
    rv = client.get(route)
    assert rv.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "base.html"
    assert context["number"] == 0
    assert context["square"] == 0


def test_main_route_status_code_number3(client, captured_templates) -> None:
    route = "/?number=3"
    rv = client.get(route)
    assert rv.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "base.html"
    assert context["number"] == 3
    assert context["square"] == 9
