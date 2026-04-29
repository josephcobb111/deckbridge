from pptx.util import Inches

from deckbridge.renderers.common.text_renderer import render_text_slot, resolve_text_content


def render_slots(ctx, slide):
    slots = ctx.layout_spec.slots

    for slot_key, slot in slots.items():
        slot_type = slot.get("type")

        # -----------------------
        # Resolve content
        # -----------------------
        if slot_type == "chart":
            block = slide["content"].get(slot_key)
            _render_chart(ctx, slot, block, chart_key=slot_key)

        elif slot_type == "text":
            content = resolve_text_content(slide, slot_key, slot)
            _render_text(ctx, slot, content, slot_key)


def _render_chart(ctx, slot, block, chart_key):
    if not block:
        return

    if ctx.backend == "pptx":
        x = Inches(slot["x"])
        y = Inches(slot["y"])
        cx = Inches(slot["w"])
        cy = Inches(slot["h"])

        chart_type, chart_data = ctx.chart_compiler.compile(block.chart)

        shape = ctx.slide_obj.shapes.add_chart(chart_type, x, y, cx, cy, chart_data)

        try:
            shape.name = chart_key
        except Exception:
            pass

    elif ctx.backend == "gslides":
        ctx.chart_compiler.compile(
            presentation_id=ctx.presentation_id,
            page_id=ctx.page_id,
            spec=block.chart,
            position=slot,
            chart_key=chart_key,
        )


def _render_text(ctx, slot, text, slot_key):
    render_text_slot(
        backend=ctx.backend,
        slot_key=slot_key,
        slot=slot,
        text=text,
        slide_obj=ctx.slide_obj,
        slides_service=ctx.slides_service,
        presentation_id=ctx.presentation_id,
        page_id=ctx.page_id,
    )
