import uuid

from deckbridge.renderers.common.style_resolver import resolve_chart_theme
from deckbridge.renderers.gslides.chart_builder import SheetsChartBuilder
from deckbridge.renderers.gslides.chart_embedder import SlidesChartEmbedder
from deckbridge.renderers.gslides.sheets_writer import SheetsDataWriter
from deckbridge.renderers.gslides.utils import text_to_number


class GSlidesChartCompiler:
    def __init__(self, slides_service, sheets_service, spreadsheet_id):
        self.slides = slides_service
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

        self.writer = SheetsDataWriter(sheets_service, spreadsheet_id)
        self.chart_builder = SheetsChartBuilder(sheets_service, spreadsheet_id)
        self.embedder = SlidesChartEmbedder(slides_service)

    def compile(self, ctx, slot, block, slot_key, value_axis_override=None):

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
        requests = self.embedder.embed_chart(ctx.presentation_id, self.spreadsheet_id, chart_id, ctx.page_id, slot)
        ctx.add_embed_chart_requests(requests)
