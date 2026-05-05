from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass
class LayoutSpec:
    name: str
    slots: Dict[str, dict]


@dataclass
class ChartSpec:
    def __init__(self, chart_type: str, data: pd.DataFrame, x: str, y: str, *, value_axis_range: tuple[float] = None):
        self.chart_type = chart_type
        self.data = data
        self.x = x
        self.y = y
        self.value_axis_range = value_axis_range
