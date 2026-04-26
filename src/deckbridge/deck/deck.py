from ..backends.base import BaseBackend
from .specs import ChartSpec


class Deck:
    def __init__(self):
        self.slides = []

    def add_title_slide(self, title, subtitle=""):
        self.slides.append({"type": "title", "title": title, "subtitle": subtitle})

    def add_chart_slide(self, title, layout, charts):
        self.slides.append({"type": "chart", "title": title, "layout": layout, "charts": charts})

    def render(self, backend: BaseBackend):
        backend.render(self)
