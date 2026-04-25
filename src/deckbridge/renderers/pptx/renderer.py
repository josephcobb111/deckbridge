from pptx import Presentation
from pptx.util import Inches

from .chart_compiler import PPTXChartCompiler


class PPTXRenderer:
    def __init__(self):
        self.compiler = PPTXChartCompiler()

    def render(self, deck, output_path: str):
        prs = Presentation()

        for slide in deck.slides:
            # -----------------------
            # Title slide
            # -----------------------
            if slide["type"] == "title":
                layout = prs.slide_layouts[0]
                s = prs.slides.add_slide(layout)

                s.shapes.title.text = slide["title"]
                s.placeholders[1].text = slide["subtitle"]

            # -----------------------
            # Chart slide (NATIVE)
            # -----------------------
            elif slide["type"] == "chart":
                layout = prs.slide_layouts[5]
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
