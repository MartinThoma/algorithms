from typing import Optional, overload


@overload
def foo(a: bool) -> bool:
    ...


@overload
def foo(a: None) -> None:
    ...


def foo(a: Optional[bool]) -> Optional[bool]:
    if a is None:
        return a
    else:
        return not a
