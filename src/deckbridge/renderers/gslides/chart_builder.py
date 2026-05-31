from deckbridge.deck.blocks import ChartBlock
from deckbridge.deck.specs import ChartSpec
from deckbridge.renderers.common.style_resolver import resolve_series_color, resolve_series_dash, resolve_series_width
from deckbridge.renderers.gslides.utils import (
    GSHEETS_CHART_DASH_MAP,
    GSHEETS_CHART_STACKING_MAP,
    GSHEETS_CHART_TYPE_MAP,
    GSLIDES_ALIGN_MAP,
    hex_to_slides_rgb,
    inches_to_pixels,
)


class SheetsChartBuilder:
    """Builder for Google Sheets chart specifications and styling.

    This class creates a chart specification compatible with the Google Sheets
    API, handles the creation of chart objects, and applies theme‑driven styling
    based on the deck's chart theme configuration.
    """

    def __init__(self, sheets_service, spreadsheet_id):
        """Initializes the SheetsChartBuilder.

        Args:
            sheets_service: Authenticated Google Sheets service instance used to
                create and update charts.
            spreadsheet_id (str): ID of the spreadsheet where chart data resides.
        """
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

    def create_chart(self, chart_id, sheet_id, spec: ChartSpec, block: ChartBlock, position: dict):
        """Create a chart in Google Sheets.

        Constructs a request payload for the Sheets API that adds a new chart
        based on the provided specification and places it on the sheet.

        Args:
            chart_id (int): Identifier for the new chart.
            sheet_id (int): Identifier of the sheet where the chart will be
                created.
            spec (ChartSpec): Specification of the chart (type, data, etc.).
            block (ChartBlock): Block containing chart metadata such as titles
                and axis labels.
            position (dict): Mapping with keys ``x``, ``y``, ``w``, ``h`` defining
                the chart's size in inches. These values are converted to pixel
                dimensions for the API request.

        Returns:
            list[dict]: A list containing a single ``addChart`` request dict that
                can be merged into the batchUpdate payload.
        """
        requests = [
            {
                "addChart": {
                    "chart": {
                        "chartId": chart_id,
                        "spec": self._build_chart_spec(sheet_id, spec, block),
                        "position": {
                            "overlayPosition": {
                                "anchorCell": {
                                    "sheetId": sheet_id,
                                    "rowIndex": 1,
                                    "columnIndex": 5,
                                },
                                "offsetXPixels": 0,
                                "offsetYPixels": 0,
                                "widthPixels": inches_to_pixels(position["w"]),
                                "heightPixels": inches_to_pixels(position["h"]),
                            }
                        },
                    }
                }
            }
        ]

        return requests

    def apply_chart_style(self, sheet_id, chart_id, block: ChartBlock, chart_theme: dict, value_axis_override):
        """Apply theme‑driven styling to an existing Google Sheets chart.

        This method updates the chart specification with titles, axis formatting,
        legend configuration, data labels, and series styling based on the
        resolved ``chart_theme``. It generates an ``updateChartSpec`` request that
        can be merged into the batchUpdate payload.

        Args:
            sheet_id (int): Identifier of the sheet containing the chart data.
            chart_id (int): Identifier of the chart to style.
            block (ChartBlock): Chart block providing titles, axis titles, and
                other metadata.
            chart_theme (dict): Resolved theme dictionary containing styling
                information for titles, axes, legend, data labels, series colors,
                dashes, and widths.
            value_axis_override (tuple, optional): Optional ``(min, max)`` tuple
                to override the chart's value axis range. If ``None`` the chart's
                own ``value_axis_range`` is used.

        Returns:
            list[dict]: A list containing a single ``updateChartSpec`` request
                dict that updates the chart with the new styling.
        """
        # chart title
        api_spec = self._build_chart_spec(sheet_id, block.chart, block)
        if chart_theme["chart_title"]["has_title"]:
            api_spec["title"] = block.chart_title
            api_spec["titleTextFormat"] = {
                "fontSize": chart_theme["chart_title"]["font_size"],
                "bold": chart_theme["chart_title"]["bold"],
                "italic": chart_theme["chart_title"]["italic"],
            }
            api_spec["titleTextPosition"] = {"horizontalAlignment": GSLIDES_ALIGN_MAP[chart_theme["chart_title"]["align"]]}

            if chart_theme["chart_subtitle"]["has_title"]:
                api_spec["subtitle"] = block.chart_subtitle
                api_spec["subtitleTextFormat"] = {
                    "fontSize": chart_theme["chart_subtitle"]["font_size"],
                    "bold": chart_theme["chart_subtitle"]["bold"],
                    "italic": chart_theme["chart_subtitle"]["italic"],
                }
                api_spec["subtitleTextPosition"] = {"horizontalAlignment": GSLIDES_ALIGN_MAP[chart_theme["chart_subtitle"]["align"]]}

        # axes
        value_axis_theme = chart_theme.get("value_axis", {})
        category_axis_theme = chart_theme.get("category_axis", {})

        value_axis = {
            "title": block.value_axis_title,
            "position": "LEFT_AXIS",
            "format": {
                "fontSize": value_axis_theme["font_size"],
                "bold": value_axis_theme["bold"],
                "italic": value_axis_theme["italic"],
            },
        }
        if block.chart.value_axis_range or value_axis_override:
            value_axis_range = block.chart.value_axis_range
            value_axis_range = value_axis_override if value_axis_override else value_axis_range
            if value_axis_range is not None:
                value_axis["viewWindowOptions"] = {
                    "viewWindowMin": value_axis_range[0],
                    "viewWindowMax": value_axis_range[1],
                }
        category_axis = {
            "title": block.category_axis_title,
            "position": "BOTTOM_AXIS",
            "format": {
                "fontSize": category_axis_theme["font_size"],
                "bold": category_axis_theme["bold"],
                "italic": category_axis_theme["italic"],
            },
        }
        api_spec["basicChart"]["axis"] = [
            value_axis,
            category_axis,
        ]

        # legend
        legend_theme = chart_theme.get("legend", {})
        if not legend_theme["visible"]:
            api_spec["basicChart"]["legendPosition"] = "NO_LEGEND"
        else:
            api_spec["basicChart"]["legendPosition"] = legend_theme["position"] + "_LEGEND"

        # data labels
        if block.chart.show_data_labels:
            data_labels_theme = chart_theme.get("data_labels", {})
            for i, s in enumerate(block.chart.series):
                api_spec["basicChart"]["series"][i]["dataLabel"] = {
                    "type": "DATA",
                    "placement": data_labels_theme["position"],
                    "textFormat": {
                        "fontSize": data_labels_theme["font_size"],
                        "bold": data_labels_theme["bold"],
                        "italic": data_labels_theme["italic"],
                    },
                }

        # series colors, dashes
        for i, s in enumerate(block.chart.series):
            color = resolve_series_color(block.chart.series[i], i, chart_theme)
            api_spec["basicChart"]["series"][i]["color"] = hex_to_slides_rgb(color)
            if block.chart.chart_type == "line":
                api_spec["basicChart"]["series"][i]["lineStyle"] = {
                    "type": GSHEETS_CHART_DASH_MAP[resolve_series_dash(block.chart.series[i], chart_theme)],
                    "width": resolve_series_width(block.chart.series[i], chart_theme),
                }

        requests = [
            {
                "updateChartSpec": {
                    "chartId": chart_id,
                    "spec": api_spec,
                }
            }
        ]

        return requests

    def _build_chart_spec(self, sheet_id, spec: ChartSpec, block: ChartBlock):
        """Construct the low‑level chart specification for the Google Sheets API.

        This helper assembles the JSON structure required by the Sheets API to
        define a chart, including data series ranges, axis definitions, and
        default legend positioning. It is used both when initially creating a
        chart and when updating its styling.

        Args:
            sheet_id (int): Identifier of the sheet containing the chart data.
            spec (ChartSpec): Specification describing the chart type, series,
                and underlying pandas ``DataFrame``.
            block (ChartBlock): Block containing user‑specified titles and axis
                labels.

        Returns:
            dict: A dictionary representing the chart specification compatible
                with the Sheets API ``addChart`` and ``updateChartSpec`` requests.
        """
        series = []

        for i, s in enumerate(spec.series):
            series.append(
                {
                    "series": {
                        "sourceRange": {
                            "sources": [
                                {
                                    "sheetId": sheet_id,
                                    "startRowIndex": 0,
                                    "endRowIndex": len(spec.data) + 1,
                                    "startColumnIndex": i + 1,  # assuming x is col 0
                                    "endColumnIndex": i + 2,
                                }
                            ]
                        }
                    },
                    "targetAxis": "BOTTOM_AXIS" if spec.chart_type == "bar_stacked" else "LEFT_AXIS",
                }
            )

        api_spec = {
            "title": None,
            "basicChart": {
                "chartType": GSHEETS_CHART_TYPE_MAP[spec.chart_type],
                "legendPosition": "BOTTOM_LEGEND",
                "headerCount": 1,
                "axis": [
                    {
                        "position": "BOTTOM_AXIS",
                        "title": block.category_axis_title,
                    },
                    {
                        "position": "LEFT_AXIS",
                        "title": block.value_axis_title,
                    },
                ],
                "domains": [
                    {
                        "domain": {
                            "sourceRange": {
                                "sources": [
                                    {
                                        "sheetId": sheet_id,
                                        "startRowIndex": 0,
                                        "endRowIndex": len(spec.data) + 1,
                                        "startColumnIndex": 0,
                                        "endColumnIndex": 1,
                                    }
                                ]
                            }
                        }
                    }
                ],
                "series": series,
            },
        }
        # Ensure proper type for mypy when adding stacked type
        if GSHEETS_CHART_STACKING_MAP[spec.chart_type] != "NOT_STACKED":
            from typing import Any, Dict, cast

            basic_chart = cast(Dict[str, Any], api_spec["basicChart"])
            basic_chart["stackedType"] = GSHEETS_CHART_STACKING_MAP[spec.chart_type]
            api_spec["basicChart"] = basic_chart

        return api_spec
