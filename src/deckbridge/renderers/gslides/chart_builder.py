from deckbridge.renderers.gslides.utils import GSLIDES_ALIGN_MAP

from ...deck.blocks import ChartBlock
from ...deck.specs import ChartSpec
from .utils import inches_to_pixels


class SheetsChartBuilder:
    def __init__(self, sheets_service, spreadsheet_id):
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

    def create_chart(self, sheet_id, spec: ChartSpec, position: dict):

        requests = [
            {
                "addChart": {
                    "chart": {
                        "spec": self._build_chart_spec(sheet_id, spec),
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

    def apply_chart_style(self, sheet_id, chart_id, block: ChartBlock, chart_theme: dict):

        # chart title
        api_spec = self._build_chart_spec(sheet_id, block.chart)
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
        if block.chart.value_axis_range:
            value_axis["viewWindowOptions"] = {
                "viewWindowMin": block.chart.value_axis_range[0],
                "viewWindowMax": block.chart.value_axis_range[1],
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

        requests = [
            {
                "updateChartSpec": {
                    "chartId": chart_id,
                    "spec": api_spec,
                }
            }
        ]

        return requests

    def _map_chart_type(self, chart_type):
        return {
            "line": "LINE",
            "bar": "COLUMN",
        }[chart_type]

    def _build_chart_spec(self, sheet_id, spec: ChartSpec):
        chart_type = self._map_chart_type(spec.chart_type)

        return {
            "title": None,
            "basicChart": {
                "chartType": self._map_chart_type(spec.chart_type),
                "legendPosition": "BOTTOM_LEGEND",
                "headerCount": 1,
                "axis": [
                    {
                        "position": "BOTTOM_AXIS",
                        "title": spec.x,
                    },
                    {
                        "position": "LEFT_AXIS",
                        "title": spec.y,
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
                "series": [
                    {
                        "series": {
                            "sourceRange": {
                                "sources": [
                                    {
                                        "sheetId": sheet_id,
                                        "startRowIndex": 0,
                                        "endRowIndex": len(spec.data) + 1,
                                        "startColumnIndex": 1,
                                        "endColumnIndex": 2,
                                    }
                                ]
                            }
                        }
                    }
                ],
            },
        }
