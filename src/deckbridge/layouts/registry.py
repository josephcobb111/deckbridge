from deckbridge.deck.specs import LayoutSpec

LAYOUTS = {
    # =========================================================
    # TITLE SLIDE
    # =========================================================
    "title_slide": LayoutSpec(
        name="title_slide",
        slots={
            "deck_title": {"x": 1, "y": 2, "w": 8, "h": 1},
            "deck_author": {"x": 1, "y": 3.2, "w": 8, "h": 0.8},
        },
    ),
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
            "chart_1_title": {"x": 0.5, "y": 1.1, "w": 6.25, "h": 0.5},
            "chart_1": {"x": 0.5, "y": 1.6, "w": 6.25, "h": 5.25},
            # Chart 2
            "chart_2_title": {"x": 6.75, "y": 1.1, "w": 6.25, "h": 0.5},
            "chart_2": {"x": 6.75, "y": 1.6, "w": 6.25, "h": 5.25},
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
            "chart_1_title": {"x": 0.5, "y": 1.1, "w": 4.17, "h": 0.5},
            "chart_1": {"x": 0.5, "y": 1.6, "w": 4.17, "h": 5.25},
            # Chart 2
            "chart_2_title": {"x": 4.67, "y": 1.1, "w": 4.17, "h": 0.5},
            "chart_2": {"x": 4.67, "y": 1.6, "w": 4.17, "h": 5.25},
            # Chart 3
            "chart_3_title": {"x": 8.84, "y": 1.1, "w": 4.17, "h": 0.5},
            "chart_3": {"x": 8.84, "y": 1.6, "w": 4.17, "h": 5.25},
        },
    ),
}
