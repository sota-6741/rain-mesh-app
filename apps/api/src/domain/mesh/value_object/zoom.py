"""ズームレベルの値オブジェクトを定義する。"""

from dataclasses import dataclass

# 下限2km相当。緯度35°付近で1タイル≒2km となるタイルズームを上限とする。
_MAX_TILE_ZOOM = 14


@dataclass(frozen=True, slots=True)
class ZoomLevel:
    """クライアント地図の表示ズームレベルを表す。"""

    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("zoom_level は 0 以上の整数であること")

    @property
    def tile_zoom(self) -> int:
        """グリッド生成とキャッシュに使う XYZ タイルズームを返す。下限2km相当で頭打ちにする。"""

        return min(self.value, _MAX_TILE_ZOOM)
