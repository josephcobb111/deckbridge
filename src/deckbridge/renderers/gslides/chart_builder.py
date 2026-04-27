from ...deck.specs import ChartSpec


class SheetsChartBuilder:
    def __init__(self, sheets_service, spreadsheet_id):
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

    def create_chart(self, sheet_name, sheet_id, spec: ChartSpec):

        requests = [
            {
                "addChart": {
                    "chart": {
                        "spec": {
                            "title": spec.title,
                            "basicChart": {
                                "chartType": self._map_chart_type(spec.chart_type),
                                "legendPosition": "BOTTOM_LEGEND",
                                "axis": [{"position": "BOTTOM_AXIS", "title": spec.x}, {"position": "LEFT_AXIS", "title": spec.y}],
                                "domains": [
                                    {
                                        "domain": {
                                            "sourceRange": {
                                                "sources": [
                                                    {
                                                        "sheetId": sheet_id,
                                                        "startRowIndex": 1,
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
                                                        "startRowIndex": 1,
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
                        "position": {"newSheet": True},
                    }
                }
            }
        ]

        return requests

    def _map_chart_type(self, chart_type):
        return {"line": "LINE", "bar": "COLUMN"}[chart_type]
