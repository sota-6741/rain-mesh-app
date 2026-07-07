"""XYZ タイル準拠の固定グリッドを表す値オブジェクトを定義する。"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, floor, log, pi, tan

from domain.geo.value_object.coordinate import Coordinate
from domain.rain.value_object.value import CellRainValue


@dataclass(frozen=True, slots=True)
class TileId:
    """固定グリッドの1セルを表す XYZ タイル座標。"""

    zoom_level: int
    x_index: int
    y_index: int

    def __post_init__(self) -> None:
        if self.zoom_level < 0:
            raise ValueError("zoom_level は 0 以上であること")
        tile_count = 2**self.zoom_level
        if not 0 <= self.x_index < tile_count:
            raise ValueError(f"x_index は [0, {tile_count}) であること")
        if not 0 <= self.y_index < tile_count:
            raise ValueError(f"y_index は [0, {tile_count}) であること")

    @staticmethod
    def from_coordinate(coordinate: Coordinate, zoom_level: int) -> TileId:
        """座標を含む XYZ タイルを返す。"""

        tile_count = 2**zoom_level
        x_index = floor((coordinate.longitude + 180.0) / 360.0 * tile_count)
        latitude_radian = coordinate.latitude * pi / 180.0
        mercator_projection = log(
            tan(latitude_radian) + 1.0 / cos(latitude_radian))
        y_index = floor((1.0 - mercator_projection / pi) / 2.0 * tile_count)

        return TileId(zoom_level=zoom_level, x_index=x_index, y_index=y_index)


@dataclass(frozen=True, slots=True)
class MeshGrid:
    """表示領域を覆う固定グリッド(同一ズームレベルのタイル集合)。"""

    zoom_level: int
    tiles: tuple[TileId, ...]

    def __post_init__(self) -> None:
        if not self.tiles:
            raise ValueError("tiles は空でないこと")
        if any(tile.zoom_level != self.zoom_level for tile in self.tiles):
            raise ValueError("全タイルの zoom_level が一致すること")


@dataclass(frozen=True, slots=True)
class MeshCell:
    """雨量値が確定した1セル(タイル + 雨量値)。"""

    tile: TileId
    rain_value: CellRainValue
