from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION
from pptx.util import Inches, Pt

from deckbridge.renderers.common.style_resolver import resolve_chart_theme


class PPTXChartBuilder:
    def build_chart_data(self, spec):
        """
        Build chart type + data (no styling here)
        """
        chart_data = self._build_chart_data(spec)
        chart_type = self._map_chart_type(spec.chart_type)

        return chart_type, chart_data

    def apply_chart_style(self, chart, theme, layout_name, block):
        """
        Apply theme-driven styling to a chart object
        """
        chart_theme = resolve_chart_theme(theme, layout_name)

        self._single_series_bar_chart(chart)
        self._set_chart_title(chart, chart_theme, block)
        self._set_chart_subtitle(chart, chart_theme, block)
        self._set_axis_title(chart, chart_theme, "value_axis", block.value_axis_title)
        self._set_axis_title(chart, chart_theme, "category_axis", block.category_axis_title)
        self._apply_legend_style(chart, chart_theme)
        self._turn_gridlines_off(chart)
        self._category_tick_label_low(chart)
        self._apply_axis_style(chart, chart_theme, block)

    def _build_chart_data(self, spec):
        chart_data = CategoryChartData()

        categories = list(spec.data[spec.x])
        values = list(spec.data[spec.y])

        chart_data.categories = categories
        chart_data.add_series(spec.y, values)

        return chart_data

    def _map_chart_type(self, chart_type):
        mapping = {
            "line": XL_CHART_TYPE.LINE,
            "bar": XL_CHART_TYPE.COLUMN_CLUSTERED,
        }

        if chart_type not in mapping:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        return mapping[chart_type]

    def _single_series_bar_chart(self, chart):
        if chart.chart_type == self._map_chart_type("bar") and len(chart.plots[0].series) == 1:
            chart.plots[0].vary_by_categories = False

    def _set_chart_title(self, chart, chart_theme, block):
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

        axis_obj.tick_labels.font.size = Pt(axis_theme["font_size"])

    def _apply_legend_style(self, chart, chart_theme):
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
        chart.value_axis.has_major_gridlines = False

    def _category_tick_label_low(self, chart):
        chart.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW

    def _apply_axis_style(self, chart, chart_theme, block):
        spec = block.chart
        axis = chart.value_axis

        if spec.value_axis_range:
            axis_min = spec.value_axis_range[0]
            axis_max = spec.value_axis_range[1]
            axis.minimum_scale = axis_min
            axis.maximum_scale = axis_max

            chart.value_axis_major_unit = (axis_max - axis_min) / 4

        if spec.value_axis_tick_format:
            chart.value_axis.tick_labels.number_format = spec.value_axis_tick_format
