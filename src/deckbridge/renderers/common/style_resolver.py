from deckbridge.themes.default import DEFAULT_TEXT_STYLE, THEME


def resolve_text_style(slot_key, slot):
    """
    Merge style layers:
    DEFAULT → THEME (global) → THEME (slot) → slot
    """

    # Match slot group (e.g. "chart_1_title" → "chart_title")
    slot_group = None
    if slot_key.endswith("_title") and "chart_" in slot_key:
        slot_group = "chart_title"
    else:
        slot_group = slot_key

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
