from __future__ import annotations

import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name = "Jane Doe"
    friends: List[str] = Field(default_factory=list)
    bank_account: Decimal = Decimal(0.0)
    class Config:
        extra='allow'


jane = User(id=1, birthdate=datetime.datetime(1990, 4, 28, 23, 59, 59))

with open("jane.json", "w") as fp:
    fp.write(jane.json(indent=4, sort_keys=True))

with open("john.json") as fp:
    john = User.parse_raw(fp.read())

print(john.dict())
