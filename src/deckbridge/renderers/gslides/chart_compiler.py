"""Utilities for compiling chart data and embedding it into Google Slides.

This module defines :class:`GSlidesChartCompiler`, which orchestrates writing chart data
to a Google Sheet, building a chart via the Sheets API, styling it, and finally
embedding the linked chart into a Slides presentation.
"""

import uuid

from deckbridge.renderers.common.style_resolver import resolve_chart_theme
from deckbridge.renderers.gslides.chart_builder import SheetsChartBuilder
from deckbridge.renderers.gslides.chart_embedder import SlidesChartEmbedder
from deckbridge.renderers.gslides.sheets_writer import SheetsDataWriter
from deckbridge.renderers.gslides.utils import text_to_number


class GSlidesChartCompiler:
    """Compiles chart data and embeds it into a Google Slides deck.

    The compiler performs the following steps for a chart block:
    1. Generates unique sheet and chart identifiers.
    2. Writes the chart's DataFrame to a new sheet.
    3. Creates a chart in the sheet via the Sheets API.
    4. Applies styling based on the theme and any overrides.
    5. Embeds the linked chart into the target slide.

    It leverages :class:`SheetsDataWriter`, :class:`SheetsChartBuilder`, and
    :class:`SlidesChartEmbedder` to orchestrate these actions.
    """

    def __init__(self, slides_service, sheets_service, spreadsheet_id):
        """Initializes the chart compiler.

        Args:
            slides_service: Authenticated Google Slides service instance.
            sheets_service: Authenticated Google Sheets service instance.
            spreadsheet_id (str): ID of the spreadsheet where chart data and
                charts will be created.
        """
        self.slides = slides_service
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

        self.writer = SheetsDataWriter(sheets_service, spreadsheet_id)
        self.chart_builder = SheetsChartBuilder(sheets_service, spreadsheet_id)
        self.embedder = SlidesChartEmbedder(slides_service)

    def compile(self, ctx, slot, block, slot_key, value_axis_override=None):
        """Compile a chart block and embed it into the slide.

        This method orchestrates the full lifecycle of a chart:
        1. Generates unique identifiers for the sheet and chart.
        2. Writes the chart's pandas ``DataFrame`` to a new sheet via
           :class:`SheetsDataWriter`.
        3. Creates a chart in the sheet using :class:`SheetsChartBuilder` and adds
           the corresponding ``createChart`` requests to the rendering context.
        4. Resolves and applies chart styling based on the current theme and any
           style overrides.
        5. Embeds the linked chart into the target slide using
           :class:`SlidesChartEmbedder`.

        Args:
            ctx: :class:`~deckbridge.renderers.common.context.RenderContext`
                instance that accumulates batchUpdate requests.
            slot: Dictionary describing the slot location and size on the slide.
            block: Chart block containing the ``chart`` definition and optional
                ``style_overrides``.
            slot_key (str): Unique key identifying the slot within the layout.
            value_axis_override (str, optional): Custom number format string for
                the value axis. If ``None`` the chart's default formatting is used.

        Returns:
            None. The method updates the ``ctx`` object with the necessary sheet,
            chart, and embed requests.
        """
        # -------------------------
        # Create ids
        # -------------------------
        sheet_name = f"{slot_key}_{uuid.uuid4().hex[:4]}"
        chart_id = text_to_number(f"{sheet_name}_chart")

        # -------------------------
        # Write sheet data
        # -------------------------
        sheet_name, sheet_id = self.writer.write_dataframe(ctx, block, sheet_name=sheet_name)

        # -------------------------
        # Create chart
        # -------------------------
        requests = self.chart_builder.create_chart(chart_id, sheet_id, block.chart, block, slot)
        ctx.add_create_chart_requests(requests)

        # -------------------------
        # Style chart
        # -------------------------
        chart_theme = resolve_chart_theme(ctx.theme, ctx.layout_spec.name, block.style_overrides)

        requests = self.chart_builder.apply_chart_style(
            sheet_id,
            chart_id,
            block,
            chart_theme,
            value_axis_override,
        )
        ctx.add_create_chart_requests(requests)

        # -------------------------
        # Embed in slide
        # -------------------------
        requests = self.embedder.embed_chart(self.spreadsheet_id, chart_id, ctx.page_id, slot)
        ctx.add_embed_chart_requests(requests)
