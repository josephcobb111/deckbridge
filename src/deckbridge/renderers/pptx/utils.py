from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

PPTX_ALIGN_MAP = {
    "center": PP_ALIGN.CENTER,
    "left": PP_ALIGN.LEFT,
    "right": PP_ALIGN.RIGHT,
    "justified": PP_ALIGN.JUSTIFY,
}


def hex_to_rgb255(hex_color: str):
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return RGBColor(r, g, b)
