from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.text import PP_ALIGN

PPTX_ALIGN_MAP = {
    "center": PP_ALIGN.CENTER,
    "left": PP_ALIGN.LEFT,
    "right": PP_ALIGN.RIGHT,
    "justified": PP_ALIGN.JUSTIFY,
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
