# Core Library modules
import json
from typing import List

# Third party modules
import pydantic.json
from pydantic import BaseModel, parse_obj_as


class User(BaseModel):
    name: str
    age: int


# Deserialize a JSON string
users_str = '[{"name": "user1", "age": 15}, {"name": "user2", "age": 28}]'
users = parse_obj_as(List[User], json.loads(users_str))

# Proof it!
print(users)

# Serialize
print(json.dumps([user.dict() for user in users]))
