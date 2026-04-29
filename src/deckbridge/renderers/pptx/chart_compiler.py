from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Inches, Pt

from deckbridge.utils import deep_merge

from .chart_builder import PPTXChartBuilder


class PPTXChartCompiler:
    def __init__(self):
        self.builder = PPTXChartBuilder()

    def compile(self, ctx, slot, block, chart_key):
        # -----------------------
        # Position
        # -----------------------
        x = Inches(slot["x"])
        y = Inches(slot["y"])
        cx = Inches(slot["w"])
        cy = Inches(slot["h"])

        # -----------------------
        # Build
        # -----------------------
        chart_type, chart_data = self.builder.build_chart_data(block.chart)

        shape = ctx.slide_obj.shapes.add_chart(chart_type, x, y, cx, cy, chart_data)

        try:
            shape.name = chart_key
        except Exception:
            pass

        chart = shape.chart

        # -----------------------
        # Style
        # -----------------------
        self.builder.apply_chart_style(
            chart,
            theme=ctx.theme,
            layout_name=ctx.layout_spec.name,
        )
