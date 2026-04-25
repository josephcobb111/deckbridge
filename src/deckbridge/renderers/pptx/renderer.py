from importlib import resources

from pptx import Presentation
from pptx.util import Inches

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

                spec = slide["spec"]

                chart_type, chart_data = self.compiler.compile(spec)

                title_box = s.shapes.title
                title_box.text = spec.title

                x, y, cx, cy = Inches(1), Inches(1.5), Inches(8), Inches(4.5)

                chart = s.shapes.add_chart(chart_type, x, y, cx, cy, chart_data).chart

                if spec.title:
                    chart.has_title = True
                    chart.chart_title.text_frame.text = spec.title

        prs.save(output_path)
