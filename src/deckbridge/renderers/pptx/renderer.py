from importlib import resources

from pptx import Presentation
from pptx.util import Inches

from deckbridge.layouts.registry import LAYOUTS
from deckbridge.renderers.common.slot_renderer import render_slot
from deckbridge.renderers.common.text_renderer import resolve_text_content

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

            for slot_key, slot in slots.items():
                slot_type = slot.get("type")

                # -----------------------
                # Resolve content
                # -----------------------
                if slot_type == "chart":
                    content = slide["content"].get(slot_key)

                elif slot_type == "text":
                    content = resolve_text_content(slide, slot_key)

                else:
                    content = None

                # -----------------------
                # Render
                # -----------------------
                render_slot(
                    backend="pptx",
                    slot_key=slot_key,
                    slot=slot,
                    content=content,
                    slide_obj=s,
                    chart_compiler=self.compiler,
                )

        prs.save(output_path)
