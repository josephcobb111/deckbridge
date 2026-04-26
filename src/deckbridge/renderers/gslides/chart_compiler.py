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

    def compile(self, presentation_id, page_id, spec: ChartSpec, slot):

        # 1. Write data to Sheets
        sheet = self.writer.write_dataframe(spec.data)

        # 2. Create chart in Sheets
        requests = self.chart_builder.create_chart(sheet, spec)

        response = self.sheets.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body={"requests": requests}).execute()

        chart_id = response["replies"][0]["addChart"]["chart"]["chartId"]

        # 3. Embed into Slides
        self.embedder.embed_chart(
            presentation_id,
            self.spreadsheet_id,
            chart_id,
            page_id,
            slot,  # 👈 NEW
        )
