from deckbridge.renderers.common.context import RenderContext
from deckbridge.renderers.common.slot_renderer import render_slots
from deckbridge.renderers.gslides.chart_compiler import GSlidesChartCompiler


class GSlidesRenderer:
    def __init__(self, slides_service, sheets_service, spreadsheet_id, presentation_id):
        self.slides = slides_service
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id
        self.presentation_id = presentation_id

        # sheet requests
        self.create_sheet_requests = []
        self.create_values_requests = []
        self.format_values_requests = []
        self.create_chart_requests = []

        # slides requests
        self.create_slide_requests = []
        self.embed_chart_requests = []
        self.create_text_requests = []
        self.create_legend_requests = []

        self.chart_compiler = GSlidesChartCompiler(slides_service, sheets_service, spreadsheet_id)

    def render(self, deck):

        # -----------------------------
        # Create slides
        # -----------------------------
        page_id_map = self._create_slides(deck)

        # -----------------------------
        # Render content for each slide
        # -----------------------------
        for i, slide in enumerate(deck.slides):
            self._render_content(slide, page_id_map[i])

        # -----------------------------
        # Execute requests
        # -----------------------------
        self._execute_requests()

    # =========================================================
    # CREATE SLIDES
    # =========================================================
    def _create_slides(self, deck):
        page_ids = {}

        for i, _ in enumerate(deck.slides):
            slide_id = f"slide_{i}"

            self.create_slide_requests.append(
                {"createSlide": {"objectId": slide_id, "slideLayoutReference": {"predefinedLayout": "BLANK"}}}
            )

            page_ids[i] = slide_id

        return page_ids

    # =========================================================
    # RENDER CONTENT
    # =========================================================
    def _render_content(self, slide, page_id):
        layout_spec = self.layouts[slide["layout"]]

        ctx = RenderContext(
            backend="gslides",
            layout_spec=layout_spec,
            theme=self.theme,
            slides_service=self.slides,
            sheets_service=self.sheets,
            presentation_id=self.presentation_id,
            spreadsheet_id=self.spreadsheet_id,
            page_id=page_id,
            chart_compiler=self.chart_compiler,
        )

        render_slots(ctx, slide)

        # add slide requests from RenderContext to deck requests
        self.create_sheet_requests.extend(ctx.create_sheet_requests)
        self.create_values_requests.extend(ctx.create_values_requests)
        self.format_values_requests.extend(ctx.format_values_requests)
        self.create_chart_requests.extend(ctx.create_chart_requests)
        self.embed_chart_requests.extend(ctx.embed_chart_requests)
        self.create_text_requests.extend(ctx.create_text_requests)

    # =========================================================
    # BATCH HELPER
    # =========================================================
    def _batch_update(self, _id, requests, service):
        if service == "sheets":
            self.sheets.spreadsheets().batchUpdate(spreadsheetId=_id, body={"requests": requests}).execute()
        elif service == "slides":
            self.slides.presentations().batchUpdate(presentationId=_id, body={"requests": requests}).execute()

    def _execute_requests(self):
        if self.create_sheet_requests:
            self._batch_update(self.spreadsheet_id, self.create_sheet_requests, "sheets")

        for value_update in self.create_values_requests:
            self.sheets.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=value_update["range"],
                valueInputOption="RAW",
                body={
                    "values": value_update["values"],
                },
            ).execute()

        if self.format_values_requests:
            self._batch_update(self.spreadsheet_id, self.format_values_requests, "sheets")

        if self.create_chart_requests:
            self._batch_update(self.spreadsheet_id, self.create_chart_requests, "sheets")

        if self.create_slide_requests:
            self._batch_update(self.presentation_id, self.create_slide_requests, "slides")

        if self.embed_chart_requests:
            self._batch_update(self.presentation_id, self.embed_chart_requests, "slides")

        if self.create_text_requests:
            self._batch_update(self.presentation_id, self.create_text_requests, "slides")

        if self.create_legend_requests:
            self._batch_update(self.presentation_id, self.create_legend_requests, "slides")
