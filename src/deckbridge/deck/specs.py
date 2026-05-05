from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass
class LayoutSpec:
    name: str
    slots: Dict[str, dict]


@dataclass
class ChartSpec:
    def __init__(
        self,
        chart_type: str,
        data: pd.DataFrame,
        x: str,
        y: str,
        *,
        series: list[dict] = None,
        value_axis_range: tuple[float] = None,
        value_axis_tick_format: str = None,
    ):
        self.chart_type = chart_type
        self.data = data
        self.x = x

        # -----------------------
        # Normalize series
        # -----------------------
        if series:
            self.series = series

        elif isinstance(y, list):
            self.series = [{"column": col, "name": col} for col in y]

        else:
            self.series = [{"column": y, "name": y}]

        self.value_axis_range = value_axis_range
        self.value_axis_tick_format = value_axis_tick_format
