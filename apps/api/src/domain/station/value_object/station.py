"""アメダス観測所の参照データを表す値オブジェクトを定義する。"""

from dataclasses import dataclass

from domain.geo.value_object.coordinate import Coordinate


@dataclass(frozen=True, slots=True)
class Station:
    """アメダス観測所(読み取り専用の参照データ)。"""

    station_id: str
    name: str
    coordinate: Coordinate

    def __post_init__(self) -> None:
        if not self.station_id:
            raise ValueError("station_id は空でないこと")
        if not self.name:
            raise ValueError("name は空でないこと")
