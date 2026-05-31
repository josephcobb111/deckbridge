"""Deck block definitions.

This module defines the data structures used to represent individual content
blocks within a slide. Currently only a :class:`ChartBlock` is defined, which
encapsulates a chart specification together with optional presentation metadata.
"""

from dataclasses import dataclass

from deckbridge.deck.specs import ChartSpec


@dataclass
class ChartBlock:
    """Container for a chart and its display attributes.

    Attributes:
        chart: The :class:`~deckbridge.deck.specs.ChartSpec` instance that
            contains all information required to render the chart (type,
            data, axes, series, etc.).
        chart_title: Optional title displayed above the chart. Defaults to an
            empty string.
        chart_subtitle: Optional subtitle displayed beneath the chart title.
            Defaults to an empty string.
        value_axis_title: Title for the value (y) axis. Empty string if not
            provided.
        category_axis_title: Title for the category (x) axis. Empty string if
            not provided.
        style_overrides: Dictionary of style properties to override the
            theme defaults for this specific chart. If ``None``, no overrides
            are applied.
    """

    chart: ChartSpec
    chart_title: str = ""
    chart_subtitle: str = ""
    value_axis_title: str = ""
    category_axis_title: str = ""
    style_overrides: dict | None = None
