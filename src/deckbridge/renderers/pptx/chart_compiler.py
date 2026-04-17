from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

from ...deck.specs import ChartSpec


class PPTXChartCompiler:
    """
    Converts ChartSpec → native python-pptx chart objects
    (fully editable in PowerPoint)
    """

    def compile(self, spec: ChartSpec):
        chart_data = CategoryChartData()

        # Extract categories (x-axis)
        categories = list(spec.data[spec.x])
        values = list(spec.data[spec.y])

        chart_data.categories = categories
        chart_data.add_series(spec.y, values)

        chart_type = self._map_chart_type(spec.chart_type)

        return chart_type, chart_data

    def _map_chart_type(self, chart_type: str):
        mapping = {
            "line": XL_CHART_TYPE.LINE,
            "bar": XL_CHART_TYPE.COLUMN_CLUSTERED,
        }

        if chart_type not in mapping:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        return mapping[chart_type]
