from typing import Optional

from hypothesis import given
from hypothesis.strategies import from_type
from pydantic import BaseModel


class Adress(BaseModel):
    city: str
    street: str
    house_number: int
    postal_code: int


class Person(BaseModel):
    prename: str
    middlename: Optional[str]
    lastname: str
    address: Adress


@given(from_type(Person))
def test_me(person: Person):
    seen = [
        Person(
            prename="",
            middlename=None,
            lastname="",
            address=Adress(city="", street="", house_number=0, postal_code=0),
        ),
        Person(
            prename="0",
            middlename=None,
            lastname="",
            address=Adress(city="", street="", house_number=0, postal_code=0),
        ),
        Person(
            prename="",
            middlename=None,
            lastname="0",
            address=Adress(city="", street="", house_number=0, postal_code=0),
        ),
        Person(
            prename="",
            middlename=None,
            lastname="",
            address=Adress(city="", street="0", house_number=0, postal_code=0),
        ),
    ]
    # assert person in seen
    assert isinstance(person, Person)
