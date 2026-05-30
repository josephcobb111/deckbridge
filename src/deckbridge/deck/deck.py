from deckbridge.layouts.registry import LAYOUTS
from deckbridge.themes.default import THEME

from deckbridge.backends.base import BaseBackend


class DeckConfig:
    def __init__(
        self,
        theme=None,
        layouts=None,
        pptx_template=None,
        gslides_template=None,
    ):

        self.theme = theme or THEME
        self.layouts = layouts or LAYOUTS

        self.pptx_template = pptx_template
        self.gslides_template = gslides_template


class Deck:
    def __init__(self, *, config=None):
        self.config = config or DeckConfig()
        self.slides = []

    def add_slide(
        self,
        layout=None,
        deck_title=None,
        deck_author=None,
        slide_title=None,
        content=None,
        color_legend=None,
        dash_legend=None,
        sync_value_axis=None,
        notes=None,
    ):
        if layout is None:
            layout = self._infer_layout(content)

        self.slides.append(
            {
                "layout": layout,
                "deck_title": deck_title,
                "deck_author": deck_author,
                "slide_title": slide_title,
                "content": content or [],
                "color_legend": color_legend or [],
                "dash_legend": dash_legend or [],
                "sync_value_axis": sync_value_axis or (),
                "notes": notes,
            }
        )

    def _infer_layout(self, content):
        if not content:
            return "title_slide"

        n = len([_item for _item in content if "chart" in _item])

        if n == 1:
            return "one_chart"
        elif n == 2:
            return "two_chart"
        elif n == 3:
            return "three_chart"

        raise ValueError(f"No default layout for {n} charts")

    def render(self, backend: BaseBackend):
        backend.render(self)
