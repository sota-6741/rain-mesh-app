"""観測値・解析値からセルの雨量値を確定するドメインサービスを定義する。"""

from domain.rain.value_object.value import CellRainValue, Provenance, RainValue


class RainValueResolver:
    """観測値があれば最大値を、なければ解析値を採用してセルの雨量値を確定する。"""

    def resolve(
        self,
        observed_values: tuple[RainValue, ...],
        analyzed_value: RainValue | None,
    ) -> CellRainValue:
        """observed_values があれば最大値+実測、なければ analyzed_value+解析を返す。"""

        if observed_values:
            return CellRainValue(
                rain_value=max(observed_values), provenance=Provenance.OBSERVED
            )
        if analyzed_value is None:
            raise ValueError("observed_values が空の場合 analyzed_value が必須")
        return CellRainValue(rain_value=analyzed_value, provenance=Provenance.ANALYZED)
