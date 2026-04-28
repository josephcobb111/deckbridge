from pptx.util import Inches

from deckbridge.renderers.common.text_renderer import render_text_slot


def render_slot(
    backend,
    slot_key,
    slot,
    content,
    *,
    slide_obj=None,
    slides_service=None,
    presentation_id=None,
    page_id=None,
    chart_compiler=None,
):
    slot_type = slot.get("type")

    if slot_type == "chart":
        _render_chart(
            backend,
            slot,
            content,
            chart_key=slot_key,
            slide_obj=slide_obj,
            slides_service=slides_service,
            presentation_id=presentation_id,
            page_id=page_id,
            chart_compiler=chart_compiler,
        )

    elif slot_type == "text":
        _render_text(
            backend=backend,
            slot_key=slot_key,
            slot=slot,
            text=content,
            slide_obj=slide_obj,
            slides_service=slides_service,
            presentation_id=presentation_id,
            page_id=page_id,
        )

    else:
        raise ValueError(f"Unsupported slot type: {slot_type}")


def _render_chart(
    backend,
    slot,
    block,
    *,
    chart_key=None,
    slide_obj=None,
    slides_service=None,
    presentation_id=None,
    page_id=None,
    chart_compiler=None,
):
    if not block:
        return

    if backend == "pptx":
        x = Inches(slot["x"])
        y = Inches(slot["y"])
        cx = Inches(slot["w"])
        cy = Inches(slot["h"])

        chart_type, chart_data = chart_compiler.compile(block.chart)

        slide_obj.shapes.add_chart(chart_type, x, y, cx, cy, chart_data)

    elif backend == "gslides":
        chart_compiler.compile(
            presentation_id=presentation_id,
            page_id=page_id,
            spec=block.chart,
            position=slot,
            chart_key=chart_key,
        )


def _render_text(
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

    render_text_slot(
        backend=backend,
        slot_key=slot_key,
        slot=slot,
        text=text,
        slide_obj=slide_obj,
        slides_service=slides_service,
        presentation_id=presentation_id,
        page_id=page_id,
    )
