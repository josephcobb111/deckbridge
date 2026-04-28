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
            # Use blank layout
            layout = prs.slide_layouts[3]  # blank is safest
            s = prs.slides.add_slide(layout)

            layout_spec = LAYOUTS[slide["layout"]]

            # -----------------------
            # Charts
            # -----------------------
            slots = layout_spec.slots

            for i, block in enumerate(slide["charts"], start=1):
                chart_slot_key = f"chart_{i}"

                if chart_slot_key in slots:
                    chart_slot = slots[chart_slot_key]

                    x = Inches(chart_slot["x"])
                    y = Inches(chart_slot["y"])
                    cx = Inches(chart_slot["w"])
                    cy = Inches(chart_slot["h"])

                    chart_type, chart_data = self.compiler.compile(block.chart)

                    s.shapes.add_chart(chart_type, x, y, cx, cy, chart_data)

            # -----------------------
            # Titles (text boxes)
            # -----------------------
            text_map = {
                "deck_title": slide.get("deck_title"),
                "deck_author": slide.get("deck_author"),
                "slide_title": slide.get("slide_title"),
            }

            # Chart titles (from ChartBlock)
            for i, block in enumerate(slide["charts"], start=1):
                if block.title:
                    text_map[f"chart_{i}_title"] = block.title

            render_text_slots(
                backend="pptx",
                slide_obj=s,
                layout_spec=layout_spec,
                text_map=text_map,
            )

        prs.save(output_path)
