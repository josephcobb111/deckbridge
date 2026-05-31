"""PowerPoint backend for rendering decks.

This module implements :class:`PPTXBackend`, a concrete subclass of
:class:`deckbridge.backends.base.BaseBackend` that renders a deck to a
PowerPoint ``.pptx`` file using the :class:`deckbridge.renderers.pptx.renderer.PPTXRenderer`.
"""

from deckbridge.backends.base import BaseBackend
from deckbridge.renderers.pptx.renderer import PPTXRenderer


class PPTXBackend(BaseBackend):
    """Backend that writes a deck to a PowerPoint file.

    The backend delegates the heavy lifting to :class:`PPTXRenderer`, which
    knows how to translate deck structures (layouts, themes, content blocks)
    into the PowerPoint format.
    """

    def __init__(self, output_path: str = "output.pptx", template_path: str | None = None):
        """Create a new :class:`PPTXBackend` instance.

        Args:
            output_path: Destination file path for the generated ``.pptx`` file.
                Defaults to ``"output.pptx"`` in the current working directory.
            template_path: Optional path to a PowerPoint template file that
                provides predefined slide masters and styles. If ``None`` the
                renderer uses its built‑in defaults.
        """
        self.output_path = output_path
        self.template_path = template_path

    def render(self, deck):
        """Render the supplied ``deck`` to a PowerPoint file.

        The method creates a :class:`PPTXRenderer`, configures it with the deck's
        theme and layout registry, and then calls its ``render`` method to produce
        the output file.

        Args:
            deck: An instance of :class:`deckbridge.deck.deck.Deck` containing the
                slide definitions and configuration.
        """
        renderer = PPTXRenderer(template_path=self.template_path)
        renderer.theme = deck.config.theme
        renderer.layouts = deck.config.layouts

        renderer.render(deck, self.output_path)
