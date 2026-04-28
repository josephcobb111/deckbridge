from pptx.dml.color import RGBColor


def hex_to_rgb255(hex_color: str):
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return RGBColor(r, g, b)
