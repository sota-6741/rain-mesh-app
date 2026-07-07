from domain.geo.value_object.coordinate import Coordinate
from domain.station.nearest import NearestStationPolicy
from domain.station.value_object.station import Station

_ZOOM_LEVEL = 10
_TOKYO = Station(
    station_id="44132", name="東京", coordinate=Coordinate(35.6895, 139.6917)
)
_OSAKA = Station(
    station_id="62078", name="大阪", coordinate=Coordinate(34.6937, 135.5023)
)


def test_同一タイルに属する観測所を返す() -> None:
    policy = NearestStationPolicy()
    near_tokyo = Coordinate(35.69, 139.70)

    found = policy.find_in_tile(
        near_tokyo, _ZOOM_LEVEL, (_TOKYO, _OSAKA)
    )

    assert found == (_TOKYO,)


def test_同一タイルに属する観測所が複数あればすべて返す() -> None:
    policy = NearestStationPolicy()
    another_tokyo_station = Station(
        station_id="44133", name="東京(別観測所)", coordinate=Coordinate(35.685, 139.70)
    )

    found = policy.find_in_tile(
        _TOKYO.coordinate, _ZOOM_LEVEL, (_TOKYO, another_tokyo_station, _OSAKA)
    )

    assert found == (_TOKYO, another_tokyo_station)


def test_同一タイルに属する観測所がなければ空を返す() -> None:
    policy = NearestStationPolicy()

    found = policy.find_in_tile(_TOKYO.coordinate, _ZOOM_LEVEL, (_OSAKA,))

    assert found == ()
