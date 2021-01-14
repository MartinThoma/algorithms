import json
from pathlib import Path
from typing import Any, Mapping

import numpy as np


def main(filepath: Path):
    people = get_people(filepath)
    friends_difference = get_account_difference(people)
    for person_id, diff in friends_difference.items():
        print(f"{person_id}: {diff:0.2f} EUR")


def get_account_difference(
    people: Mapping[str, Mapping[str, Any]]
) -> Mapping[int, float]:
    result = {}
    for person in people.values():
        if person["friends"] is not None:
            friends_account = [
                people[friend]["bank_account"] for friend in person["friends"]
            ]
            median = np.median(friends_account)
        else:
            median = None

        if median is None:
            result[person["id"]] = 0
        else:
            result[person["id"]] = person["bank_account"] - median
    return result


def get_people(filepath: Path) -> Mapping[str, Mapping[str, Any]]:
    with open(filepath) as fp:
        people = json.loads(fp.read())
    id2person = {}
    for person in people:
        id2person[person["id"]] = person
    return id2person


if __name__ == "__main__":
    main(Path("people.json"))
