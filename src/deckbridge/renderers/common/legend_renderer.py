from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.util import Inches, Pt

from deckbridge.renderers.common.text_renderer import render_text_slot
from deckbridge.renderers.gslides.utils import (
    GSLIDES_LINE_DASH_MAP,
    hex_to_slides_rgb,
    inches_to_emu,
)
from deckbridge.renderers.pptx.utils import (
    PPTX_DASH_MAP,
    hex_to_rgb255,
)

LEGEND_STYLE = {
    "font_size": 12,
    # Layout
    "max_rows": 2,
    "col_w": 1.15,
    "row_h": 0.25,
    # Color legend
    "box_size": 0.18,
    "text_x_offset": 0.14,
    "text_y_offset": -0.08,
    "text_box_w": 1,
    "text_box_h": 0.3,
    # Dash legend
    "line_w": 0.35,
    "line_text_x_offset": 0.45,
    "line_text_y_offset": -0.15,
}


# =========================================================
# Helpers
# =========================================================


def _get_label(item):
    return item.get("name") or item.get("column") or item.get("label", "")


def _grid_position(i, x, y):
    row = i % LEGEND_STYLE["max_rows"]
    col = i // LEGEND_STYLE["max_rows"]

    return (
        x + col * LEGEND_STYLE["col_w"],
        y + row * LEGEND_STYLE["row_h"],
    )


def _line_position(i, y):
    return y + (i * LEGEND_STYLE["row_h"])


# =========================================================
# COLOR LEGEND
# =========================================================


def render_color_legend(ctx, slot_key, slot, slide):

    legend = slide.get("color_legend", [])

    if not legend:
        return

    if ctx.backend == "pptx":
        _render_color_legend_pptx(
            ctx,
            slot,
            legend,
        )

    elif ctx.backend == "gslides":
        _render_color_legend_gslides(
            ctx,
            slot_key,
            slot,
            legend,
        )


def _render_color_legend_pptx(
    ctx,
    slot,
    legend,
):

    x = slot["x"]
    y = slot["y"]

    for i, item in enumerate(legend):
        x_i, y_i = _grid_position(i, x, y)

        color = item.get("color", "#999999")

        square = ctx.slide_obj.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.RECTANGLE,
            Inches(x_i),
            Inches(y_i),
            Inches(LEGEND_STYLE["box_size"]),
            Inches(LEGEND_STYLE["box_size"]),
        )

        square.fill.solid()
        square.fill.fore_color.rgb = hex_to_rgb255(color)

        square.line.fill.background()
        square.shadow.inherit = False

        textbox = ctx.slide_obj.shapes.add_textbox(
            Inches(x_i + LEGEND_STYLE["text_x_offset"]),
            Inches(y_i + LEGEND_STYLE["text_y_offset"]),
            Inches(LEGEND_STYLE["text_box_w"]),
            Inches(LEGEND_STYLE["text_box_h"]),
        )

        textbox.text_frame.text = _get_label(item)
        textbox.text_frame.paragraphs[0].font.size = Pt(LEGEND_STYLE["font_size"])


def _render_color_legend_gslides(
    ctx,
    slot_key,
    slot,
    legend,
):

    requests = []

    x = slot["x"]
    y = slot["y"]

    for i, item in enumerate(legend):
        x_i, y_i = _grid_position(i, x, y)

        color = item.get("color", "#999999")

        box_id = f"{slot_key}_box_{i}_{ctx.page_id}"

        requests.append(
            {
                "createShape": {
                    "objectId": box_id,
                    "shapeType": "RECTANGLE",
                    "elementProperties": {
                        "pageObjectId": ctx.page_id,
                        "size": {
                            "height": {
                                "magnitude": inches_to_emu(LEGEND_STYLE["box_size"]),
                                "unit": "EMU",
                            },
                            "width": {
                                "magnitude": inches_to_emu(LEGEND_STYLE["box_size"]),
                                "unit": "EMU",
                            },
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": inches_to_emu(x_i),
                            "translateY": inches_to_emu(y_i),
                            "unit": "EMU",
                        },
                    },
                }
            }
        )

        requests.append(
            {
                "updateShapeProperties": {
                    "objectId": box_id,
                    "shapeProperties": {"shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": hex_to_slides_rgb(color)}}}},
                    "fields": "shapeBackgroundFill",
                }
            }
        )

        text_slot = {
            "x": x_i + LEGEND_STYLE["text_x_offset"],
            "y": y_i + LEGEND_STYLE["text_y_offset"],
            "w": LEGEND_STYLE["text_box_w"],
            "h": LEGEND_STYLE["text_box_h"],
            "vertical_align": "MIDDLE",
        }

        render_text_slot(
            backend="gslides",
            slot_key=f"{slot_key}_text_{i}",
            slot=text_slot,
            text=_get_label(item),
            slides_service=ctx.slides_service,
            presentation_id=ctx.presentation_id,
            page_id=ctx.page_id,
        )

    if requests:
        ctx.slides_service.presentations().batchUpdate(
            presentationId=ctx.presentation_id,
            body={"requests": requests},
        ).execute()


