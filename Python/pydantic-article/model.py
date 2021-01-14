import datetime
from decimal import Decimal
from typing import List, NewType, Optional

from pydantic import BaseModel, root_validator

PersonId = NewType("PersonId", int)


class Person(BaseModel):
    id: PersonId
    name: str
    bank_account: Decimal
    birthdate: datetime.date
    friends: Optional[List[PersonId]] = None

    class Config:
        extra = "forbid"

    @root_validator
    def cannot_self_friend(cls, values):
        friends = values.get("friends")
        self_id = values.get("id")
        if friends is not None:
            values["friends"] = [
                friend_id for friend_id in friends if friend_id != self_id
            ]
        return values
