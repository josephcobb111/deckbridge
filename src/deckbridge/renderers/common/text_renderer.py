from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from deckbridge.renderers.common.style_resolver import resolve_text_style
from deckbridge.renderers.gslides.utils import GSLIDES_ALIGN_MAP, hex_to_slides_rgb, inches_to_emu
from deckbridge.renderers.pptx.utils import PPTX_ALIGN_MAP, hex_to_rgb255


def resolve_text_content(slide, slot_key, slot):
    content_type = slot.get("content_type")

    if content_type == "chart_title":
        block = slide["content"].get(slot["source"])
        return block.chart_title if block else None

    return slide.get(slot_key)


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
        _render_text_pptx(slide_obj, slot_key, slot, text)

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


def _render_text_pptx(slide, slot_key, slot, text):
    style = resolve_text_style(slot_key, slot)

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

    p.font.size = Pt(style["font_size"])
    p.alignment = PPTX_ALIGN_MAP[style["align"]]
    p.font.color.rgb = hex_to_rgb255(style["font_color"])
    p.font.bold = style["bold"]
    p.font.italic = style["italic"]
    p.font.underline = style["underline"]


def _render_text_gslides(
    slides_service,
    presentation_id,
    page_id,
    slot_key,
    slot,
    text,
):
    style = resolve_text_style(slot_key, slot)

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

    api_style = {
        "fontSize": {"magnitude": style["font_size"], "unit": "PT"},
        "foregroundColor": {"opaqueColor": {"rgbColor": hex_to_slides_rgb(style["font_color"])}},
        "bold": style["bold"],
        "italic": style["italic"],
        "underline": style["underline"],
    }

    requests.append(
        {
            "updateTextStyle": {
                "objectId": object_id,
                "textRange": {"type": "ALL"},
                "style": api_style,
                "fields": ",".join(api_style.keys()),
            }
        }
    )

    # Alignment
    requests.append(
        {
            "updateParagraphStyle": {
                "objectId": object_id,
                "textRange": {"type": "ALL"},
                "style": {"alignment": GSLIDES_ALIGN_MAP[style["align"]]},
                "fields": "alignment",
            }
        }
    )

    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests},
    ).execute()
