from .base_filter import BaseFilter
from entities import FilterConfig, FilterType, TradeAlgorithm


class BollingerBendsFilter(BaseFilter):
    _FILTER_TYPE = FilterType.BOLLINGER_BENDS
    _DEF_PERIODS = 20

    def __init__(self, config: FilterConfig, trade_algorithm: TradeAlgorithm):
        super().__init__(config, trade_algorithm)
        self._periods = config.periods or self._DEF_PERIODS

    @property
    def periods(self):
        return self._periods
