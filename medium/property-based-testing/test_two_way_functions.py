from base64 import b64decode, b64encode

from hypothesis import given
from hypothesis import strategies as s


@given(s.binary())
def test_base64_encode_decode_together(data):
    assert b64decode(b64encode(data)) == data
