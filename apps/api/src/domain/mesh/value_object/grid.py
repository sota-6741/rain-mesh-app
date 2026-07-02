from dataclasses import dataclass

from domain.geo.value_object.bounding_box import BoundingBox
from domain.mesh.value_object.zoom import CellSize


@dataclass(frozen=True, slots=True)
class Cell:
    """擬似メッシュを構成する1マス(幾何のみ。雨量値は持たない)。

    Attributes:
        row: 格子内の行番号(0 始まり、南西を原点とする)。
        col: 格子内の列番号(0 始まり、南西を原点とする)。
        bounds: このセルが覆う緯度経度の矩形。
    """
    row: int
    col: int
    bounds: BoundingBox


@dataclass(frozen=True, slots=True)
class Grid:
    """表示領域を覆う擬似メッシュ"""
    bounds: BoundingBox
    cell_size: CellSize
