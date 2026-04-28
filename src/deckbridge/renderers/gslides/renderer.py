from deckbridge.layouts.registry import LAYOUTS
from deckbridge.renderers.common.slot_renderer import render_slot
from deckbridge.renderers.common.text_renderer import resolve_text_content
from deckbridge.renderers.gslides.chart_compiler import GSlidesChartCompiler

from .utils import inches_to_emu


class GSlidesRenderer:
    def __init__(self, slides_service, sheets_service, spreadsheet_id):
        self.slides = slides_service
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

        self.chart_compiler = GSlidesChartCompiler(slides_service, sheets_service, spreadsheet_id)

    def render(self, deck, presentation_id: str):

        # -----------------------------
        # Create slides
        # -----------------------------
        page_id_map = self._create_slides(deck, presentation_id)

        # -----------------------------
        # Render content for each slide
        # -----------------------------
        for i, slide in enumerate(deck.slides):
            self._render_content(slide, presentation_id, page_id_map[i])

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

        self._batch_update(presentation_id, requests)

        return page_ids

    # =========================================================
    # RENDER CONTENT
    # =========================================================
    def _render_content(self, slide, presentation_id, page_id):

        layout_spec = LAYOUTS[slide["layout"]]
        slots = layout_spec.slots

        for slot_key, slot in slots.items():
            slot_type = slot.get("type")

            # -----------------------
            # Resolve content
            # -----------------------
            if slot_type == "chart":
                content = slide["content"].get(slot_key)

            elif slot_type == "text":
                content = resolve_text_content(slide, slot_key)

            else:
                content = None

            # -----------------------
            # Render
            # -----------------------
            render_slot(
                backend="gslides",
                slot_key=slot_key,
                slot=slot,
                content=content,
                slides_service=self.slides,
                presentation_id=presentation_id,
                page_id=page_id,
                chart_compiler=self.chart_compiler,
            )

    # =========================================================
    # BATCH HELPER
    # =========================================================
    def _batch_update(self, presentation_id, requests):
        self.slides.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
