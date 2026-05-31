from deckbridge.themes.default import DEFAULT_TEXT_STYLE
from deckbridge.utils import deep_merge


def resolve_chart_theme(theme, layout_name, style_overrides=None):
    """Resolve the chart style configuration for a given layout.

    Combines the default chart style with any layout‑specific overrides and
    optional user‑provided ``style_overrides``. The merging follows a deep‑merge
    strategy where later dictionaries take precedence.

    Args:
        theme (dict): The full theme dictionary containing ``"chart"`` settings.
        layout_name (str): Name of the layout for which to resolve chart styles.
        style_overrides (dict, optional): Additional overrides that should be
            applied on top of the resolved theme.

    Returns:
        dict: The resolved chart style dictionary for the specified layout.
    """
    base = theme.get("chart", {}).get("default", {})
    layout_override = theme.get("chart", {}).get("layouts", {}).get(layout_name, {})

    resolved = deep_merge(base, layout_override)
    if style_overrides:
        resolved = deep_merge(resolved, style_overrides)

    return resolved


def resolve_text_style(slot_key, slot, theme, layout_name, style_overrides):
    """Resolve the final text style for a slot.

    Merges style layers in the following order (later layers override earlier):

    1. ``DEFAULT_TEXT_STYLE`` – the package‑wide defaults.
    +   2. Global theme ``"text"`` settings.
    +    3. Theme ``"slots"`` overrides for the slot group.
    +    4. Chart‑specific style overrides when the slot pertains to a chart.
    +    5. The slot dictionary itself, which may contain explicit style keys.
    +    6. Optional ``style_overrides`` supplied by the caller.

    The function also validates that all required style keys are present.

    Args:
        slot_key (str): Fallback style key for the slot.
        slot (dict): Slot definition, possibly containing ``"style_key"`` and
            other style attributes.
        theme (dict): Theme configuration dictionary.
        layout_name (str): Name of the layout used for chart style resolution.
        style_overrides (dict): Optional explicit overrides.

    Returns:
        dict: A dictionary containing the fully resolved style.
    """
    """Merge style layers: DEFAULT → THEME (global) → THEME (slot) → slot."""
    slot_group = slot.get("style_key", slot_key)

    chart_theme = resolve_chart_theme(theme, layout_name, style_overrides) if "chart" in slot_key else {}

    style = {
        **DEFAULT_TEXT_STYLE,
        **theme.get("text", {}),
        **theme.get("slots", {}).get(slot_group, {}),
        **chart_theme.get(slot_group, {}),
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
    """Resolve the color for a chart series.

    The function picks a color in the following order:

    1. If the series dictionary defines a ``"color"`` key, that value is used.
    2. Otherwise, the function falls back to the ``"series_colors"`` palette
       defined in ``chart_theme`` and selects a color based on ``index`` using a
       modulo operation.
    3. If no palette is defined, a safe default color ``"#4E79A7"`` is returned.

    Args:
        series (dict): Series configuration which may contain an explicit ``"color"``.
        index (int): Index of the series within the chart (used for palette lookup).
        chart_theme (dict): Chart theme dictionary containing a ``"series_colors"`` list.

    Returns:
        str: Hex string representing the resolved color.
    """
    # Explicit series override wins
    if series.get("color"):
        return series["color"]

    palette = chart_theme.get("series_colors", [])

    if not palette:
        return "#4E79A7"  # safe fallback

    return palette[index % len(palette)]


def resolve_series_dash(series, chart_theme):
    """Resolve the dash style for a chart series.

    The dash style determines the line pattern used for the series. The
    resolution order is:

    1. If the ``series`` dict defines a ``"dash_style"`` key, that value is used.
    +   2. Otherwise, fall back to the ``"dash_style"`` defined in the chart theme's
    +      ``"series_defaults"``.
    +    3. If neither is present, the default ``"solid"`` is returned.

    Args:
        series (dict): Series configuration which may contain a ``"dash_style"``.
        chart_theme (dict): Chart theme dictionary containing ``"series_defaults"``.

    Returns:
        str: The resolved dash style (e.g., ``"solid"``, ``"dash"``).
    """
    if series.get("dash_style"):
        return series["dash_style"]

    return chart_theme.get("series_defaults", {}).get("dash_style", "solid")


def resolve_series_width(series, chart_theme):
    """Resolve the line width for a chart series.

    The width determination follows a similar precedence to other series
    attributes:

    1. If the ``series`` dict provides a ``"line_width"`` entry, that value is
       used directly.
    +   2. Otherwise, the function looks for a ``"line_width"`` value in the chart
    +      theme's ``"series_defaults"``.
    +    3. If neither source supplies a width, a default of ``2.25`` points is
    +       returned.

    Args:
        series (dict): Series configuration which may contain a ``"line_width"``.
        chart_theme (dict): Chart theme dictionary containing ``"series_defaults"``.

    Returns:
        float: The resolved line width.
    """
    if series.get("line_width"):
        return series["line_width"]

    return chart_theme.get("series_defaults", {}).get("line_width", 2.25)
