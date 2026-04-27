import uuid

from ...deck.specs import ChartSpec
from .chart_builder import SheetsChartBuilder
from .chart_embedder import SlidesChartEmbedder
from .sheets_writer import SheetsDataWriter


class GSlidesChartCompiler:
    def __init__(self, slides_service, sheets_service, spreadsheet_id):
        self.slides = slides_service
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

        self.writer = SheetsDataWriter(sheets_service, spreadsheet_id)
        self.chart_builder = SheetsChartBuilder(sheets_service, spreadsheet_id)
        self.embedder = SlidesChartEmbedder(slides_service)

    def compile(self, presentation_id, page_id, spec: ChartSpec, position: dict, chart_key: str):

        # Create unique sheet name
        sheet_name = f"{chart_key}_{uuid.uuid4().hex[:4]}"

        # Write data
        sheet_name, sheet_id = self.writer.write_dataframe(spec.data, sheet_name=sheet_name)

        # Create chart
        requests = self.chart_builder.create_chart(
            sheet_id,
            spec,
            position,
        )

        response = self.sheets.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body={"requests": requests}).execute()

        chart_id = response["replies"][0]["addChart"]["chart"]["chartId"]

        # Embed chart
        self.embedder.embed_chart(presentation_id, self.spreadsheet_id, chart_id, page_id, position)
