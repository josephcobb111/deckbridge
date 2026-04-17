from dataclasses import dataclass

import pandas as pd


@dataclass
class ChartSpec:
    chart_type: str
    data: pd.DataFrame
    x: str
    y: str
    title: str = ""
