from domain.mesh.value_object.grid import MeshCell, TileId
from domain.rain.value_object.value import CellRainValue, Provenance, RainValue


def test_mesh_cell_を生成できる() -> None:
    tile = TileId(zoom_level=10, x_index=909, y_index=403)
    rain_value = CellRainValue(rain_value=RainValue(1.5), provenance=Provenance.OBSERVED)

    cell = MeshCell(tile=tile, rain_value=rain_value)

    assert cell.tile == tile
    assert cell.rain_value == rain_value
