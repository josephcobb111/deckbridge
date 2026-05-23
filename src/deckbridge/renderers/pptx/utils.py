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
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return RGBColor(r, g, b)


def _validate_xy_numeric(x_values, y_values, x_col, y_col):
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
