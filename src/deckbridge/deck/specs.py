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
        *,
        y: str = None,
        series: list[dict] = None,
        value_axis_range: tuple[float] = None,
        value_axis_tick_format: str = None,
        data_format: str = "wide",
        series_field: str = None,
        show_data_labels: bool = False,
    ):
        self.chart_type = chart_type
        self.x = x

        if data_format == "wide":
            self.data = data

            if not (y or series):
                raise ValueError("Either y or series must be defined.")

            # -----------------------
            # Normalize series
            # -----------------------
            if series:
                self.series = series
            elif isinstance(y, list):
                self.series = [{"column": col, "name": col} for col in y]
            else:
                self.series = [{"column": y, "name": y}]
        elif data_format == "long":
            if not y:
                raise ValueError("y must be specified for long data format.")
            if not series_field:
                raise ValueError("series_field must be specified for long data format.")
            self.data = self._normalize_to_wide(data, x, y, series_field)
            # -----------------------
            # Normalize series
            # -----------------------
            if series:
                self.series = series
            else:
                columns = [c for c in self.data.columns if c != x]
                self.series = [{"column": col, "name": col} for col in columns]

        self.value_axis_range = value_axis_range
        self.value_axis_tick_format = value_axis_tick_format
        self.show_data_labels = show_data_labels

    def _normalize_to_wide(self, data, x, y, series_field):
        # preserve category axis data order
        categories = data[x].unique()
        data[x] = pd.Categorical(data[x], categories=categories, ordered=True)

        df = data.pivot(
            index=x,
            columns=series_field,
            values=y,
        ).reset_index()

        # handle NaN
        df = df.where(pd.notnull(df), None)

        return df
