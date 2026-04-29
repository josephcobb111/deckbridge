EMU_PER_INCH = 914400
PIXEL_PER_INCH = 96

DEFAULT_PPTX_TO_GOOGLE_SCALE_FACTOR = 1


def inches_to_emu(inches):
    return int(inches * EMU_PER_INCH * DEFAULT_PPTX_TO_GOOGLE_SCALE_FACTOR)


def inches_to_pixels(inches):
    return int(inches * PIXEL_PER_INCH * DEFAULT_PPTX_TO_GOOGLE_SCALE_FACTOR)


def hex_to_slides_rgb(hex_color: str) -> dict:
    """
    Convert a hex color string (e.g. '7F7F7F' or '#7F7F7F')
    to Google Slides API rgbColor format (0–1 floats).
    """
    hex_color = hex_color.lstrip("#")

    if len(hex_color) != 6:
        raise ValueError("Hex color must be 6 characters long.")

    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255

    return {"red": r, "green": g, "blue": b}
