import pytest
from hypothesis import given
from hypothesis.strategies import from_type
from model import Person
from pydantic import ValidationError
from pydantic_example import get_account_difference


@given(from_type(Person), from_type(Person))
def test_two_people(person_a: Person, person_b: Person):
    if person_a.id == person_b.id:
        person_a.friends = (person_b.id,)
        assert len(person_a.friends) == 0
    else:
        person_a.friends = (person_b.id,)
        person_b.friends = (person_a.id,)
        diff = get_account_difference(
            people={person_a.id: person_a, person_b.id: person_b}
        )
        assert diff[person_a.id] == diff[person_b.id]
        assert len(diff) == 2
