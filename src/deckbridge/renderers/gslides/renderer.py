from deckbridge.layouts.registry import LAYOUTS
from deckbridge.renderers.common.text_renderer import render_text_slots
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

        text_map = {}

        # -----------------------
        # Global text fields
        # -----------------------
        for key in ["deck_title", "deck_author", "slide_title"]:
            if slide.get(key):
                text_map[key] = slide[key]

        # -----------------------
        # Slot-driven rendering
        # -----------------------
        for slot_key, slot in slots.items():
            # -----------------------
            # Chart slots
            # -----------------------
            if slot_key.startswith("chart_") and not slot_key.endswith("_title"):
                block = slide["content"].get(slot_key)
                if not block:
                    continue

                # Render chart
                self.chart_compiler.compile(
                    presentation_id=presentation_id,
                    page_id=page_id,
                    spec=block.chart,
                    position=slot,
                    chart_key=slot_key,
                )

                # Add chart title to text_map
                if getattr(block, "chart_title", None):
                    text_map[f"{slot_key}_title"] = block.chart_title

        # -----------------------
        # Render all text slots
        # -----------------------
        render_text_slots(
            backend="gslides",
            layout_spec=layout_spec,
            text_map=text_map,
            slides_service=self.slides,
            presentation_id=presentation_id,
            page_id=page_id,
        )

    # =========================================================
    # BATCH HELPER
    # =========================================================
    def _batch_update(self, presentation_id, requests):
        self.slides.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
