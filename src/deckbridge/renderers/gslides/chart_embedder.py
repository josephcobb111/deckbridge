from .utils import inches_to_emu


class SlidesChartEmbedder:
    def __init__(self, slides_service):
        self.slides = slides_service

    def embed_chart(self, presentation_id, spreadsheet_id, chart_id, page_id, position):

        requests = [
            {
                "createSheetsChart": {
                    "spreadsheetId": spreadsheet_id,
                    "chartId": chart_id,
                    "linkingMode": "LINKED",
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {
                            "height": {"magnitude": inches_to_emu(position["h"]), "unit": "EMU"},
                            "width": {"magnitude": inches_to_emu(position["w"]), "unit": "EMU"},
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": inches_to_emu(position["x"]),
                            "translateY": inches_to_emu(position["y"]),
                            "unit": "EMU",
                        },
                    },
                },
            },
        ]

        self.slides.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
