"""Utilities for compiling and embedding PowerPoint charts.

This module defines :class:`PPTXChartCompiler`, which orchestrates the creation of
chart shapes on a PowerPoint slide using :class:`~deckbridge.renderers.pptx.chart_builder.PPTXChartBuilder`.
It handles positioning, data building, and theme‑driven styling.
"""

from pptx.util import Inches

from deckbridge.renderers.pptx.chart_builder import PPTXChartBuilder


class PPTXChartCompiler:
    """Compile chart specifications into PowerPoint chart objects.

    This compiler coordinates chart creation on a PowerPoint slide. It positions
    the chart based on the supplied ``slot``, delegates data construction to
    :class:`~deckbridge.renderers.pptx.chart_builder.PPTXChartBuilder`, and applies
    theme‑driven styling. The compiled chart is added to the slide via the
    rendering context.
    """

    def __init__(self):
        """Initializes the PPTXChartCompiler.

        Creates an instance of :class:`PPTXChartBuilder` used for constructing
        chart data and applying styling.
        """
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

        shape.name = chart_key

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
