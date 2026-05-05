from ..backends.base import BaseBackend


class Deck:
    def __init__(self):
        self.slides = []

    def add_slide(self, layout=None, deck_title=None, deck_author=None, slide_title=None, content=None, notes=None):
        if layout is None:
            layout = self._infer_layout(content)

        self.slides.append(
            {
                "layout": layout,
                "deck_title": deck_title,
                "deck_author": deck_author,
                "slide_title": slide_title,
                "content": content or [],
                "notes": notes,
            }
        )

    def _infer_layout(self, content):
        if not content:
            return "title_slide"

        n = len(content)  # assumes charts are only content for now

        if n == 1:
            return "one_chart"
        elif n == 2:
            return "two_chart"
        elif n == 3:
            return "three_chart"

        raise ValueError(f"No default layout for {n} charts")

    def render(self, backend: BaseBackend):
        backend.render(self)
