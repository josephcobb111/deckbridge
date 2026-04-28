from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from deckbridge.renderers.gslides.utils import hex_to_slides_rgb, inches_to_emu
from deckbridge.renderers.pptx.utils import hex_to_rgb255


def render_text_slots(
    backend,
    layout_spec,
    text_map,
    *,
    slide_obj=None,  # pptx
    slides_service=None,  # gslides
    presentation_id=None,
    page_id=None,
):
    """
    Render all text slots defined in a layout.

    Parameters
    ----------
    backend : "pptx" or "gslides"
    slide_obj :
        - pptx: Slide object
        - gslides: ignored (use page_id instead)
    layout_spec : LayoutSpec
    text_map : dict
        {"slot_name": "text"}
    slides_service : required for gslides
    presentation_id : required for gslides
    page_id : required for gslides
    """

    if backend == "pptx":
        _render_pptx(slide_obj, layout_spec, text_map)

    elif backend == "gslides":
        _render_gslides(
            slides_service,
            presentation_id,
            page_id,
            layout_spec,
            text_map,
        )

    else:
        raise ValueError(f"Unsupported backend: {backend}")


# =========================================================
# PPTX IMPLEMENTATION
# =========================================================
def _render_pptx(slide, layout_spec, text_map):
    for slot_name, text in text_map.items():
        if slot_name not in layout_spec.slots:
            continue
        if not text:
            continue

        slot = layout_spec.slots[slot_name]

        left = Inches(slot["x"])
        top = Inches(slot["y"])
        width = Inches(slot["w"])
        height = Inches(slot["h"])

        textbox = slide.shapes.add_textbox(left, top, width, height)
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
            p.font.color.rgb = hex_to_rgb255(slot.get("font_color"))

        p.font.bold = slot.get("bold") or False

        p.font.italic = slot.get("italic") or False

        p.font.underline = slot.get("underline") or False


# =========================================================
# GOOGLE SLIDES IMPLEMENTATION
# =========================================================
def _render_gslides(
    slides_service,
    presentation_id,
    page_id,
    layout_spec,
    text_map,
):
    requests = []

    for slot_name, text in text_map.items():
        if slot_name not in layout_spec.slots:
            continue
        if not text:
            continue

        slot = layout_spec.slots[slot_name]

        object_id = f"{slot_name}_{page_id}"

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

        requests.append({"insertText": {"objectId": object_id, "text": text}})

        if slot.get("font_size"):
            requests.append(
                {
                    "updateTextStyle": {
                        "objectId": object_id,
                        "textRange": {"type": "ALL"},
                        "style": {"fontSize": {"magnitude": slot.get("font_size"), "unit": "PT"}},
                        "fields": "fontSize",
                    },
                }
            )

        requests.append(
            {
                "updateTextStyle": {
                    "objectId": object_id,
                    "textRange": {"type": "ALL"},
                    "style": {
                        "bold": slot.get("bold") or False,
                        "italic": slot.get("italic") or False,
                        "underline": slot.get("underline") or False,
                    },
                    "fields": "bold,italic,underline",
                }
            }
        )

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
                        "style": {"alignment": align_map[slot.get("align")]},
                        "fields": "alignment",
                    },
                }
            )

        if slot.get("font_color"):
            color = hex_to_slides_rgb(slot.get("font_color"))
            requests.append(
                {
                    "updateTextStyle": {
                        "objectId": object_id,
                        "textRange": {"type": "ALL"},
                        "style": {"foregroundColor": {"opaqueColor": {"rgbColor": color}}},
                        "fields": "foregroundColor",
                    }
                }
            )

    if requests:
        slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
