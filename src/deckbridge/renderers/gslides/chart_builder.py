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
        api_spec["title"] = block.chart_title if chart_theme["chart_title"]["has_title"] else None

        # axes
        axis_theme = chart_theme.get("axis", {})
        api_spec["basicChart"]["axis"] = [
            {
                "title": block.chart.x,
                "position": "BOTTOM_AXIS",
                "format": {
                    "fontSize": axis_theme["font_size"],
                },
            },
            {
                "title": block.chart.y,
                "position": "LEFT_AXIS",
                "format": {
                    "fontSize": axis_theme["font_size"],
                },
            },
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
