from importlib import resources

from pptx import Presentation

from deckbridge.layouts.registry import LAYOUTS
from deckbridge.renderers.common.context import RenderContext
from deckbridge.renderers.common.slot_renderer import render_slots

from .chart_compiler import PPTXChartCompiler


def get_default_template_path():
    return str(resources.files("deckbridge.templates").joinpath("default.pptx"))


class PPTXRenderer:
    def __init__(self, template_path=None):
        self.compiler = PPTXChartCompiler()
        self.template_path = template_path or get_default_template_path()

    def render(self, deck, output_path):
        prs = Presentation(self.template_path)

        for slide in deck.slides:
            s = prs.slides.add_slide(prs.slide_layouts[3])

            layout_spec = LAYOUTS[slide["layout"]]

            ctx = RenderContext(
                backend="pptx",
                slide_obj=s,
                layout_spec=layout_spec,
                chart_compiler=self.compiler,
            )

            render_slots(ctx, slide)

        prs.save(output_path)
