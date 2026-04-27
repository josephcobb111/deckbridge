from dataclasses import dataclass

from deckbridge.deck.specs import ChartSpec


@dataclass
class ChartBlock:
    chart: ChartSpec
    title: str = ""
