from dataclasses import dataclass
from typing import Dict

from deckbridge.deck.specs import ChartSpec


@dataclass
class ChartBlock:
    chart: ChartSpec
    title: str = ""
