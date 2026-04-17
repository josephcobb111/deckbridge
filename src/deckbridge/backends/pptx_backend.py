from ..renderers.pptx.renderer import PPTXRenderer
from .base import BaseBackend


class PPTXBackend(BaseBackend):
    def __init__(self, output_path="output.pptx"):
        self.output_path = output_path

    def render(self, deck):
        PPTXRenderer().render(deck, self.output_path)
