from pathlib import Path
from typing import List, Mapping

import numpy as np
from model import Person, PersonId
from pydantic import parse_file_as


def main(filepath: Path):
    people = get_people(filepath)
    friends_difference = get_account_difference(people)
    for person_id, diff in friends_difference.items():
        print(f"{person_id}: {diff:0.2f} EUR")


def get_account_difference(
    people: Mapping[PersonId, Person]
) -> Mapping[PersonId, float]:
    result = {}
    for person in people.values():
        if person.friends is not None:
            median = np.median(
                [people[friend].bank_account for friend in person.friends]
            )
            result[person.id] = person.bank_account - median
        else:
            result[person.id] = 0
    return result


def get_people(filepath: Path) -> Mapping[PersonId, Person]:
    people = parse_file_as(List[Person], filepath)
    return {person.id: person for person in people}


if __name__ == "__main__":
    main(Path("people.json"))
