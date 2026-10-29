from typing import Optional
from pydantic import field_validator, BaseModel
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    longitude: float
    latitude: float
    address: Optional[str] = None

    @field_validator("longitude")
    @classmethod
    def longitude_value_range(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError(f"Longitude was {v}, but must be in [-180, +180]")
        return v

    @field_validator("latitude")
    @classmethod
    def latitude_value_range(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError(f"Latitude was {v}, but must be in [-90, +90]")
        return v


# class Position(BaseModel):
#     longitude: float
#     latitude: float
#     address: Optional[str] = None


pos1 = Position(longitude=8.4044193, latitude=49.0139741, address="Schloßbezirk 10")
pos2 = Position(longitude=9.1649964, latitude=42.1238762)
pos3 = Position(longitude=8.4044193, latitude=49.0139741, address="Schloßbezirk 10")


def get_distance(p1: Position, p2: Position) -> float:
    pass
