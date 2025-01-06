from collections import defaultdict

from indicators.indicators_pool import IndicatorsPool
from .deal_filter import DealFilter
from .entities import DealState, DealPhase
from entities import DealConfig, ExitMode, TimeFrame, FilterConfig


class Deal:
    def __init__(
        self,
        config: DealConfig,
        indicators_pool: IndicatorsPool,
        current_state: DealState | None = None,
    ):
        self._config = config
        self._indicators_pool = indicators_pool
        self._algorithm = config.trade_algorithm
        self._state = current_state or DealState()
        self._filters: dict[TimeFrame, list[DealFilter]] = defaultdict(list)

        self._init_state()

    def _init_state(self):
        if self._state.phase == DealPhase.LOOK_FOR_ENTRY_POINT:
            self._inti_look_entry_state()
        else:
            self._init_in_deal_state()

    def _create_filters(self, filters_config: list[FilterConfig]):
        for filter_config in filters_config:
            deal_filter = DealFilter(filter_config, self._indicators_pool)
            self._filters[filter_config.timeframe].append(deal_filter)

    def _inti_look_entry_state(self):
        self._create_filters(self._config.entry_condition.filters)

    def _init_in_deal_state(self):
        if self._config.exit_condition.mode == ExitMode.SIGNAL:
            self._create_filters(self._config.exit_condition.signal.filters)

    @property
    def state(self) -> DealState:
        return self._state

    def get_filters(self, timeframe: TimeFrame) -> list[DealFilter]:
        return self._filters[timeframe]
