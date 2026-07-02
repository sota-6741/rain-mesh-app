from __future__ import annotations

from dataclasses import dataclass

_MIN_ZOOM_LEVEL = 0
_MAX_ZOOM_LEVEL = 18
_MIN_CELL_SIZE_KM = 2.0


@dataclass(frozen=True, slots=True)
class CellSize:
    """メッシュのセル一辺の大きさ。ズームレベルごとに固定。"""

    km: float

    def __post_init__(self) -> None:
        if self.km < _MIN_CELL_SIZE_KM:
            raise ValueError(f"km は {_MIN_CELL_SIZE_KM} 以上であること")


_ZOOM_TO_KM: dict[int, float] = {
    0: 256,
    1: 256,
    2: 256,
    3: 256,
    4: 256,
    5: 256,
    6: 128,
    7: 64,
    8: 32,
    9: 16,
    10: 8,
    11: 4,
    12: 2,
    13: 2,
    14: 2,
    15: 2,
    16: 2,
    17: 2,
    18: 2,
}

ZOOM_TO_CELL_SIZE: dict[int, CellSize] = {
    zoom: CellSize(km=km) for zoom, km in _ZOOM_TO_KM.items()
}


@dataclass(frozen=True, slots=True)
class ZoomLevel:
    value: int

    def __post_init__(self) -> None:
        if not (_MIN_ZOOM_LEVEL <= self.value <= _MAX_ZOOM_LEVEL):
            raise ValueError(
                f"zoom_level は {_MIN_ZOOM_LEVEL}..{_MAX_ZOOM_LEVEL} の整数であること"
            )

    @property
    def cell_size(self) -> CellSize:
        return ZOOM_TO_CELL_SIZE[self.value]
