from hypothesis import given, strategies as s

from base64 import b64encode, b64decode


@given(s.binary())
def test_base64_encode_decode_together(data):
    assert b64decode(b64encode(data)) == data
