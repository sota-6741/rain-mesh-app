"""表示領域の境界値オブジェクトを定義する。"""

from dataclasses import dataclass

from domain.geo.value_object.coordinate import Coordinate


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """雨量メッシュの表示範囲を表す。"""

    southwest: Coordinate
    northeast: Coordinate

    def __post_init__(self) -> None:
        if self.southwest.latitude >= self.northeast.latitude:
            raise ValueError("south < north であること")
        if self.southwest.longitude >= self.northeast.longitude:
            raise ValueError("west < east であること")
