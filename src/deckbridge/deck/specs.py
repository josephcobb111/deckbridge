"""Data specifications for deckbridge deck layouts and charts.

This module defines dataclasses that represent layout specifications and
chart specifications used throughout the deckbridge rendering pipeline.
"""

from dataclasses import dataclass
from typing import Dict, Optional

import pandas as pd


@dataclass
class LayoutSpec:
    """Specification for a deck layout.

    Attributes:
        name: The unique name identifying the layout.
        slots: A mapping from slot identifiers to configuration dictionaries.
    """

    name: str
    slots: Dict[str, dict]


@dataclass
class ChartSpec:
    """Specification for a chart to be rendered.

    The class normalises input data depending on the ``data_format`` and
    constructs a ``series`` description that downstream renderers consume.
    """

    def __init__(
        self,
        chart_type: str,
        data: pd.DataFrame,
        x: str,
        *,
        y: Optional[str] = None,
        series: Optional[list[dict]] = None,
        value_axis_range: Optional[tuple[float, float]] = None,
        value_axis_tick_format: Optional[str] = None,
        data_format: str = "wide",
        series_field: Optional[str] = None,
        show_data_labels: bool = False,
    ):
        """Create a new :class:`ChartSpec` instance.

        Args:
            chart_type: The type of chart (e.g., ``"bar"``, ``"line"``).
            data: The data source as a :class:`pandas.DataFrame`.
            x: The column name to use for the x‑axis.
            y: The column name for the y‑axis when ``data_format`` is ``"wide"``.
                May be a list of column names.
            series: Explicit series definitions. Each entry is a ``dict`` with
                at least ``"column"`` and ``"name"`` keys.
            value_axis_range: Optional tuple defining the min and max values
                for the value axis.
            value_axis_tick_format: Optional format string for axis ticks.
            data_format: ``"wide"`` (default) or ``"long"``. Determines how
                ``data`` is interpreted and possibly reshaped.
            series_field: When ``data_format`` is ``"long"``, the column that
                identifies distinct series.
            show_data_labels: Whether to display data labels on the chart.
        """
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
        """Convert long‑format data to wide format.

        Args:
            data: The input :class:`pandas.DataFrame` in long format.
            x: Column name representing categories on the x‑axis.
            y: Column name containing the values.
            series_field: Column name that distinguishes different series.

        Returns:
            A new :class:`pandas.DataFrame` pivoted to wide format with NaN
            values replaced by ``None``.
        """
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
