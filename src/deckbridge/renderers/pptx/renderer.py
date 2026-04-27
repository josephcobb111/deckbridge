from importlib import resources

from pptx import Presentation
from pptx.util import Inches

from deckbridge.layouts.registry import LAYOUTS

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
            # =====================================================
            # TITLE SLIDE (leave mostly as-is for now)
            # =====================================================
            if slide["type"] == "title":
                layout = prs.slide_layouts[0]
                s = prs.slides.add_slide(layout)

                s.shapes[0].text_frame.text = slide["title"]
                s.shapes[1].text_frame.text = slide["subtitle"]

            # =====================================================
            # CHART SLIDE (FULL SLOT SYSTEM)
            # =====================================================
            elif slide["type"] == "chart":
                # Use blank layout (we control everything)
                layout = prs.slide_layouts[3]  # blank is safest
                s = prs.slides.add_slide(layout)

                layout_spec = LAYOUTS[slide["layout"]]
                slots = layout_spec.slots

                # -----------------------
                # 1. Slide title
                # -----------------------
                if "slide_title" in slots and slide.get("title"):
                    slot = slots["slide_title"]

                    textbox = s.shapes.add_textbox(
                        Inches(slot["x"]),
                        Inches(slot["y"]),
                        Inches(slot["w"]),
                        Inches(slot["h"]),
                    )

                    textbox.text_frame.text = slide["title"]

                # -----------------------
                # 2. Charts + Chart Titles
                # -----------------------
                for i, block in enumerate(slide["charts"], start=1):
                    chart_slot_key = f"chart_{i}"
                    title_slot_key = f"chart_{i}_title"

                    # --- Chart ---
                    if chart_slot_key not in slots:
                        continue

                    chart_slot = slots[chart_slot_key]

                    x = Inches(chart_slot["x"])
                    y = Inches(chart_slot["y"])
                    cx = Inches(chart_slot["w"])
                    cy = Inches(chart_slot["h"])

                    chart_type, chart_data = self.compiler.compile(block.chart)

                    s.shapes.add_chart(chart_type, x, y, cx, cy, chart_data)

                    # --- Chart Title ---
                    if block.title and title_slot_key in slots:
                        title_slot = slots[title_slot_key]

                        textbox = s.shapes.add_textbox(
                            Inches(title_slot["x"]),
                            Inches(title_slot["y"]),
                            Inches(title_slot["w"]),
                            Inches(title_slot["h"]),
                        )

                        textbox.text_frame.text = block.title

        prs.save(output_path)
