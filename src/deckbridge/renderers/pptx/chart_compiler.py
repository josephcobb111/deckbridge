from pptx.util import Inches

from deckbridge.renderers.pptx.chart_builder import PPTXChartBuilder


class PPTXChartCompiler:
    """Compile chart specifications into PowerPoint chart objects.

    The :class:`PPTXChartCompiler` orchestrates the creation of a chart shape on a
    slide using :class:`PPTXChartBuilder`. It is responsible for positioning the
    chart on the slide, delegating data construction to the builder, and applying
    theme‑driven styling. The public ``compile`` method is called by the rendering
    pipeline with the rendering context, layout slot, block definition, and an
    identifier for the chart shape.
    """

    def __init__(self):
        self.builder = PPTXChartBuilder()

    def compile(self, ctx, slot, block, chart_key, value_axis_override=None):
        """Compile a chart into a PowerPoint slide.

        Parameters
        ----------
        ctx : RenderContext
            Rendering context containing the slide object and theme information.
        slot : dict
            Dictionary with positional keys ``x``, ``y``, ``w``, ``h`` defining
            the location and size of the chart on the slide (in inches).
        block : Block
            The block definition that includes the chart specification and
            styling overrides.
        chart_key : str
            Identifier used to name the shape on the slide.
        value_axis_override : tuple, optional
            Optional ``(min, max)`` tuple to override the chart's value axis
            range.

        Returns
        -------
        None
            The method adds the chart shape to the slide and applies styling.
        """
        # -----------------------
        # Position
        # -----------------------
        x = Inches(slot["x"])
        y = Inches(slot["y"])
        cx = Inches(slot["w"])
        cy = Inches(slot["h"])

        # -----------------------
        # Build
        # -----------------------
        chart_type, chart_data = self.builder.build_chart_data(block.chart)

        shape = ctx.slide_obj.shapes.add_chart(chart_type, x, y, cx, cy, chart_data)

        try:
            shape.name = chart_key
        except Exception:
            pass

        chart = shape.chart

        # -----------------------
        # Style
        # -----------------------
        self.builder.apply_chart_style(
            chart,
            theme=ctx.theme,
            layout_name=ctx.layout_spec.name,
            block=block,
            value_axis_override=value_axis_override,
        )
