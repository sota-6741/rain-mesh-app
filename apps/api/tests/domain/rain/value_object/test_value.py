import pytest

from domain.rain.value_object.value import CellRainValue, Provenance, RainValue


def test_rain_value_を生成できる() -> None:
    assert RainValue(0.0).millimeters_per_hour == 0.0


def test_rain_value_は負値だと生成に失敗する() -> None:
    with pytest.raises(ValueError):
        RainValue(-0.1)


def test_rain_value_は大小比較できる() -> None:
    assert RainValue(3.0) > RainValue(1.0)
    assert max(RainValue(1.0), RainValue(5.0), RainValue(2.0)) == RainValue(5.0)


def test_cell_rain_value_を生成できる() -> None:
    cell_rain_value = CellRainValue(
        rain_value=RainValue(1.0), provenance=Provenance.OBSERVED
    )

    assert cell_rain_value.rain_value == RainValue(1.0)
    assert cell_rain_value.provenance == Provenance.OBSERVED
