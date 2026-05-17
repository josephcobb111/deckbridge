from deckbridge.themes.default import DEFAULT_TEXT_STYLE, THEME
from deckbridge.utils import deep_merge


def resolve_chart_theme(theme, layout_name):
    base = theme.get("chart", {}).get("default", {})
    layout_override = theme.get("chart", {}).get("layouts", {}).get(layout_name, {})

    return deep_merge(base, layout_override)


def resolve_text_style(slot_key, slot):
    """
    Merge style layers:
    DEFAULT → THEME (global) → THEME (slot) → slot
    """

    slot_group = slot.get("style_key", slot_key)

    style = {
        **DEFAULT_TEXT_STYLE,
        **THEME.get("text", {}),
        **THEME.get("slots", {}).get(slot_group, {}),
        **slot,
    }

    # enforce completeness
    required = [
        "font_size",
        "font_color",
        "align",
        "bold",
        "italic",
        "underline",
    ]

    for key in required:
        if key not in style:
            raise ValueError(f"Missing required style key: {key}")

    return style


def resolve_series_color(series, index, chart_theme):
    # Explicit series override wins
    if series.get("color"):
        return series["color"]

    palette = chart_theme.get("series_colors", [])

    if not palette:
        return "#4E79A7"  # safe fallback

    return palette[index % len(palette)]


def resolve_series_dash(series, chart_theme):
    if series.get("dash_style"):
        return series["dash_style"]

    return chart_theme.get("series_defaults", {}).get("dash_style", "solid")


def resolve_series_width(series, chart_theme):
    if series.get("line_width"):
        return series["line_width"]

    return chart_theme.get("series_defaults", {}).get("line_width", 2.25)
