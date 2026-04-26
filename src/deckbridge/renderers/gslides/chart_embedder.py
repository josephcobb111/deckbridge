from .utils import to_emu


class SlidesChartEmbedder:
    def __init__(self, slides_service):
        self.slides = slides_service

    def embed_chart(self, presentation_id, spreadsheet_id, chart_id, page_id, slot):

        width = to_emu(slot["w"])
        height = to_emu(slot["h"])
        x = to_emu(slot["x"])
        y = to_emu(slot["y"])

        requests = [
            {
                "createSheetsChart": {
                    "spreadsheetId": spreadsheet_id,
                    "chartId": chart_id,
                    "linkingMode": "LINKED",
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {"height": {"magnitude": height, "unit": "EMU"}, "width": {"magnitude": width, "unit": "EMU"}},
                        "transform": {"scaleX": 1, "scaleY": 1, "translateX": x, "translateY": y, "unit": "EMU"},
                    },
                }
            }
        ]

        self.slides.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
