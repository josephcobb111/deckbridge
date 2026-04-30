from deckbridge.deck.specs import LayoutSpec

LAYOUTS = {
    # =========================================================
    # TITLE SLIDE
    # =========================================================
    "title_slide": LayoutSpec(
        name="title_slide",
        slots={
            "deck_title": {"type": "text", "x": 1, "y": 2, "w": 8, "h": 1},
            "deck_author": {"type": "text", "x": 1, "y": 3.2, "w": 8, "h": 0.8},
        },
    ),
    # =========================================================
    # ONE CHART
    # =========================================================
    "one_chart": LayoutSpec(
        name="one_chart",
        slots={
            # Slide title (top)
            "slide_title": {"type": "text", "x": 0.5, "y": 0.1, "w": 12.5, "h": 0.8},
            # Chart
            "chart_1": {"type": "chart", "x": 0.5, "y": 1.6, "w": 12.5, "h": 5.25},
            # Chart title (above chart)
            "chart_1_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_1",
                "x": 0.5,
                "y": 1.1,
                "w": 12.5,
                "h": 0.5,
            },
            "notes": {"type": "text", "x": 0.5, "y": 6.85, "w": 12.5, "h": 0.8},
        },
    ),
    # =========================================================
    # TWO CHART
    # =========================================================
    "two_chart": LayoutSpec(
        name="two_chart",
        slots={
            # Slide title
            "slide_title": {"type": "text", "x": 0.5, "y": 0.1, "w": 12.5, "h": 0.8},
            # Chart 1
            "chart_1": {"type": "chart", "x": 0.5, "y": 1.6, "w": 6.25, "h": 5.25},
            "chart_1_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_1",
                "x": 0.5,
                "y": 1.1,
                "w": 6.25,
                "h": 0.5,
            },
            # Chart 2
            "chart_2": {"type": "chart", "x": 6.75, "y": 1.6, "w": 6.25, "h": 5.25},
            "chart_2_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_2",
                "x": 6.75,
                "y": 1.1,
                "w": 6.25,
                "h": 0.5,
            },
            "notes": {"type": "text", "x": 0.5, "y": 6.85, "w": 12.5, "h": 0.8},
        },
    ),
    # =========================================================
    # THREE CHART
    # =========================================================
    "three_chart": LayoutSpec(
        name="three_chart",
        slots={
            # Slide title
            "slide_title": {"type": "text", "x": 0.5, "y": 0.1, "w": 12.5, "h": 0.8},
            # Chart 1
            "chart_1": {"type": "chart", "x": 0.5, "y": 1.6, "w": 4.17, "h": 5.25},
            "chart_1_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_1",
                "x": 0.5,
                "y": 1.1,
                "w": 4.17,
                "h": 0.5,
            },
            # Chart 2
            "chart_2": {"type": "chart", "x": 4.67, "y": 1.6, "w": 4.17, "h": 5.25},
            "chart_2_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_2",
                "x": 4.67,
                "y": 1.1,
                "w": 4.17,
                "h": 0.5,
            },
            # Chart 3
            "chart_3": {"type": "chart", "x": 8.84, "y": 1.6, "w": 4.17, "h": 5.25},
            "chart_3_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_3",
                "x": 8.84,
                "y": 1.1,
                "w": 4.17,
                "h": 0.5,
            },
            "notes": {"type": "text", "x": 0.5, "y": 6.85, "w": 12.5, "h": 0.8},
        },
    ),
}
