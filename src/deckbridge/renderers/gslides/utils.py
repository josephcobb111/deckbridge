import zlib

EMU_PER_INCH = 914400
PIXEL_PER_INCH = 96

DEFAULT_PPTX_TO_GOOGLE_SCALE_FACTOR = 1

GSLIDES_ALIGN_MAP = {
    "center": "CENTER",
    "left": "START",
    "right": "END",
    "justified": "JUSTIFIED",
}

GSLIDES_VERTICAL_ALIGN_MAP = {
    "TOP": "TOP",
    "MIDDLE": "MIDDLE",
    "BOTTOM": "BOTTOM",
}

GSHEETS_CHART_DASH_MAP = {
    "solid": "SOLID",
    "dash": "MEDIUM_DASHED",
    "dot": "DOTTED",
    "dash_dot": "MEDIUM_DASHED_DOTTED",
}

GSLIDES_LINE_DASH_MAP = {
    "solid": "SOLID",
    "dash": "DASH",
    "dot": "DOT",
    "dash_dot": "DASH_DOT",
}

GSHEETS_CHART_TYPE_MAP = {
    "line": "LINE",
    "bar": "COLUMN",
    "area_stacked": "AREA",
    "area_stacked_100": "AREA",
    "bar_stacked": "BAR",
    "column_stacked": "COLUMN",
    "scatter": "SCATTER",
}

GSHEETS_CHART_STACKING_MAP = {
    "line": "NOT_STACKED",
    "bar": "NOT_STACKED",
    "area_stacked": "STACKED",
    "area_stacked_100": "PERCENT_STACKED",
    "bar_stacked": "STACKED",
    "column_stacked": "STACKED",
    "scatter": "NOT_STACKED",
}


def inches_to_emu(inches: float) -> int:
    """Convert inches to EMU (English Metric Units).

    Args:
        inches: Length in inches.

    Returns:
        Length in EMU.
    """
    return int(inches * EMU_PER_INCH * DEFAULT_PPTX_TO_GOOGLE_SCALE_FACTOR)


def inches_to_pixels(inches: float) -> int:
    """Convert inches to pixels.

    Args:
        inches: Length in inches.

    Returns:
        Length in pixels.
    """
    return int(inches * PIXEL_PER_INCH * DEFAULT_PPTX_TO_GOOGLE_SCALE_FACTOR)


def hex_to_slides_rgb(hex_color: str) -> dict:
    """Convert a hex color string (e.g. '7F7F7F' or '#7F7F7F') to Google Slides API rgbColor format (0–1 floats).

    Args:
        hex_color: Hex color string with or without '#'.

    Returns:
        Dictionary with 'red', 'green', 'blue' keys (values between 0 and 1).

    Raises:
        ValueError: If hex_color is not 6 characters long.
    """
    hex_color = hex_color.lstrip("#")

    if len(hex_color) != 6:
        raise ValueError("Hex color must be 6 characters long.")

    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255

    return {"red": r, "green": g, "blue": b}


def text_to_number(text: str) -> int:
    """Convert text to a number using CRC32 hash.

    Args:
        text: Input text to convert.

    Returns:
        Hashed number between 0 and 2^31-1.
    """
    return zlib.crc32(text.encode()) & 0x7FFFFFFF
