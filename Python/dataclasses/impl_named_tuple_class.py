from typing import NamedTuple


class Position(NamedTuple):
    longitude: int
    latitude: int
    address: int


pos1 = Position(49.0127913, 8.4231381, "Parkstraße 17")
pos2 = Position(42.1238762, 9.1649964, None)
pos3 = Position(49.0127913, 8.4231381, "Parkstraße 17")


def get_distance(p1: Position, p2: Position) -> float:
    pass


print(pos1)
# Position(longitude=49.0127913, latitude=8.4231381,
#          address='Parkstraße 17')
