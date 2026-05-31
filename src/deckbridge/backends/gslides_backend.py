"""Google Slides backend for rendering decks.

This module provides :class:`GSlidesBackend`, a concrete implementation of
:class:`deckbridge.backends.base.BaseBackend` that renders a deck directly into a
Google Slides presentation using the :class:`deckbridge.renderers.gslides.renderer.GSlidesRenderer`.
"""

from deckbridge.backends.base import BaseBackend
from deckbridge.renderers.gslides.renderer import GSlidesRenderer


class GSlidesBackend(BaseBackend):
    """Backend that writes a deck to a Google Slides presentation.

    The backend constructs a :class:`GSlidesRenderer` with the required Google
    service objects and delegates rendering of the deck to it.
    """

    def __init__(
        self,
        presentation_id: str,
        spreadsheet_id: str,
        slides_service,
        sheets_service,
        execute_requests: bool = True,
    ):
        """Create a new :class:`GSlidesBackend` instance.

        Args:
            presentation_id: The ID of the Google Slides presentation to which
                the deck will be rendered.
            spreadsheet_id: The ID of the Google Sheets spreadsheet used for
                data-driven charts.
            slides_service: Authenticated Google Slides API service object.
            sheets_service: Authenticated Google Sheets API service object.
            execute_requests: If ``True`` (default), the renderer will execute
                batch update requests against the Google APIs. Setting this to
                ``False`` can be useful for dry‑run testing.
        """
        self.presentation_id = presentation_id
        self.spreadsheet_id = spreadsheet_id
        self.slides_service = slides_service
        self.sheets_service = sheets_service

        self.renderer = GSlidesRenderer(
            slides_service=slides_service,
            sheets_service=sheets_service,
            spreadsheet_id=spreadsheet_id,
            presentation_id=presentation_id,
            execute_requests=execute_requests,
        )

    def render(self, deck):
        """Render the supplied ``deck`` into the target Google Slides presentation.

        The method configures the underlying renderer with the deck's theme and
        layout registry before invoking its ``render`` method.

        Args:
            deck: An instance of :class:`deckbridge.deck.deck.Deck` containing the
                slides, layouts, and theme to be rendered.
        """
        self.renderer.theme = deck.config.theme
        self.renderer.layouts = deck.config.layouts

        self.renderer.render(deck)
