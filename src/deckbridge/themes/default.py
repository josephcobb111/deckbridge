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
        "chart_subtitle": {
            "font_size": 14,
            "align": "center",
            "bold": False,
            "italic": True,
            "underline": False,
        },
        "notes": {
            "font_size": 10,
        },
    },
    "chart": {
        "default": {
            "chart_title": {
                "has_title": False,
                "font_size": 14,
                "bold": True,
                "italic": False,
                "underline": True,
                "align": "center",
            },
            "chart_subtitle": {
                "has_title": False,
                "font_size": 12,
                "bold": False,
                "italic": True,
                "underline": False,
                "align": "center",
            },
            "value_axis": {
                "has_title": True,
                "font_size": 14,
                "bold": True,
                "italic": False,
                "underline": False,
            },
            "category_axis": {
                "has_title": True,
                "font_size": 14,
                "bold": True,
                "italic": False,
                "underline": False,
            },
            "legend": {
                "visible": True,
                "position": "BOTTOM",
                "font_size": 14,
            },
        },
        "layouts": {
            "one_chart": {},
            "two_chart": {},
            "three_chart": {},
        },
    },
}
