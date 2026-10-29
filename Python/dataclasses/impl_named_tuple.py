from collections import namedtuple

Position = namedtuple("Position", "longitude latitude address")
pos1 = Position(8.4044193, 49.0139741, "Schloßbezirk 10")
pos2 = Position(9.1649964, 42.1238762, None)


def get_distance(p1: Position, p2: Position) -> float:
    pass


print(pos1)
# Position(longitude=8.4044193, latitude=49.0139741,
#          address='Schloßbezirk 10')
