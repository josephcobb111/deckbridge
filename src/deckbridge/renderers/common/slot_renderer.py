from pptx.util import Inches

from deckbridge.renderers.common.legend_renderer import render_dash_legend
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
            _render_chart(ctx, slot, block, slot_key)

        elif slot_type == "text":
            text = resolve_text_content(slide, slot_key, slot)
            _render_text(ctx, slot, text, slot_key)

        elif slot_type == "legend":
            render_dash_legend(ctx, slot_key, slot, slide)


def _render_chart(ctx, slot, block, slot_key):
    if not block:
        return

    ctx.chart_compiler.compile(ctx, slot, block, slot_key)


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
