"""Utilities for building and styling PowerPoint charts.

This module provides :class:`PPTXChartBuilder` which constructs chart data
structures from a chart specification and applies theme‑driven styling to the
resulting :class:`pptx.chart.chart.Chart` objects.
"""

from pptx.chart.data import CategoryChartData, XyChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION
from pptx.util import Pt

from deckbridge.renderers.common.style_resolver import (
    resolve_chart_theme,
    resolve_series_color,
    resolve_series_dash,
    resolve_series_width,
)
from deckbridge.renderers.pptx.utils import PPTX_DASH_MAP, _validate_xy_numeric, hex_to_rgb255


class PPTXChartBuilder:
    """Builder for PowerPoint chart data and styling.

    This class creates chart data structures from a chart specification and
    applies theme‑driven styling to the resulting :class:`pptx.chart.chart.Chart`
    objects. It is used by the PPTX rendering pipeline to embed charts into a
    presentation.
    """

    def build_chart_data(self, spec):
        """Build chart type + data (no styling here)."""
        chart_data = self._build_chart_data(spec)
        chart_type = self._map_chart_type(spec.chart_type)

        return chart_type, chart_data

    def apply_chart_style(self, chart, theme, layout_name, block, value_axis_override):
        """Apply theme-driven styling to a chart object."""
        chart_theme = resolve_chart_theme(theme, layout_name, block.style_overrides)

        self._single_series_bar_chart(chart)
        self._set_chart_title(chart, chart_theme, block)
        self._set_chart_subtitle(chart, chart_theme, block)
        self._set_axis_title(chart, chart_theme, "value_axis", block.value_axis_title)
        self._set_axis_title(chart, chart_theme, "category_axis", block.category_axis_title)
        self._apply_legend_style(chart, chart_theme)
        self._turn_gridlines_off(chart)
        self._category_tick_label_low(chart)
        self._apply_axis_style(chart, chart_theme, block, value_axis_override)
        self._set_data_labels(chart, chart_theme, block)
        self._set_series_colors(chart, chart_theme, block)
        self._set_series_dashes(chart, chart_theme, block)
        self._set_series_line_width(chart, chart_theme, block)
        self._no_lines_scatter_chart(chart)

    def _build_chart_data(self, spec):
        """Construct chart data based on the specification.

        This method creates a :class:`CategoryChartData` or :class:`XyChartData`
        instance depending on the chart type. It populates the data series from
        the pandas ``DataFrame`` provided in ``spec.data``.

        Args:
            spec: Chart specification object containing ``chart_type``, ``x``,
                ``series`` and ``data`` attributes.

        Returns:
            A populated chart data object suitable for the Slides API.
        """
        if spec.chart_type == "scatter":
            chart_data = XyChartData()

            x_values = list(spec.data[spec.x])

            for s in spec.series:
                y_values = list(spec.data[s["column"]])
                _validate_xy_numeric(x_values, y_values, spec.x, s["column"])
                series = chart_data.add_series(s["name"])

                for x, y in zip(x_values, y_values):
                    series.add_data_point(x, y)
        else:
            chart_data = CategoryChartData()

            categories = list(spec.data[spec.x])
            chart_data.categories = categories

            for s in spec.series:
                values = list(spec.data[s["column"]])
                chart_data.add_series(s["name"], values)

        return chart_data

    def _map_chart_type(self, chart_type):
        """Map a chart type string to a ``pptx`` ``XL_CHART_TYPE``.

        The function translates the library‑agnostic chart type identifiers used in
        the specification (e.g. ``"line"``, ``"bar"``) to the corresponding enum
        values from ``pptx.enum.chart.XL_CHART_TYPE``. A ``ValueError`` is raised for
        unsupported types.

        Args:
            chart_type (str): The chart type identifier from the spec.

        Returns:
            XL_CHART_TYPE: The matching enum value.
        """
        mapping = {
            "line": XL_CHART_TYPE.LINE,
            "bar": XL_CHART_TYPE.COLUMN_CLUSTERED,
            "area_stacked": XL_CHART_TYPE.AREA_STACKED,
            "area_stacked_100": XL_CHART_TYPE.AREA_STACKED_100,
            "bar_stacked": XL_CHART_TYPE.BAR_STACKED,
            "column_stacked": XL_CHART_TYPE.COLUMN_STACKED,
            "scatter": XL_CHART_TYPE.XY_SCATTER_SMOOTH,
        }

        if chart_type not in mapping:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        return mapping[chart_type]

    def _single_series_bar_chart(self, chart):
        """Configure bar charts with a single series to not vary by categories.

        For bar charts that contain only one data series, the default behavior of
        ``pptx`` varies the color by category. This method disables that so the
        single series uses a uniform style.

        Args:
            chart: The ``pptx`` chart object to modify.
        """
        if chart.chart_type == self._map_chart_type("bar") and len(chart.plots[0].series) == 1:
            chart.plots[0].vary_by_categories = False

    def _no_lines_scatter_chart(self, chart):
        """Hide line elements for scatter charts.

        In a smooth scatter chart the individual series are represented by markers
        rather than connecting lines. This method disables any line drawing and
        clears the line fill to avoid rendering stray lines.

        Args:
            chart: The ``pptx`` chart object to modify.
        """
        if chart.chart_type == self._map_chart_type("scatter"):
            for s in chart.series:
                s.format.line.visible = False
                s.format.line.fill.background()

    def _set_chart_title(self, chart, chart_theme, block):
        """Apply title styling to the chart.

        If the theme indicates a title should be displayed, this method enables the
        title, sets its text from ``block.chart_title`` and applies size, weight,
        and decoration based on the theme configuration.

        Args:
            chart: The ``pptx`` chart object to modify.
            chart_theme: Resolved theme dictionary containing ``chart_title`` settings.
            block: The layout block providing the ``chart_title`` string.
        """
        if chart_theme["chart_title"]["has_title"]:
            chart.has_title = True
            chart_title = chart.chart_title.text_frame.paragraphs[0]
            chart_title.text = block.chart_title
            chart_title.font.size = Pt(chart_theme["chart_title"]["font_size"])
            chart_title.font.bold = chart_theme["chart_title"]["bold"]
            chart_title.font.italic = chart_theme["chart_title"]["italic"]
            chart_title.font.underline = chart_theme["chart_title"]["underline"]
        else:
            chart.has_title = False

    def _set_chart_subtitle(self, chart, chart_theme, block):
        """Apply subtitle styling when both title and subtitle are enabled.

        The subtitle appears as a second paragraph in the chart title text frame.
        It inherits its content from ``block.chart_subtitle`` and receives styling
        (size, weight, italic, underline) from the resolved theme configuration.

        Args:
            chart: The ``pptx`` chart object to modify.
            chart_theme: Theme dictionary containing ``chart_subtitle`` settings.
            block: The layout block providing the ``chart_subtitle`` string.
        """
        if chart_theme["chart_title"]["has_title"] and chart_theme["chart_subtitle"]["has_title"]:
            chart.chart_title.text_frame.add_paragraph()
            chart_subtitle = chart.chart_title.text_frame.paragraphs[1]
            chart_subtitle.text = block.chart_subtitle
            for run in chart_subtitle.runs:
                run.font.size = Pt(chart_theme["chart_subtitle"]["font_size"])
                run.font.bold = chart_theme["chart_subtitle"]["bold"]
                run.font.italic = chart_theme["chart_subtitle"]["italic"]
                run.font.underline = chart_theme["chart_subtitle"]["underline"]

    def _set_axis_title(self, chart, chart_theme, axis, axis_title):
        """Apply title and formatting to a chart axis.

        Sets the axis title text and styling based on the resolved theme. If the
        theme indicates no title, the axis title is disabled. Tick label font size
        is also set according to the theme.

        Args:
            chart: The ``pptx`` chart object.
            chart_theme: Theme dictionary containing axis configuration.
            axis (str): Either ``"value_axis"`` or ``"category_axis"``.
            axis_title (str): Title text to display on the axis.
        """
        axis_theme = chart_theme.get(axis, {})

        if axis == "value_axis":
            axis_obj = chart.value_axis
        elif axis == "category_axis":
            axis_obj = chart.category_axis

        axis_obj.has_title = axis_theme["has_title"]
        if axis_theme["has_title"] and axis_title:
            axis_obj.axis_title.text_frame.text = axis_title

            for paragraph in axis_obj.axis_title.text_frame.paragraphs:
                paragraph.font.size = Pt(axis_theme["font_size"])
                paragraph.font.bold = axis_theme["bold"]
                paragraph.font.italic = axis_theme["italic"]
                paragraph.font.underline = axis_theme["underline"]
        else:
            axis_obj.has_title = False

        axis_obj.tick_labels.font.size = Pt(axis_theme["font_size"])

    def _apply_legend_style(self, chart, chart_theme):
        """Configure the chart legend based on theme settings.

        Enables or disables the legend, sets its position, and applies font size
        according to the provided ``chart_theme``. When the legend is hidden the
        method returns early.

        Args:
            chart: The ``pptx`` chart object.
            chart_theme: Theme dictionary containing ``legend`` configuration.
        """
        legend_theme = chart_theme.get("legend", {})

        chart.has_legend = legend_theme["visible"]
        if not legend_theme["visible"]:
            return

        chart.legend.include_in_layout = False

        if "position" in legend_theme:
            position_map = {
                "BOTTOM": XL_LEGEND_POSITION.BOTTOM,
                "RIGHT": XL_LEGEND_POSITION.RIGHT,
                "LEFT": XL_LEGEND_POSITION.LEFT,
                "TOP": XL_LEGEND_POSITION.TOP,
            }

            chart.legend.position = position_map.get(legend_theme["position"], XL_LEGEND_POSITION.BOTTOM)

        if "font_size" in legend_theme:
            chart.legend.font.size = Pt(legend_theme["font_size"])

    def _turn_gridlines_off(self, chart):
        """Disable major gridlines on the chart's value axis.

        Gridlines can clutter a chart; this method turns them off for a cleaner
        appearance.

        Args:
            chart: The ``pptx`` chart object to modify.
        """
        chart.value_axis.has_major_gridlines = False

    def _category_tick_label_low(self, chart):
        """Set category axis tick labels to the low position.

        This positions the tick label text at the bottom of the plot area, which
        aligns with the default style used throughout the library.

        Args:
            chart: The ``pptx`` chart object to modify.
        """
        chart.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW

    def _apply_axis_style(self, chart, chart_theme, block, value_axis_override):
        """Apply scaling and number format to the value axis.

        Handles optional explicit axis range overrides and applies tick label
        number formatting if specified in the chart specification.

        Args:
            chart: The ``pptx`` chart object.
            chart_theme: Theme dictionary (not used directly here but kept for
                signature consistency).
            block: Layout block containing the original chart spec.
            value_axis_override: Optional tuple ``(min, max)`` to force a specific
                axis range, overriding any range defined in the spec.
        """
        spec = block.chart
        axis = chart.value_axis

        if spec.value_axis_range or value_axis_override:
            value_axis_range = spec.value_axis_range
            value_axis_range = value_axis_override if value_axis_override else value_axis_range
            axis_min = value_axis_range[0]
            axis_max = value_axis_range[1]
            axis.minimum_scale = axis_min
            axis.maximum_scale = axis_max

            chart.value_axis_major_unit = (axis_max - axis_min) / 4

        if spec.value_axis_tick_format:
            chart.value_axis.tick_labels.number_format = spec.value_axis_tick_format

    def _set_data_labels(self, chart, chart_theme, block):
        """Configure data label visibility and styling for chart series.

        If the chart block requests data labels, this method enables them for each
        series, applies font size and style from the theme, and sets the label
        position. When a value‑axis tick format is defined, it is also applied to the
        data labels.

        Args:
            chart: The ``pptx`` chart object.
            chart_theme: Theme dictionary containing ``data_labels`` settings.
            block: Layout block providing the chart specification and the
                ``show_data_labels`` flag.
        """
        data_labels_theme = chart_theme.get("data_labels", {})

        spec = block.chart
        if block.chart.show_data_labels:
            position_map = {
                "OUTSIDE_END": XL_DATA_LABEL_POSITION.OUTSIDE_END,
            }

            for s in chart.series:
                s.data_labels.show_value = True
                s.data_labels.font.size = Pt(data_labels_theme["font_size"])
                s.data_labels.font.bold = data_labels_theme["bold"]
                s.data_labels.font.italic = data_labels_theme["italic"]
                s.data_labels.font.underline = data_labels_theme["underline"]
                s.data_labels.position = position_map[data_labels_theme["position"]]
                if spec.value_axis_tick_format:
                    s.data_labels.number_format = spec.value_axis_tick_format

    def _set_series_colors(self, chart, chart_theme, block):
        """Apply color styling to each series in the chart.

        Resolves the appropriate color for each series using ``resolve_series_color``
        and sets both the fill and line colors. For scatter charts the marker is
        also colored. This ensures consistent theming across all series.

        Args:
            chart: The ``pptx`` chart object.
            chart_theme: Theme dictionary (used indirectly via ``resolve_series_color``).
            block: Layout block containing the chart specification.
        """
        spec = block.chart

        for i, s in enumerate(chart.series):
            color = resolve_series_color(
                spec.series[i],
                i,
                chart_theme,
            )

            if hasattr(s, "invert_if_negative"):
                s.invert_if_negative = False

            s.format.fill.solid()
            s.format.fill.fore_color.rgb = hex_to_rgb255(color)
            s.format.line.fill.solid()
            s.format.line.color.rgb = hex_to_rgb255(color)

            if chart.chart_type == self._map_chart_type("scatter"):
                s.marker.style = 8  # automatic / circle depending on PPT

                s.marker.format.fill.solid()
                s.marker.format.fill.fore_color.rgb = hex_to_rgb255(color)

                s.marker.format.line.color.rgb = hex_to_rgb255(color)

    def _set_series_dashes(self, chart, chart_theme, block):
        """Apply dash style to line chart series.

        For line charts, each series' line dash style is resolved from the theme
        using ``resolve_series_dash`` and applied via the ``PPTX_DASH_MAP`` mapping.

        Args:
            chart: The ``pptx`` chart object.
            chart_theme: Theme dictionary containing dash style settings.
            block: Layout block providing the chart specification.
        """
        spec = block.chart

        if spec.chart_type == "line":
            for i, s in enumerate(chart.series):
                dash = resolve_series_dash(spec.series[i], chart_theme)
                s.format.line.dash_style = PPTX_DASH_MAP[dash]

    def _set_series_line_width(self, chart, chart_theme, block):
        """Set the line width for each series in a line chart.

        Uses ``resolve_series_width`` to obtain the width value from the theme and
        applies it (in points) to the series line using ``pptx.util.Pt``.

        Args:
            chart: The ``pptx`` chart object.
            chart_theme: Theme dictionary containing width settings.
            block: Layout block providing the chart specification.
        """
        spec = block.chart

        if spec.chart_type == "line":
            for i, s in enumerate(chart.series):
                s.format.line.width = Pt(resolve_series_width(spec.series[i], chart_theme))
