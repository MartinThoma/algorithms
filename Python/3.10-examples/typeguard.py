from typing import TypedDict, TypeGuard


class User(TypedDict):
    name: str
    email: str


def is_user(data: dict) -> TypeGuard[User]:
    return "name" in data and "email" in data


if __name__ == "__main__":
    user = {"name": "Martin", "email": "info@martin-thoma.de"}
    user = {}
    if is_user(user):
        print(user["x"])
