from deckbridge.layouts.registry import LAYOUTS
from deckbridge.renderers.gslides.chart_compiler import GSlidesChartCompiler


class GSlidesRenderer:
    def __init__(self, slides_service, sheets_service, spreadsheet_id):
        self.slides = slides_service
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

        self.chart_compiler = GSlidesChartCompiler(slides_service, sheets_service, spreadsheet_id)

    def render(self, deck, presentation_id: str):

        # -----------------------------
        # STEP 1: Create slides
        # -----------------------------
        page_id_map = self._create_slides(deck, presentation_id)

        # -----------------------------
        # STEP 2: Render content via slots
        # -----------------------------
        for i, slide in enumerate(deck.slides):
            if slide["type"] == "title":
                self._render_title_slide(slide, presentation_id, page_id_map[i])

            elif slide["type"] == "chart":
                self._render_chart_slide(slide, presentation_id, page_id_map[i])

    # =========================================================
    # CREATE SLIDES
    # =========================================================
    def _create_slides(self, deck, presentation_id):
        requests = []
        page_ids = {}

        for i, _ in enumerate(deck.slides):
            slide_id = f"slide_{i}"

            requests.append({"createSlide": {"objectId": slide_id, "slideLayoutReference": {"predefinedLayout": "BLANK"}}})

            page_ids[i] = slide_id

        self.slides.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()

        return page_ids

    # =========================================================
    # TITLE SLIDE (keep simple for now)
    # =========================================================
    def _render_title_slide(self, slide, presentation_id, page_id):
        requests = []

        # Title
        requests += self._create_textbox(object_id=f"title_{page_id}", text=slide["title"], page_id=page_id, x=1, y=1, w=8, h=1)

        # Subtitle
        if slide.get("subtitle"):
            requests += self._create_textbox(object_id=f"subtitle_{page_id}", text=slide["subtitle"], page_id=page_id, x=1, y=2, w=8, h=1)

        self._batch_update(presentation_id, requests)

    # =========================================================
    # CHART SLIDE (SLOT-DRIVEN)
    # =========================================================
    def _render_chart_slide(self, slide, presentation_id, page_id):

        layout_spec = LAYOUTS[slide["layout"]]
        slots = layout_spec.slots

        requests = []

        # -----------------------
        # Slide title
        # -----------------------
        if "slide_title" in slots and slide.get("title"):
            slot = slots["slide_title"]

            requests += self._create_textbox(object_id=f"slide_title_{page_id}", text=slide["title"], page_id=page_id, **slot)

        # -----------------------
        # Charts + chart titles
        # -----------------------
        for i, block in enumerate(slide["charts"], start=1):
            chart_slot_key = f"chart_{i}"
            title_slot_key = f"chart_{i}_title"

            # --- Chart ---
            if chart_slot_key in slots:
                chart_slot = slots[chart_slot_key]

                self.chart_compiler.compile(
                    presentation_id=presentation_id,
                    page_id=page_id,
                    spec=block.chart,
                    position=chart_slot,
                    chart_key=chart_slot_key,
                )

            # --- Chart title ---
            if block.title and title_slot_key in slots:
                title_slot = slots[title_slot_key]

                requests += self._create_textbox(object_id=f"{title_slot_key}_{page_id}", text=block.title, page_id=page_id, **title_slot)

        if requests:
            self._batch_update(presentation_id, requests)

    # =========================================================
    # TEXTBOX HELPER
    # =========================================================
    def _create_textbox(self, object_id, text, page_id, x, y, w, h):
        return [
            {
                "createShape": {
                    "objectId": object_id,
                    "shapeType": "TEXT_BOX",
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {"height": {"magnitude": h * 914400, "unit": "EMU"}, "width": {"magnitude": w * 914400, "unit": "EMU"}},
                        "transform": {"scaleX": 1, "scaleY": 1, "translateX": x * 914400, "translateY": y * 914400, "unit": "EMU"},
                    },
                }
            },
            {"insertText": {"objectId": object_id, "text": text}},
        ]

    # =========================================================
    # BATCH HELPER
    # =========================================================
    def _batch_update(self, presentation_id, requests):
        self.slides.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
