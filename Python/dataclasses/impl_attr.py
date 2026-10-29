from typing import Optional
import attr


@attr.s
class Position:
    longitude: float = attr.ib()
    latitude: float = attr.ib()
    address: Optional[str] = attr.ib(default=None)

    @longitude.validator
    def check_long(self, attribute, v):
        if not (-180 <= v <= 180):
            raise ValueError(f"Longitude was {v}, but must be in [-180, +180]")

    @latitude.validator
    def check_lat(self, attribute, v):
        if not (-90 <= v <= 90):
            raise ValueError(f"Latitude was {v}, but must be in [-90, +90]")


pos1 = Position(8.4044193, 49.0139741, "Schloßbezirk 10")
pos2 = Position(9.1649964, 42.1238762)
pos3 = Position(8.4044193, 49.0139741, "Schloßbezirk 10")


def get_distance(p1: Position, p2: Position) -> float:
    pass


print(pos1)
# Position(longitude=8.4044193, latitude=49.0139741, address='Schloßbezirk 10')