# =========================================================
# DASH LEGEND
# =========================================================


def render_dash_legend(ctx, slot_key, slot, slide):

    legend = slide.get("dash_legend", [])

    if not legend:
        return

    if ctx.backend == "pptx":
        _render_dash_legend_pptx(
            ctx,
            slot,
            legend,
        )

    elif ctx.backend == "gslides":
        _render_dash_legend_gslides(
            ctx,
            slot_key,
            slot,
            legend,
        )


def _render_dash_legend_pptx(
    ctx,
    slot,
    legend,
):

    x = slot["x"]
    y = slot["y"]

    for i, item in enumerate(legend):
        y_i = _line_position(i, y)

        label = _get_label(item)
        color = item.get("color", "#999999")
        dash = item.get("dash_style", "solid")
        width = item.get("width", 2)

        line = ctx.slide_obj.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT,
            Inches(x),
            Inches(y_i),
            Inches(x + LEGEND_STYLE["line_w"]),
            Inches(y_i),
        )

        line.line.color.rgb = hex_to_rgb255(color)
        line.line.width = Pt(width)
        line.shadow.inherit = False

        if dash != "solid":
            line.line.dash_style = PPTX_DASH_MAP[dash]

        textbox = ctx.slide_obj.shapes.add_textbox(
            Inches(x + LEGEND_STYLE["line_text_x_offset"]),
            Inches(y_i + LEGEND_STYLE["line_text_y_offset"]),
            Inches(1.5),
            Inches(0.3),
        )

        textbox.text_frame.text = label
        textbox.text_frame.paragraphs[0].font.size = Pt(LEGEND_STYLE["font_size"])


def _render_dash_legend_gslides(
    ctx,
    slot_key,
    slot,
    legend,
):

    requests = []

    x = slot["x"]
    y = slot["y"]

    for i, item in enumerate(legend):
        y_i = _line_position(i, y)

        label = _get_label(item)
        color = item.get("color", "#999999")
        dash = item.get("dash_style", "solid")
        width = item.get("width", 2)

        line_id = f"{slot_key}_line_{i}_{ctx.page_id}"

        requests.append(
            {
                "createLine": {
                    "objectId": line_id,
                    "category": "STRAIGHT",
                    "elementProperties": {
                        "pageObjectId": ctx.page_id,
                        "size": {
                            "width": {
                                "magnitude": inches_to_emu(LEGEND_STYLE["line_w"]),
                                "unit": "EMU",
                            },
                            "height": {
                                "magnitude": 0,
                                "unit": "EMU",
                            },
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": inches_to_emu(x),
                            "translateY": inches_to_emu(y_i),
                            "unit": "EMU",
                        },
                    },
                }
            }
        )

        requests.append(
            {
                "updateLineProperties": {
                    "objectId": line_id,
                    "lineProperties": {
                        "weight": {
                            "magnitude": width,
                            "unit": "PT",
                        },
                        "dashStyle": GSLIDES_LINE_DASH_MAP[dash],
                        "lineFill": {"solidFill": {"color": {"rgbColor": hex_to_slides_rgb(color)}}},
                    },
                    "fields": "weight,dashStyle,lineFill",
                }
            }
        )

        text_slot = {
            "x": x + LEGEND_STYLE["line_text_x_offset"],
            "y": y_i + LEGEND_STYLE["line_text_y_offset"],
            "w": 1.5,
            "h": 0.3,
            "vertical_align": "MIDDLE",
        }

        render_text_slot(
            backend="gslides",
            slot_key=f"{slot_key}_text_{i}",
            slot=text_slot,
            text=label,
            slides_service=ctx.slides_service,
            presentation_id=ctx.presentation_id,
            page_id=ctx.page_id,
        )

    if requests:
        ctx.slides_service.presentations().batchUpdate(
            presentationId=ctx.presentation_id,
            body={"requests": requests},
        ).execute()
