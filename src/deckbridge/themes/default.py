DEFAULT_TEXT_STYLE = {
    "font_size": 16,
    "font_color": "#000000",
    "font_family": "Arial",
    "bold": False,
    "italic": False,
    "underline": False,
    "align": "left",
}


THEME = {
    "text": {},
    "slots": {
        "deck_title": {
            "font_size": 32,
            "font_color": "#7F7F7F",
            "bold": True,
            "italic": False,
            "underline": False,
        },
        "deck_author": {
            "font_size": 18,
            "align": "left",
        },
        "slide_title": {
            "font_size": 20,
            "font_color": "#7F7F7F",
            "bold": True,
        },
        "chart_title": {
            "font_size": 16,
            "align": "center",
            "bold": True,
            "underline": True,
        },
    },
    "chart": {
        "default": {
            "axis": {"font_size": 12},
            "legend": {"visible": True, "position": "BOTTOM", "font_size": 10},
            "chart_title": {"has_title": False},
        },
        "layouts": {
            "one_chart": {
                "axis": {"font_size": 14},
                "legend": {"font_size": 12},
            },
            "two_chart": {
                "axis": {"font_size": 12},
                "legend": {"font_size": 10},
            },
            "three_chart": {
                "axis": {"font_size": 12},
                "legend": {"font_size": 10},
            },
        },
    },
}
