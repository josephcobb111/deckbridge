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
                        "spec": {
                            "basicChart": {
                                "chartType": self._map_chart_type(spec.chart_type),
                                "legendPosition": "BOTTOM_LEGEND",
                                "headerCount": 1,
                                "axis": [{"position": "BOTTOM_AXIS", "title": spec.x}, {"position": "LEFT_AXIS", "title": spec.y}],
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
                        },
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
                        # },
                    }
                }
            }
        ]

        return requests

    def _map_chart_type(self, chart_type):
        return {"line": "LINE", "bar": "COLUMN"}[chart_type]
