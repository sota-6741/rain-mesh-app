"""気象庁アメダスの観測値取得ポートを定義する。"""

from typing import Protocol

from domain.rain.value_object.value import RainValue
from domain.station.value_object.station import Station


class AmedasObservationProvider(Protocol):
    """気象庁アメダスの最新観測値を一括取得するポート。"""

    def fetch_latest_observations(self) -> tuple[tuple[Station, RainValue], ...]:
        """観測所ごとの最新の実測雨量値を返す。"""
        ...
