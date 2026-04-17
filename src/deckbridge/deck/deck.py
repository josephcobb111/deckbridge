from ..backends.base import BaseBackend
from .specs import ChartSpec


class Deck:
    def __init__(self):
        self.slides = []

    def add_title_slide(self, title, subtitle=""):
        self.slides.append({"type": "title", "title": title, "subtitle": subtitle})

    def add_chart_slide(self, title, chart_type, data, x, y):
        spec = ChartSpec(chart_type=chart_type, data=data, x=x, y=y, title=title)

        self.slides.append({"type": "chart", "spec": spec})

    def render(self, backend: BaseBackend):
        backend.render(self)
