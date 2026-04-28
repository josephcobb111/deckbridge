import uuid

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

        object_id = f"{page_id}_{slot_name}_{uuid.uuid4().hex[:6]}"

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

        style = {}
        fields = []

        if slot.get("font_size"):
            style["fontSize"] = {"magnitude": slot["font_size"], "unit": "PT"}
            fields.append("fontSize")

        style["bold"] = slot.get("bold") or False
        style["italic"] = slot.get("italic") or False
        style["underline"] = slot.get("underline") or False
        fields.extend(["bold", "italic", "underline"])

        if slot.get("font_color"):
            style["foregroundColor"] = {"opaqueColor": {"rgbColor": hex_to_slides_rgb(slot["font_color"])}}
            fields.append("foregroundColor")

        requests.append(
            {
                "updateTextStyle": {
                    "objectId": object_id,
                    "textRange": {"type": "ALL"},
                    "style": style,
                    "fields": ",".join(fields),
                }
            }
        )

    if requests:
        slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
