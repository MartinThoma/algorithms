from typing import overload


@overload
def upcase(s: str) -> str:
    ...


@overload
def upcase(s: bytes) -> bytes:
    ...


def upcase(s):
    if isinstance(s, str):
        return s.upper()
    elif isinstance(s, bytes):
        return bytes(x - 0x20 if 0x61 <= x <= 0x7A else x for x in s)
    else:
        raise TypeError("need str or bytes")
