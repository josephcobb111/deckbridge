from ..renderers.pptx.renderer import PPTXRenderer
from .base import BaseBackend


class PPTXBackend(BaseBackend):
    def __init__(self, output_path="output.pptx", template_path=None):
        self.output_path = output_path
        self.template_path = template_path

    def render(self, deck):
        PPTXRenderer(template_path=self.template_path).render(deck, self.output_path)
