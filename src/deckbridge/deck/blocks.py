from dataclasses import dataclass

from deckbridge.deck.specs import ChartSpec


@dataclass
class ChartBlock:
    chart: ChartSpec
    chart_title: str = ""
    chart_subtitle: str = ""
    value_axis_title: str = ""
    category_axis_title: str = ""
