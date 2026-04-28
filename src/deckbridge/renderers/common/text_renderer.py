from pptx.util import Inches

from deckbridge.renderers.gslides.utils import inches_to_emu


def render_text_slots(
    backend: str,
    slide_obj,
    layout_spec,
    text_map: dict,
    slides_service=None,
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

    if requests:
        slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
