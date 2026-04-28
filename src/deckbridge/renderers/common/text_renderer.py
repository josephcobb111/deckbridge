import uuid

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from deckbridge.renderers.gslides.utils import hex_to_slides_rgb, inches_to_emu
from deckbridge.renderers.pptx.utils import hex_to_rgb255


def resolve_text_content(slide, slot_key):
    # Slide
    content = slide.get(slot_key)
    if content is not None:
        return content

    # Chart-derived
    if slot_key.endswith("_title"):
        chart_key = slot_key.replace("_title", "")
        block = slide["content"].get(chart_key)
        if block:
            return block.chart_title

    return None


def render_text_slot(
    backend,
    slot_key,
    slot,
    text,
    *,
    slide_obj=None,
    slides_service=None,
    presentation_id=None,
    page_id=None,
):
    if not text:
        return

    if backend == "pptx":
        _render_text_pptx(slide_obj, slot, text)

    elif backend == "gslides":
        _render_text_gslides(
            slides_service,
            presentation_id,
            page_id,
            slot_key,
            slot,
            text,
        )

    else:
        raise ValueError(f"Unsupported backend: {backend}")


def _render_text_pptx(slide, slot, text):
    textbox = slide.shapes.add_textbox(
        Inches(slot["x"]),
        Inches(slot["y"]),
        Inches(slot["w"]),
        Inches(slot["h"]),
    )

    tf = textbox.text_frame
    tf.clear()

    p = tf.paragraphs[0]
    p.text = text

    if slot.get("font_size"):
        p.font.size = Pt(slot["font_size"])

    align_map = {
        "center": PP_ALIGN.CENTER,
        "left": PP_ALIGN.LEFT,
        "right": PP_ALIGN.RIGHT,
        "justified": PP_ALIGN.JUSTIFY,
    }
    if slot.get("align"):
        p.alignment = align_map[slot["align"]]

    if slot.get("font_color"):
        p.font.color.rgb = hex_to_rgb255(slot["font_color"])

    p.font.bold = slot.get("bold", False)
    p.font.italic = slot.get("italics", False)
    p.font.underline = slot.get("underline", False)


def _render_text_gslides(
    slides_service,
    presentation_id,
    page_id,
    slot_key,
    slot,
    text,
):
    object_id = f"{slot_key}_{page_id}"

    requests = []

    # Create box
    requests.append(
        {
            "createShape": {
                "objectId": object_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": page_id,
                    "size": {
                        "height": {"magnitude": inches_to_emu(slot["h"]), "unit": "EMU"},
                        "width": {"magnitude": inches_to_emu(slot["w"]), "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": inches_to_emu(slot["x"]),
                        "translateY": inches_to_emu(slot["y"]),
                        "unit": "EMU",
                    },
                },
            }
        }
    )

    # Insert text
    requests.append(
        {
            "insertText": {
                "objectId": object_id,
                "text": text,
            }
        }
    )

    # Style
    style_fields = []
    style = {}

    if slot.get("font_size"):
        style["fontSize"] = {"magnitude": slot["font_size"], "unit": "PT"}
        style_fields.append("fontSize")

    if slot.get("font_color"):
        style["foregroundColor"] = {"opaqueColor": {"rgbColor": hex_to_slides_rgb(slot["font_color"])}}
        style_fields.append("foregroundColor")

    style["bold"] = slot.get("bold", False)
    style["italic"] = slot.get("italics", False)
    style["underline"] = slot.get("underline", False)
    style_fields.extend(["bold", "italic", "underline"])

    requests.append(
        {
            "updateTextStyle": {
                "objectId": object_id,
                "textRange": {"type": "ALL"},
                "style": style,
                "fields": ",".join(style_fields),
            }
        }
    )

    # Alignment
    align_map = {
        "center": "CENTER",
        "left": "START",
        "right": "END",
        "justified": "JUSTIFIED",
    }

    if slot.get("align"):
        requests.append(
            {
                "updateParagraphStyle": {
                    "objectId": object_id,
                    "textRange": {"type": "ALL"},
                    "style": {"alignment": align_map[slot["align"]]},
                    "fields": "alignment",
                }
            }
        )

    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests},
    ).execute()
