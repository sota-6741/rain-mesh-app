from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Coordinate:
    """緯度・経度を持つ座標"""
    lat: float
    lon: float

    def __post_init__(self) -> None:
        if not -90 <= self.lat <= 90:
            raise ValueError("lat は [-90, 90]")
        if not -180 <= self.lon <= 180:
            raise ValueError("lon は [-180, 180]")
