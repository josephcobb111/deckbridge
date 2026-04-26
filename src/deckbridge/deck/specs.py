from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass
class ChartSpec:
    chart_type: str
    data: pd.DataFrame
    x: str
    y: str
    title: str = ""


@dataclass
class LayoutSpec:
    name: str
    slots: Dict[str, dict]
