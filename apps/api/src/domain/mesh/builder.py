"""固定グリッドを組み立てるドメインサービスを定義する。"""

from domain.geo.value_object.bounding_box import BoundingBox
from domain.mesh.value_object.grid import MeshGrid, TileId
from domain.mesh.value_object.zoom import ZoomLevel


class MeshBuilder:
    """表示領域とズームレベルから固定グリッドを組み立てる。"""

    def build(self, bounding_box: BoundingBox, zoom_level: ZoomLevel) -> MeshGrid:
        """表示領域を覆う XYZ タイル集合を固定グリッドとして返す。"""

        tile_zoom = zoom_level.tile_zoom
        southwest_tile = TileId.from_coordinate(bounding_box.southwest, tile_zoom)
        northeast_tile = TileId.from_coordinate(bounding_box.northeast, tile_zoom)

        min_x_index, max_x_index = sorted(
            (southwest_tile.x_index, northeast_tile.x_index)
        )
        min_y_index, max_y_index = sorted(
            (southwest_tile.y_index, northeast_tile.y_index)
        )

        tiles = tuple(
            TileId(zoom_level=tile_zoom, x_index=x_index, y_index=y_index)
            for x_index in range(min_x_index, max_x_index + 1)
            for y_index in range(min_y_index, max_y_index + 1)
        )
        return MeshGrid(zoom_level=tile_zoom, tiles=tiles)
