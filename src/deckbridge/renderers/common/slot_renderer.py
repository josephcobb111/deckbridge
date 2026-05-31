from deckbridge.renderers.common.axis_resolver import resolve_shared_axis_ranges
from deckbridge.renderers.common.legend_renderer import render_color_legend, render_dash_legend
from deckbridge.renderers.common.text_renderer import render_text_slot, resolve_text_content


def render_slots(ctx, slide):
    """Render all slots for a given slide using the layout specification.

    Iterates over each slot defined in ``ctx.layout_spec.slots`` and dispatches
    rendering based on the slot ``type``. Supported slot types are:

    - ``"chart"`` – renders a chart block via ``_render_chart``.
    - ``"text"`` – resolves text content and renders it via ``_render_text``.
    - ``"color_legend"`` – renders a color legend using ``render_color_legend``.
    - ``"dash_legend"`` – renders a dash legend using ``render_dash_legend``.

    Args:
        ctx: Rendering context providing layout specifications, theme, and
            backend helpers.
        slide (dict): Slide definition containing a ``"content"`` mapping of
            block identifiers to block objects.

    Returns:
        None. Rendering functions modify the context or output objects in‑place.
    """
    slots = ctx.layout_spec.slots

    for slot_key, slot in slots.items():
        slot_type = slot.get("type")

        # -----------------------
        # Resolve content
        # -----------------------
        if slot_type == "chart":
            block = slide["content"].get(slot_key)
            _render_chart(ctx, slot, block, slot_key, slide)

        elif slot_type == "text":
            text, style_overrides = resolve_text_content(slide, slot_key, slot)
            _render_text(ctx, slot, text, slot_key, style_overrides)

        elif slot_type == "color_legend":
            render_color_legend(ctx, slot_key, slot, slide)

        elif slot_type == "dash_legend":
            render_dash_legend(ctx, slot_key, slot, slide)


def _render_chart(ctx, slot, block, slot_key, slide):
    """Render a chart block into the slide.

    If ``block`` is ``None`` the function returns early. Otherwise it resolves any
    shared axis ranges across the slide and delegates to the ``chart_compiler``
    in the rendering context to produce the chart output.

    Args:
        ctx: Rendering context containing the chart compiler and other helpers.
        slot (dict): Slot definition describing the chart placement and size.
        block (object): Chart block instance with data and styling information.
        slot_key (str): Identifier for the slot, used for logging or lookup.
        slide (dict): Full slide definition, potentially needed for shared axis
            resolution.

    Returns:
        None. The chart is added to the context's output structures.
    """
    if not block:
        return

    shared_axis = resolve_shared_axis_ranges(slide)
    ctx.chart_compiler.compile(ctx, slot, block, slot_key, shared_axis)


def _render_text(ctx, slot, text, slot_key, style_overrides=None):
    render_text_slot(ctx, slot, text, slot_key, style_overrides)
