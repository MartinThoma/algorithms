from typing import Optional
from pydantic import validator, BaseModel
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    longitude: float
    latitude: float
    address: Optional[str] = None

    @validator("longitude")
    def longitude_value_range(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError(f"Longitude was {v}, but must be in [-180, +180]")
        return v

    @validator("latitude")
    def latitude_value_range(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError(f"Latitude was {v}, but must be in [-90, +90]")
        return v


# class Position(BaseModel):
#     longitude: float
#     latitude: float
#     address: Optional[str] = None


pos1 = Position(longitude=49.0127913, latitude=8.4231381, address="Parkstraße 17")
pos2 = Position(longitude=42.1238762, latitude=9.1649964)
pos3 = Position(longitude=49.0127913, latitude=8.4231381, address="Parkstraße 17")


def get_distance(p1: Position, p2: Position) -> float:
    pass
