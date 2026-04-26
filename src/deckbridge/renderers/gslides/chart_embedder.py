class SlidesChartEmbedder:
    def __init__(self, slides_service):
        self.slides = slides_service

    def embed_chart(self, presentation_id, spreadsheet_id, chart_id, page_id):

        requests = [
            {
                "createSheetsChart": {
                    "spreadsheetId": spreadsheet_id,
                    "chartId": chart_id,
                    "linkingMode": "LINKED",
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {"height": {"magnitude": 3500000, "unit": "EMU"}, "width": {"magnitude": 7000000, "unit": "EMU"}},
                        "transform": {"scaleX": 1, "scaleY": 1, "translateX": 1000000, "translateY": 1200000, "unit": "EMU"},
                    },
                }
            }
        ]

        self.slides.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
