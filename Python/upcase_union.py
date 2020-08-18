from typing import Union


def upcase(s: Union[str, bytes]) -> Union[str, bytes]:
    if isinstance(s, str):
        return s.upper()
    elif isinstance(s, bytes):
        return bytes(x - 0x20 if 0x61 <= x <= 0x7A else x for x in s)
    else:
        raise TypeError("need str or bytes")
