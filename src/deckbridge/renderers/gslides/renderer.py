from .chart_compiler import GSlidesChartCompiler


class GSlidesRenderer:
    def __init__(self, slides_service, sheets_service, spreadsheet_id):
        self.slides_service = slides_service
        self.sheets_service = sheets_service
        self.spreadsheet_id = spreadsheet_id

        self.chart_compiler = GSlidesChartCompiler(slides_service, sheets_service, spreadsheet_id)

    def render(self, deck, presentation_id: str):

        # -----------------------------
        # STEP 1: Create slide shells
        # -----------------------------
        page_id_map = self._create_slides(deck, presentation_id)

        # -----------------------------
        # STEP 2: Add title text
        # -----------------------------
        self._add_titles(deck, presentation_id, page_id_map)
        self._add_slide_titles(deck, presentation_id, page_id_map)

        # -----------------------------
        # STEP 3: Add charts
        # -----------------------------
        for i, slide in enumerate(deck.slides):
            if slide["type"] != "chart":
                continue

            spec = slide["spec"]

            self.chart_compiler.compile(presentation_id=presentation_id, page_id=page_id_map[i], spec=spec)

    # =========================================================
    # STEP 1 — CREATE SLIDES (STRUCTURE ONLY)
    # =========================================================
    def _create_slides(self, deck, presentation_id):
        requests = []
        page_ids = {}

        for i, slide in enumerate(deck.slides):
            slide_id = f"slide_{i}"

            requests.append({"createSlide": {"objectId": slide_id, "slideLayoutReference": {"predefinedLayout": "BLANK"}}})

            page_ids[i] = slide_id

        self.slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()

        return page_ids

    # =========================================================
    # STEP 2 — ADD TITLES (SAFE TEXT BOX APPROACH)
    # =========================================================
    def _add_titles(self, deck, presentation_id, page_id_map):
        requests = []

        for i, slide in enumerate(deck.slides):
            if slide["type"] != "title":
                continue

            slide_id = page_id_map[i]

            title_box_id = f"title_box_{i}"

            TITLE_STYLE = {
                "title": {"x": 1000000, "y": 800000, "width": 8000000, "height": 1500000},
                "subtitle": {"x": 1000000, "y": 2200000, "width": 8000000, "height": 800000},
            }

            requests.append(
                {
                    "createShape": {
                        "objectId": title_box_id,
                        "shapeType": "TEXT_BOX",
                        "elementProperties": {
                            "pageObjectId": slide_id,
                            "size": {"height": {"magnitude": 1000000, "unit": "EMU"}, "width": {"magnitude": 8000000, "unit": "EMU"}},
                            "transform": {
                                "scaleX": 1,
                                "scaleY": 1,
                                "translateX": TITLE_STYLE["title"]["x"],
                                "translateY": TITLE_STYLE["title"]["y"],
                                "unit": "EMU",
                            },
                        },
                    }
                }
            )

            requests.append({"insertText": {"objectId": title_box_id, "text": slide["title"]}})

            # center alignment
            requests.append({"updateParagraphStyle": {"objectId": title_box_id, "style": {"alignment": "CENTER"}, "fields": "alignment"}})

            # subtitle (optional)
            if slide.get("subtitle"):
                subtitle_box_id = f"subtitle_box_{i}"

                requests.append(
                    {
                        "createShape": {
                            "objectId": subtitle_box_id,
                            "shapeType": "TEXT_BOX",
                            "elementProperties": {
                                "pageObjectId": slide_id,
                                "size": {"height": {"magnitude": 800000, "unit": "EMU"}, "width": {"magnitude": 8000000, "unit": "EMU"}},
                                "transform": {
                                    "scaleX": 1,
                                    "scaleY": 1,
                                    "translateX": TITLE_STYLE["subtitle"]["x"],
                                    "translateY": TITLE_STYLE["subtitle"]["y"],
                                    "unit": "EMU",
                                },
                            },
                        }
                    }
                )

                requests.append({"insertText": {"objectId": subtitle_box_id, "text": slide["subtitle"]}})

                # 👇 Center subtitle
                requests.append(
                    {"updateParagraphStyle": {"objectId": subtitle_box_id, "style": {"alignment": "CENTER"}, "fields": "alignment"}}
                )

                requests.append(
                    {
                        "updateTextStyle": {
                            "objectId": subtitle_box_id,
                            "style": {"fontSize": {"magnitude": 18, "unit": "PT"}},
                            "fields": "fontSize",
                        }
                    }
                )

        if requests:
            self.slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()

    def _add_slide_titles(self, deck, presentation_id, page_id_map):
        requests = []

        for i, slide in enumerate(deck.slides):
            if slide["type"] != "chart":
                continue

            slide_id = page_id_map[i]
            title_id = f"chart_title_{i}"

            requests.append(
                {
                    "createShape": {
                        "objectId": title_id,
                        "shapeType": "TEXT_BOX",
                        "elementProperties": {
                            "pageObjectId": slide_id,
                            "size": {"height": {"magnitude": 800000, "unit": "EMU"}, "width": {"magnitude": 8000000, "unit": "EMU"}},
                            "transform": {"scaleX": 1, "scaleY": 1, "translateX": 500000, "translateY": 200000, "unit": "EMU"},
                        },
                    }
                }
            )

            requests.append({"insertText": {"objectId": title_id, "text": slide["spec"].title}})

        if requests:
            self.slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
