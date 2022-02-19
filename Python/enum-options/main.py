from builtin_enum import HttpStatus as HttpStatusBuiltin
from enum_class import HttpStatus as HttpStatusClass
from django_choices import HttpStatus as DjangoHttpStatus
import enum_module
from typing import NoReturn, Literal


def assert_never(value: NoReturn) -> NoReturn:
    assert False, f"Unhandled value: {value} ({type(value).__name__})"


def main(enums):
    for enum_name, enum in enums:
        print(f"\n\n## {enum_name} ############################################")
        print(f"\t{enum}")
        print(f"\t{enum.NOT_FOUND}")
        print("Iteration:")
        try:
            for item in enum:
                print(f"\t{item}")
        except Exception:
            print("\tnot possible")
        print("Comparison:")
        print(f"\tenum.NOT_FOUND == 404: {enum.NOT_FOUND == 404}")
        try:
            print(f"\tenum.NOT_FOUND.value == 404: {enum.NOT_FOUND.value == 404}")
        except Exception:
            pass


def print_status(status: HttpStatusBuiltin) -> None:
    if status is HttpStatusBuiltin.SUCCESS:
        print("SUCCESS")
    elif status is HttpStatusBuiltin.NOT_FOUND:
        print("NOT_FOUND")
    else:
        assert_never(status)


def handle_status_class(status: HttpStatusClass) -> None:
    if status is HttpStatusClass.SUCCESS:
        print("ship order")

    elif status is HttpStatusClass.NOT_FOUND:
        print("charge order")
    else:
        assert_never(status)


def handle_status_django(status: DjangoHttpStatus) -> None:
    if status is DjangoHttpStatus.SUCCESS:
        print("ship order")

    elif status is DjangoHttpStatus.NOT_FOUND:
        print("charge order")
    else:
        assert_never(status)


def handle_status_literal(status: Literal["a", "b", "c"]) -> None:
    if status == "a":
        print("ship order")
    elif status == "b":
        print("charge order")
    else:
        assert_never(status)


main(
    [
        ("Built-in Enum", HttpStatusBuiltin),
        ("Basic Class", HttpStatusClass),
        ("Enum Module", enum_module),
        ("Django Choices", DjangoHttpStatus),
    ]
)
