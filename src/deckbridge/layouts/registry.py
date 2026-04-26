from deckbridge.deck.specs import LayoutSpec

LAYOUTS = {
    "one_chart": LayoutSpec(name="one_chart", slots={"chart_1": {"x": 1, "y": 1.5, "w": 8, "h": 4.5}}),
    "two_chart": LayoutSpec(
        name="two_chart",
        slots={
            "chart_1": {"x": 0.5, "y": 1.5, "w": 4.5, "h": 4},
            "chart_2": {"x": 5, "y": 1.5, "w": 4.5, "h": 4},
        },
    ),
    "three_chart": LayoutSpec(
        name="three_chart",
        slots={
            "chart_1": {"x": 0.5, "y": 1.5, "w": 3, "h": 4},
            "chart_2": {"x": 3.5, "y": 1.5, "w": 3, "h": 4},
            "chart_3": {"x": 6.5, "y": 1.5, "w": 3, "h": 4},
        },
    ),
}
