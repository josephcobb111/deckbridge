from deckbridge.renderers.common.context import RenderContext
from deckbridge.renderers.common.slot_renderer import render_slots
from deckbridge.renderers.gslides.chart_compiler import GSlidesChartCompiler


class GSlidesRenderer:
    """Renderer for Google Slides presentations.

    This class coordinates creation of slides, sheets, and charts, accumulating
    batchUpdate requests for the Google Slides and Sheets APIs. It delegates the
    actual chart compilation to :class:`~deckbridge.renderers.gslides.chart_compiler.GSlidesChartCompiler`
    and uses :class:`~deckbridge.renderers.common.context.RenderContext` to
    render individual slots on each slide.
    """

    def __init__(self, slides_service, sheets_service, spreadsheet_id, presentation_id, execute_requests):
        """Initializes the GSlidesRenderer.

        Args:
            slides_service: Authenticated Google Slides service instance.
            sheets_service: Authenticated Google Sheets service instance.
            spreadsheet_id: ID of the spreadsheet used for data sheets.
            presentation_id: ID of the Slides presentation being rendered.
            execute_requests: Whether to automatically execute the accumulated batch
                update requests after rendering.
        """
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

        self.execute_requests = execute_requests

    def render(self, deck):
        """Renders the entire deck into Google Slides.

        The method performs three main steps:
        1. Creates blank slides for each slide in the deck.
        2. Renders the content of each slide using the appropriate layout.
        3. Optionally executes all accumulated batchUpdate requests.

        Args:
            deck: A :class:`deckbridge.models.Deck` (or compatible) object that
                contains a list of slide definitions in ``deck.slides``.
        """
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
        if self.execute_requests:
            self._execute_requests()

    # =========================================================
    # CREATE SLIDES
    # =========================================================
    def _create_slides(self, deck):
        """Create blank slides for each slide in the deck.

        Generates a unique ``objectId`` for each slide (e.g. ``slide_0``) and
        appends a ``createSlide`` request to ``self.create_slide_requests``.
        Returns a mapping from the slide index to the generated ``objectId`` so
        that subsequent rendering steps can reference the correct page.

        Args:
            deck: Deck object containing a ``slides`` attribute.

        Returns:
            dict[int, str]: Mapping of slide index to slide ``objectId``.
        """
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
        """Render a single slide's content.

        Creates a ``RenderContext`` for the slide, runs ``render_slots`` to populate
        the slide with text, images, charts, etc., and then gathers the resulting
        request lists from the context into the renderer's accumulated request
        collections.

        Args:
            slide (dict): Slide definition containing layout and slot data.
            page_id (str): The Google Slides object ID for the target slide.
        """
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
        """Execute a batchUpdate request for the appropriate Google API.

        The method abstracts the differences between the Slides and Sheets services,
        handling three possible ``service`` values:

        * ``"sheets"`` – updates sheet structure (e.g., adding sheets).
        * ``"sheets_values"`` – writes cell values.
        * ``"slides"`` – updates slide objects (e.g., creating shapes, inserting text).

        Args:
            _id (str): The spreadsheet ID for Sheets or the presentation ID for Slides.
            requests (list[dict]): A list of request dictionaries for the API.
            service (str): Which service to target (``"sheets"``, ``"sheets_values"`` or ``"slides"``).
        """
        if service == "sheets":
            self.sheets.spreadsheets().batchUpdate(spreadsheetId=_id, body={"requests": requests}).execute()
        if service == "sheets_values":
            self.sheets.spreadsheets().values().batchUpdate(
                spreadsheetId=self.spreadsheet_id, body={"valueInputOption": "RAW", "data": requests}
            ).execute()
        elif service == "slides":
            self.slides.presentations().batchUpdate(presentationId=_id, body={"requests": requests}).execute()

    def _execute_requests(self):
        """Execute all accumulated batchUpdate requests for Sheets and Slides.

        This helper runs each non‑empty request list in the appropriate order, calling
        ``_batch_update`` with the correct service identifier. It ensures that sheet
        creation, value writes, chart creation, slide creation, and embedding steps
        are performed before text and legend insertion.
        """
        if self.create_sheet_requests:
            self._batch_update(self.spreadsheet_id, self.create_sheet_requests, "sheets")

        if self.create_values_requests:
            self._batch_update(self.spreadsheet_id, self.create_values_requests, "sheets_values")

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
