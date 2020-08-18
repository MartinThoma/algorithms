import responses
from requests_example import get_ip


@responses.activate
def test_get_ip():
    responses.add(
        responses.GET,
        "http://ip.jsontest.com/",
        json={"ip": "123.456.789.0"},
        status=404,
    )
    assert get_ip() == {"ip": "123.456.789.0"}
