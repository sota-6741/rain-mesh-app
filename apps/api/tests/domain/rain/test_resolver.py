import pytest

from domain.rain.resolver import RainValueResolver
from domain.rain.value_object.value import Provenance, RainValue


def test_観測値があれば最大値を実測として返す() -> None:
    resolver = RainValueResolver()

    resolved = resolver.resolve(
        observed_values=(RainValue(1.0), RainValue(5.0), RainValue(3.0)),
        analyzed_value=RainValue(10.0),
    )

    assert resolved.rain_value == RainValue(5.0)
    assert resolved.provenance == Provenance.OBSERVED


def test_観測値がなければ解析値を採用する() -> None:
    resolver = RainValueResolver()

    resolved = resolver.resolve(observed_values=(), analyzed_value=RainValue(2.0))

    assert resolved.rain_value == RainValue(2.0)
    assert resolved.provenance == Provenance.ANALYZED


def test_観測値も解析値もなければ例外を送出する() -> None:
    resolver = RainValueResolver()

    with pytest.raises(ValueError):
        resolver.resolve(observed_values=(), analyzed_value=None)
