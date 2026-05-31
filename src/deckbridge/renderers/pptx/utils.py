import math
from numbers import Number

from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.text import MSO_VERTICAL_ANCHOR, PP_ALIGN

PPTX_ALIGN_MAP = {
    "center": PP_ALIGN.CENTER,
    "left": PP_ALIGN.LEFT,
    "right": PP_ALIGN.RIGHT,
    "justified": PP_ALIGN.JUSTIFY,
}

PPTX_VERTICAL_ALIGN_MAP = {
    "TOP": MSO_VERTICAL_ANCHOR.TOP,
    "MIDDLE": MSO_VERTICAL_ANCHOR.MIDDLE,
    "BOTTOM": MSO_VERTICAL_ANCHOR.BOTTOM,
}

PPTX_DASH_MAP = {
    "solid": MSO_LINE_DASH_STYLE.SOLID,
    "dash": MSO_LINE_DASH_STYLE.DASH,
    "dot": MSO_LINE_DASH_STYLE.ROUND_DOT,
    "dash_dot": MSO_LINE_DASH_STYLE.DASH_DOT,
}


def hex_to_rgb255(hex_color: str):
    """Convert a hex color string to a ``pptx`` ``RGBColor`` object.

    The input may optionally start with ``#``. The function parses the
    six‑character hexadecimal value and returns an ``RGBColor`` instance
    with integer components in the range 0‑255.

    Args:
        hex_color: A color string such as "#ff00aa" or "ff00aa".

    Returns:
        An ``RGBColor`` representing the equivalent color.
    """
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return RGBColor(r, g, b)


def _validate_xy_numeric(x_values, y_values, x_col, y_col):
    """Validate that X and Y values for a scatter chart are numeric.

    The function iterates over the supplied ``x_values`` and ``y_values`` sequences
    and raises a ``ValueError`` if any entry is not a real number (including ``bool``
    or ``nan``).  The error messages identify the offending column name and the
    index of the problematic row, which assists callers in pinpointing data issues.

    Args:
        x_values (Sequence): Iterable of X‑axis values.
        y_values (Sequence): Iterable of Y‑axis values.
        x_col (str): Column name for the X values – used in error messages.
        y_col (str): Column name for the Y values – used in error messages.

    Raises:
        ValueError: If a non‑numeric or ``nan`` value is encountered in either
            sequence.
    """
    for i, x in enumerate(x_values):
        if not isinstance(x, Number) or isinstance(x, bool) or math.isnan(float(x)):
            raise ValueError(
                f"Smooth scatter chart requires numeric X values. Column '{x_col}' contains invalid value {repr(x)} at row {i}."
            )

    for i, y in enumerate(y_values):
        if not isinstance(y, Number) or isinstance(y, bool) or math.isnan(float(y)):
            raise ValueError(
                f"Smooth scatter chart requires numeric Y values. Column '{y_col}' contains invalid value {repr(y)} at row {i}."
            )
