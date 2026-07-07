import pytest

from domain.geo.value_object.coordinate import Coordinate
from domain.station.value_object.station import Station


def test_station_を生成できる() -> None:
    station = Station(
        station_id="44132", name="東京", coordinate=Coordinate(35.6895, 139.6917)
    )

    assert station.station_id == "44132"
    assert station.name == "東京"


@pytest.mark.parametrize(
    "station_id, name",
    [("", "東京"), ("44132", "")],
)
def test_station_id_または_name_が空文字なら生成に失敗する(
    station_id: str, name: str
) -> None:
    with pytest.raises(ValueError):
        Station(station_id=station_id, name=name, coordinate=Coordinate(35.0, 139.0))
