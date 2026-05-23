from .utils import text_to_number


class SheetsDataWriter:
    def __init__(self, sheets_service, spreadsheet_id):
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

    def write_dataframe(self, ctx, block, sheet_name):

        df = block.chart.data

        # Create new sheet
        sheet_id = text_to_number(sheet_name)
        ctx.add_create_sheet_requests({"addSheet": {"properties": {"sheetId": sheet_id, "title": sheet_name}}})

        # Write data
        series_names = [block.chart.x]
        df_names = [block.chart.x]
        for s in block.chart.series:
            series_names.append(s["name"])
            df_names.append(s["column"])
        values = [series_names] + df[df_names].values.tolist()

        ctx.add_create_values_requests(
            {
                "range": f"{sheet_name}!A1",
                "values": values,
            }
        )

        value_axis_tick_format = block.chart.value_axis_tick_format
        if value_axis_tick_format:
            ctx.add_format_values_requests(
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 1,  # skip header
                            "endRowIndex": len(df) + 1,
                            "startColumnIndex": 1,  # assuming y is col 1
                            "endColumnIndex": len(df.columns) + 1,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "numberFormat": {
                                    "type": "NUMBER",
                                    "pattern": value_axis_tick_format,
                                }
                            }
                        },
                        "fields": "userEnteredFormat.numberFormat",
                    }
                }
            )

        return sheet_name, sheet_id
