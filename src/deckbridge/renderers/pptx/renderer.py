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
            # -----------------------
            # Title slide
            # -----------------------
            if slide["type"] == "title":
                layout = prs.slide_layouts[0]
                s = prs.slides.add_slide(layout)

                s.shapes[0].text_frame.text = slide["title"]
                s.shapes[1].text_frame.text = slide["subtitle"]

            # -----------------------
            # Chart slide (NATIVE)
            # -----------------------
            elif slide["type"] == "chart":
                layout = prs.slide_layouts[2]
                s = prs.slides.add_slide(layout)

                title_box = s.shapes.title
                title_box.text = slide["title"]

                layout_spec = LAYOUTS[slide["layout"]]

                for i, spec in enumerate(slide["charts"]):
                    slot = list(layout_spec.slots.values())[i]

                    x = Inches(slot["x"])
                    y = Inches(slot["y"])
                    cx = Inches(slot["w"])
                    cy = Inches(slot["h"])

                    chart_type, chart_data = self.compiler.compile(spec)

                    chart = s.shapes.add_chart(chart_type, x, y, cx, cy, chart_data).chart

                    if spec.title:
                        chart.has_title = True
                        chart.chart_title.text_frame.text = spec.title

        prs.save(output_path)
