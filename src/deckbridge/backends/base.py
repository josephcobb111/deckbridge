"""Backend base module.

This module defines the abstract :class:`BaseBackend` class, which provides the
interface that concrete backend implementations (e.g., PowerPoint, Google
Slides) must follow. Subclasses are responsible for rendering a
:class:`deckbridge.deck.deck.Deck` instance to a target format.
"""


class BaseBackend:
    """Abstract base class for deck rendering backends.

    Subclasses must implement the :meth:`render` method, which receives a
    fully‑populated :class:`deckbridge.deck.deck.Deck` object and performs the
    rendering to the desired output (file, API, etc.).
    """

    def render(self, deck):
        """Render the provided ``deck``.

        This method should be overridden by concrete backend implementations.
        The default implementation raises :class:`NotImplementedError` to
        indicate that the subclass must provide its own rendering logic.

        Args:
            deck: The :class:`deckbridge.deck.deck.Deck` instance containing
                slide definitions, layout configurations, and theme settings.
        """
        raise NotImplementedError
