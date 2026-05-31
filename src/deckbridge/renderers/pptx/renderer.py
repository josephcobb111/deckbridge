from importlib import resources

from pptx import Presentation

from deckbridge.renderers.common.context import RenderContext
from deckbridge.renderers.common.slot_renderer import render_slots
from deckbridge.renderers.pptx.chart_compiler import PPTXChartCompiler


def get_default_template_path():
    """Return the absolute path to the bundled default PPTX template.

    The function locates ``deckbridge/templates/default.pptx`` using
    :mod:`importlib.resources` and returns it as a string suitable for passing to
    :class:`pptx.Presentation`.  This path is used when the user does not supply a
    custom template to :class:`PPTXRenderer`.
    """
    return str(resources.files("deckbridge.templates").joinpath("default.pptx"))


class PPTXRenderer:
    """Renderer for converting a Deckbridge deck into a PowerPoint presentation.

    The renderer uses a PPTX template (default or user‑provided) and a
    :class:`PPTXChartCompiler` to translate chart specifications into native
    ``pptx`` chart objects.  Layout specifications are looked up via
    ``self.layouts`` and styling/theme information via ``self.theme`` – both are
    expected to be populated by the caller before :meth:`render` is invoked.

    Typical workflow:

    1. Instantiate the renderer, optionally passing a custom template path.
    2. Assign ``self.layouts`` (a mapping of layout names to layout specs) and
       ``self.theme`` (a theme configuration used by the slot renderer).
    3. Call :meth:`render` with a deck object and an output file path to produce
       the final ``.pptx`` file.

    The class is deliberately lightweight; most of the heavy lifting is
    delegated to :func:`render_slots` and the chart compiler.
    """

    def __init__(self, template_path=None):
        """Create a PPTXRenderer.

        Args:
            template_path (str, optional): Path to a PPTX file to use as the
                presentation template. If omitted, the default template
                bundled with the package (``deckbridge.templates.default.pptx``)
                is used.

        The constructor initializes a :class:`PPTXChartCompiler` for converting
        chart specifications into ``pptx`` chart objects and stores the resolved
        template path. Theme and layout information are expected to be set on the
        instance by the caller before invoking :meth:`render`.
        """
        self.compiler = PPTXChartCompiler()
        self.template_path = template_path or get_default_template_path()

    def render(self, deck, output_path):
        """Render a Deckbridge deck to a PowerPoint file.

        This method creates a new :class:`pptx.presentation.Presentation` from the
        configured template, iterates over the deck's slides, and populates each
        slide using the appropriate layout specification and theme.  For each
        slide a rendering context is constructed and passed to the common slot
        renderer which fills in text, images and charts.  Finally the completed
        presentation is written to ``output_path``.

        Args:
            deck: A :class:`deckbridge.deck.Deck` (or compatible mapping) that
                contains a ``slides`` sequence. Each slide entry must provide a
                ``layout`` key used to look up ``self.layouts``.
            output_path: Path (str or :class:`pathlib.Path`) where the generated
                ``.pptx`` file should be saved.
        """
        prs = Presentation(self.template_path)

        for slide in deck.slides:
            s = prs.slides.add_slide(prs.slide_layouts[3])

            layout_spec = self.layouts[slide["layout"]]

            ctx = RenderContext(
                backend="pptx",
                slide_obj=s,
                layout_spec=layout_spec,
                chart_compiler=self.compiler,
                theme=self.theme,
            )

            render_slots(ctx, slide)

        prs.save(output_path)
