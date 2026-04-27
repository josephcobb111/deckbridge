from deckbridge.deck.specs import LayoutSpec

LAYOUTS = {
    # =========================================================
    # ONE CHART
    # =========================================================
    "one_chart": LayoutSpec(
        name="one_chart",
        slots={
            # Slide title (top)
            "slide_title": {"x": 0.5, "y": 0.1, "w": 12.5, "h": 0.8},
            # Chart title (above chart)
            "chart_1_title": {"x": 0.5, "y": 1.1, "w": 12.5, "h": 0.5},
            # Chart
            "chart_1": {"x": 0.5, "y": 1.6, "w": 12.5, "h": 5.25},
        },
    ),
    # =========================================================
    # TWO CHART
    # =========================================================
    "two_chart": LayoutSpec(
        name="two_chart",
        slots={
            # Slide title
            "slide_title": {"x": 0.5, "y": 0.1, "w": 12.5, "h": 0.8},
            # Chart 1
            "chart_1_title": {"x": 0.5, "y": 1.2, "w": 4.5, "h": 0.4},
            "chart_1": {"x": 0.5, "y": 1.7, "w": 4.5, "h": 4},
            # Chart 2
            "chart_2_title": {"x": 5, "y": 1.2, "w": 4.5, "h": 0.4},
            "chart_2": {"x": 5, "y": 1.7, "w": 4.5, "h": 4},
        },
    ),
    # =========================================================
    # THREE CHART
    # =========================================================
    "three_chart": LayoutSpec(
        name="three_chart",
        slots={
            # Slide title
            "slide_title": {"x": 0.5, "y": 0.1, "w": 12.5, "h": 0.8},
            # Chart 1
            "chart_1_title": {"x": 0.5, "y": 1.2, "w": 3, "h": 0.4},
            "chart_1": {"x": 0.5, "y": 1.7, "w": 3, "h": 4},
            # Chart 2
            "chart_2_title": {"x": 3.5, "y": 1.2, "w": 3, "h": 0.4},
            "chart_2": {"x": 3.5, "y": 1.7, "w": 3, "h": 4},
            # Chart 3
            "chart_3_title": {"x": 6.5, "y": 1.2, "w": 3, "h": 0.4},
            "chart_3": {"x": 6.5, "y": 1.7, "w": 3, "h": 4},
        },
    ),
}
