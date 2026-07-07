"""雨量値・値の由来区分を表す値オブジェクトを定義する。"""

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True, order=True)
class RainValue:
    """雨量(mm/h)を表す。"""

    millimeters_per_hour: float

    def __post_init__(self) -> None:
        if self.millimeters_per_hour < 0:
            raise ValueError("millimeters_per_hour は0以上であること")


class Provenance(StrEnum):
    """雨量値の由来区分。"""

    OBSERVED = "observed"
    ANALYZED = "analyzed"


@dataclass(frozen=True, slots=True)
class CellRainValue:
    """1セルに割り当てる最終的な雨量値(値 + 由来区分)。"""

    rain_value: RainValue
    provenance: Provenance
