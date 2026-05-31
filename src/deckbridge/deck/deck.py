"""Deck module for building presentation decks.

This module provides a simple API for constructing a deck of slides and
rendering them with a backend implementation. It defines configuration
objects, a ``Deck`` container class, and helper methods for slide creation
and layout inference.
"""

from deckbridge.backends.base import BaseBackend
from deckbridge.layouts.registry import LAYOUTS
from deckbridge.themes.default import THEME


class DeckConfig:
    """Configuration holder for a :class:`Deck`.

    Attributes:
        theme: The theme object used for styling the deck. If ``None`` is
            provided, the default theme ``THEME`` is used.
        layouts: Mapping of layout identifiers to layout specifications. If
            ``None`` is provided, the global ``LAYOUTS`` registry is used.
        pptx_template: Optional path to a PowerPoint template file.
        gslides_template: Optional path to a Google Slides template file.
    """

    def __init__(
        self,
        theme=None,
        layouts=None,
        pptx_template=None,
        gslides_template=None,
    ):
        """Create a new :class:`DeckConfig` instance.

        Args:
            theme: Theme instance or ``None`` to use the default.
            layouts: Dictionary of layout specifications or ``None`` to use the
                built‑in ``LAYOUTS`` registry.
            pptx_template: Path to a PowerPoint template file.
            gslides_template: Path to a Google Slides template file.
        """
        self.theme = theme or THEME
        self.layouts = layouts or LAYOUTS
        self.pptx_template = pptx_template
        self.gslides_template = gslides_template


class Deck:
    """Container for a collection of slides.

    A ``Deck`` object holds a list of slide dictionaries and delegates the
    rendering step to a concrete ``BaseBackend`` implementation.
    """

    def __init__(self, *, config=None):
        """Initialize a new deck.

        Args:
            config: Optional :class:`DeckConfig` instance. If omitted, a default
                configuration is created.
        """
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
        """Add a slide definition to the deck.

        The slide is stored as a dictionary that later renderers understand.

        Args:
            layout: Identifier of the layout to use. If ``None``, a layout is
                inferred from the ``content`` using :meth:`_infer_layout`.
            deck_title: Title of the overall deck (optional).
            deck_author: Author name for the deck (optional).
            slide_title: Title for the individual slide (optional).
            content: List of slide content items. If omitted an empty list is
                used.
            color_legend: List of colour legend entries; defaults to an empty
                list.
            dash_legend: List of dash legend entries; defaults to an empty
                list.
            sync_value_axis: Tuple of axes to synchronise across charts;
                defaults to an empty tuple.
            notes: Optional speaker notes for the slide.
        """
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
        """Infer a default layout based on the number of charts in ``content``.

        The function looks for items containing a ``"chart"`` key and selects a
        layout name accordingly. Supported defaults are ``"title_slide"`` for
        empty content, ``"one_chart"``, ``"two_chart"`` and ``"three_chart"``.

        Args:
            content: List of content dictionaries for a slide.

        Returns:
            A string naming the inferred layout.

        Raises:
            ValueError: If the number of chart items does not match a known
                default layout.
        """
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
        """Render the deck using the supplied backend.

        Args:
            backend: An instance of a subclass of :class:`BaseBackend` that
                implements the ``render`` method.
        """
        backend.render(self)
