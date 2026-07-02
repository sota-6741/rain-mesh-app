"""座標値オブジェクトを定義する。"""

from dataclasses import dataclass

# Web メルカトル図法(EPSG:3857、XYZ タイルの座標系)の緯度上限。
# メルカトルは極で無限大に発散するため、投影 y の範囲を経度と揃えて
# 地図を正方形にする境界で緯度を打ち切る。この境界が下式で導かれる:
#   degrees(atan(sinh(pi))) = 85.0511287798066  (以下はその丸め値)
# これより極側の座標は XYZ タイル計算(log(tan+sec))が破綻するため弾く。
_WEB_MERCATOR_MAX_LATITUDE = 85.05112878
_MIN_LONGITUDE = -180.0
_MAX_LONGITUDE = 180.0


@dataclass(frozen=True, slots=True)
class Coordinate:
    """緯度・経度を表す。"""

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -_WEB_MERCATOR_MAX_LATITUDE <= self.latitude <= _WEB_MERCATOR_MAX_LATITUDE:
            raise ValueError("latitude は Web メルカトルの有効範囲内であること")
        if not _MIN_LONGITUDE <= self.longitude <= _MAX_LONGITUDE:
            raise ValueError("longitude は [-180, 180] であること")
