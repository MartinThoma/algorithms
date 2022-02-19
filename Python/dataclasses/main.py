from impl_named_tuple_class import pos1, pos2, pos3, Position

import sys
from types import ModuleType, FunctionType
from gc import get_referents

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType


def getsize(obj):
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError("getsize() does not take argument of type: " + str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size


print(f"size = {getsize(pos1)}")
print(f"{pos1 == pos2} (expected False)")
print(f"{pos1 == pos3} (expected True)")

print(str(pos1))
print(repr(pos1))
# print(pos1.__hash__())
# print({pos1, pos2, pos3})

Position(1234, 567)
try:
    Position(1234, 567)
except Exception as exc:
    print(exc)
