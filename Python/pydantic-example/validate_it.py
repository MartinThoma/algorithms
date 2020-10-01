from __future__ import annotations

from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name = "Jane Doe"
    friends: List[str] = Field(default_factory=list)
    bank_account: Decimal = Decimal(0.0)


jane = User(id=1)

with open("jane.json", "w") as fp:
    fp.write(jane.json())

with open("john.json") as fp:
    john = User.parse_raw(fp.read())

print(john.dict())
