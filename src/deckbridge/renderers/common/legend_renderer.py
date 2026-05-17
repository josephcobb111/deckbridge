from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.util import Inches, Pt

from deckbridge.renderers.common.style_resolver import (
    resolve_chart_theme,
    resolve_series_color,
    resolve_series_dash,
    resolve_series_width,
)
from deckbridge.renderers.common.text_renderer import (
    render_text_slot,
)
from deckbridge.renderers.gslides.utils import GSLIDES_LINE_DASH_MAP, hex_to_slides_rgb, inches_to_emu
from deckbridge.renderers.pptx.utils import PPTX_DASH_MAP, hex_to_rgb255


def render_color_legend(ctx, slot_key, slot, slide):

    color_legend = slide.get("color_legend", [])

    if not color_legend:
        return

    if ctx.backend == "pptx":
        _render_color_legend_pptx(
            ctx,
            slot,
            color_legend,
        )

    elif ctx.backend == "gslides":
        _render_color_legend_gslides(
            ctx,
            slot_key,
            slot,
            color_legend,
        )


def _render_color_legend_pptx(
    ctx,
    slot,
    color_legend,
):

    x = slot["x"]
    y = slot["y"]

    max_rows = 2
    col_w = 1.75
    row_h = 0.25
    box_size = 0.18

    for i, _series in enumerate(color_legend):
        color = _series.get("color", "#999999")

        row = i % max_rows
        col = i // max_rows

        x_i = x + (col * col_w)
        y_i = y + (row * row_h)

        square = ctx.slide_obj.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.RECTANGLE,
            Inches(x_i),
            Inches(y_i),
            Inches(box_size),
            Inches(box_size),
        )

        square.fill.solid()
        square.fill.fore_color.rgb = hex_to_rgb255(color)

        square.line.fill.background()
        square.shadow.inherit = False

        textbox = ctx.slide_obj.shapes.add_textbox(
            Inches(x_i + 0.14),
            Inches(y_i - 0.09),
            Inches(1.5),
            Inches(0.3),
        )

        textbox.text_frame.text = _series.get("name") or _series.get("column") or _series["label"]
        textbox.text_frame.paragraphs[0].font.size = Pt(12)


def _render_color_legend_gslides(
    ctx,
    slot_key,
    slot,
    color_legend,
):

    requests = []

    x = slot["x"]
    y = slot["y"]

    max_rows = 2
    col_w = 1.75
    row_h = 0.25
    box_size = 0.18

    for i, _series in enumerate(color_legend):
        color = _series.get("color", "#999999")

        row = i % max_rows
        col = i // max_rows

        x_i = x + (col * col_w)
        y_i = y + (row * row_h)

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
                                "magnitude": inches_to_emu(box_size),
                                "unit": "EMU",
                            },
                            "width": {
                                "magnitude": inches_to_emu(box_size),
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
            "x": x_i + 0.14,
            "y": y_i - 0.09,
            "w": 1.5,
            "h": 0.3,
        }

        render_text_slot(
            backend="gslides",
            slot_key=f"{slot_key}_text_{i}",
            slot=text_slot,
            text=(_series.get("name") or _series.get("column") or _series["label"]),
            slides_service=ctx.slides_service,
            presentation_id=ctx.presentation_id,
            page_id=ctx.page_id,
        )

    if requests:
        ctx.slides_service.presentations().batchUpdate(
            presentationId=ctx.presentation_id,
            body={"requests": requests},
        ).execute()


def render_dash_legend(ctx, slot_key, slot, slide):

    dash_legend = slide.get("dash_legend", [])

    if not dash_legend:
        return

    if ctx.backend == "pptx":
        _render_dash_legend_pptx(
            ctx,
            slot,
            dash_legend,
        )

    elif ctx.backend == "gslides":
        _render_dash_legend_gslides(
            ctx,
            slot_key,
            slot,
            dash_legend,
        )


def _render_dash_legend_pptx(ctx, slot, dash_legend):
    x = slot["x"]
    y = slot["y"]

    line_w = 0.35
    row_h = 0.25

    for i, _series in enumerate(dash_legend):
        label = _series.get("label", "")
        color = _series.get("color", "#999999")
        dash = _series.get("dash_style", "solid")
        width = _series.get("width", 2)

        y_i = y + i * row_h

        line = ctx.slide_obj.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT,
            Inches(x),
            Inches(y_i),
            Inches(x + line_w),
            Inches(y_i),
        )

        line.line.color.rgb = hex_to_rgb255(color)
        line.line.width = Pt(width)
        line.shadow.inherit = False

        if dash != "solid":
            line.line.dash_style = PPTX_DASH_MAP[dash]

        textbox = ctx.slide_obj.shapes.add_textbox(
            Inches(x + 0.45),
            Inches(y_i - 0.15),
            Inches(1.5),
            Inches(0.3),
        )

        textbox.text_frame.text = label
        textbox.text_frame.paragraphs[0].font.size = Pt(12)


def _render_dash_legend_gslides(ctx, slot_key, slot, dash_legend):
    requests = []

    x = slot["x"]
    y = slot["y"]

    line_w = 0.35
    row_h = 0.25

    for i, _series in enumerate(dash_legend):
        label = _series.get("label", "")
        color = _series.get("color", "#999999")
        dash = _series.get("dash_style", "solid")
        width = _series.get("width", 2)

        y_i = y + i * row_h

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
                                "magnitude": inches_to_emu(line_w),
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

        text_id = f"{slot_key}_text_{i}_{ctx.page_id}"

        requests.append(
            {
                "createShape": {
                    "objectId": text_id,
                    "shapeType": "TEXT_BOX",
                    "elementProperties": {
                        "pageObjectId": ctx.page_id,
                        "size": {
                            "height": {
                                "magnitude": inches_to_emu(0.3),
                                "unit": "EMU",
                            },
                            "width": {
                                "magnitude": inches_to_emu(1.5),
                                "unit": "EMU",
                            },
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": inches_to_emu(x + 0.45),
                            "translateY": inches_to_emu(y_i - 0.15),
                            "unit": "EMU",
                        },
                    },
                }
            }
        )

        requests.append(
            {
                "insertText": {
                    "objectId": text_id,
                    "text": label,
                }
            }
        )

        requests.append(
            {
                "updateTextStyle": {
                    "objectId": text_id,
                    "textRange": {"type": "ALL"},
                    "style": {
                        "fontSize": {
                            "magnitude": 12,
                            "unit": "PT",
                        },
                        "bold": False,
                    },
                    "fields": "fontSize,bold",
                }
            }
        )

        requests.append(
            {
                "updateParagraphStyle": {
                    "objectId": text_id,
                    "textRange": {"type": "ALL"},
                    "style": {
                        "alignment": "START",
                    },
                    "fields": "alignment",
                }
            }
        )

        requests.append(
            {
                "updateShapeProperties": {
                    "objectId": text_id,
                    "shapeProperties": {"contentAlignment": "MIDDLE"},
                    "fields": "contentAlignment",
                }
            }
        )

    ctx.slides_service.presentations().batchUpdate(
        presentationId=ctx.presentation_id,
        body={"requests": requests},
    ).execute()
