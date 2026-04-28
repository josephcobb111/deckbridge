from importlib import resources

from pptx import Presentation
from pptx.util import Inches

from deckbridge.layouts.registry import LAYOUTS
from deckbridge.renderers.common.text_renderer import render_text_slots

from .chart_compiler import PPTXChartCompiler


def get_default_template_path():
    return str(resources.files("deckbridge.templates").joinpath("default.pptx"))


class PPTXRenderer:
    def __init__(self, template_path=None):
        self.compiler = PPTXChartCompiler()
        self.template_path = template_path or get_default_template_path()

    def render(self, deck, output_path: str):
        prs = Presentation(self.template_path)

        for slide in deck.slides:
            layout = prs.slide_layouts[3]  # blank
            s = prs.slides.add_slide(layout)

            layout_spec = LAYOUTS[slide["layout"]]
            slots = layout_spec.slots

            text_map = {}

            # -----------------------
            # Global text fields
            # -----------------------
            for key in ["deck_title", "deck_author", "slide_title"]:
                if slide.get(key):
                    text_map[key] = slide[key]

            # -----------------------
            # Slot-driven rendering
            # -----------------------
            for slot_key, slot in slots.items():
                # -----------------------
                # Chart slots
                # -----------------------
                if slot["type"] == "chart":
                    block = slide["content"].get(slot_key)
                    if not block:
                        continue

                    # Render chart
                    chart_slot = slots[slot_key]

                    x = Inches(chart_slot["x"])
                    y = Inches(chart_slot["y"])
                    cx = Inches(chart_slot["w"])
                    cy = Inches(chart_slot["h"])

                    chart_type, chart_data = self.compiler.compile(block.chart)

                    s.shapes.add_chart(chart_type, x, y, cx, cy, chart_data)

                    # Add chart title to text_map
                    if getattr(block, "chart_title", None):
                        text_map[f"{slot_key}_title"] = block.chart_title

            # -----------------------
            # Render all text slots
            # -----------------------
            render_text_slots(
                backend="pptx",
                slide_obj=s,
                layout_spec=layout_spec,
                text_map=text_map,
            )

        prs.save(output_path)
