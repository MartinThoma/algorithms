from example import foo


def test_foo():
    assert foo(a=None) is None
    assert foo(False) is True
    assert foo(True) is False
