"""近傍観測所判定のドメインロジックを定義する。"""

from domain.geo.value_object.coordinate import Coordinate
from domain.mesh.value_object.grid import TileId
from domain.station.value_object.station import Station


class NearestStationPolicy:
    """座標が属する XYZ タイル内の観測所を判定する。"""

    def find_in_tile(
        self,
        coordinate: Coordinate,
        zoom_level: int,
        stations: tuple[Station, ...],
    ) -> tuple[Station, ...]:
        """coordinate と同じタイルに属する観測所を返す。"""

        target_tile = TileId.from_coordinate(coordinate, zoom_level)
        return tuple(
            station
            for station in stations
            if TileId.from_coordinate(station.coordinate, zoom_level) == target_tile
        )
