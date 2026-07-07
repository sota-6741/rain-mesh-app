"""YOLPの解析雨量値取得ポートを定義する。"""

from typing import Protocol

from domain.mesh.value_object.grid import TileId
from domain.rain.value_object.value import RainValue


class AnalyzedRainValueProvider(Protocol):
    """YOLPでタイル単位の解析雨量値をオンデマンド取得するポート。"""

    def fetch_analyzed_value(self, tile: TileId) -> RainValue:
        """指定タイルの解析雨量値を返す。"""
        ...
