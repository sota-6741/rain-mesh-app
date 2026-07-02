from dataclasses import dataclass

from domain.geo.value_object.coordinate import Coordinate


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """雨量メッシュを表示する範囲"""
    southwest: Coordinate
    northeast: Coordinate

    def __post_init__(self) -> None:
        if self.southwest.lat >= self.northeast.lat:
            raise ValueError("south < north であること")
        if self.southwest.lon >= self.northeast.lon:
            raise ValueError("west < east であること")
