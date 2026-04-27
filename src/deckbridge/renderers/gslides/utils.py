EMU_PER_INCH = 914400
PIXEL_PER_INCH = 96

DEFAULT_PPTX_TO_GOOGLE_SCALE_FACTOR = 0.75


def inches_to_emu(inches):
    return int(inches * EMU_PER_INCH * DEFAULT_PPTX_TO_GOOGLE_SCALE_FACTOR)


def inches_to_pixels(inches):
    return int(inches * PIXEL_PER_INCH * DEFAULT_PPTX_TO_GOOGLE_SCALE_FACTOR)
