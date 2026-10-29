from typing import Optional
from dataclasses import dataclass


@dataclass
class Position:
    longitude: float
    latitude: float
    address: Optional[str] = None

    @property
    def latitude(self) -> float:
        """Getter for latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: float) -> None:
        """Setter for latitude."""
        if not (-90 <= latitude <= 90):
            raise ValueError(f"latitude was {latitude}, but has to be in [-90, 90]")
        self._latitude = latitude

    @property
    def longitude(self) -> float:
        """Getter for longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: float) -> None:
        """Setter for longitude."""
        if not (-180 <= longitude <= 180):
            raise ValueError(f"longitude was {longitude}, but has to be in [-180, 180]")
        self._longitude = longitude


pos1 = Position(8.4044193, 49.0139741, "Schloßbezirk 10")
pos2 = Position(9.1649964, 42.1238762, None)
pos3 = Position(8.4044193, 49.0139741, "Schloßbezirk 10")


def get_distance(p1: Position, p2: Position) -> float:
    pass


print(pos1)
# Position(longitude=8.4044193, latitude=49.0139741,
#          address='Schloßbezirk 10')
