class SheetsDataWriter:
    def __init__(self, sheets_service, spreadsheet_id):
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

    def write_dataframe(self, block, sheet_name):

        df = block.chart.data

        # Create new sheet
        add_sheet_request = {"addSheet": {"properties": {"title": sheet_name}}}

        response = (
            self.sheets.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body={"requests": [add_sheet_request]}).execute()
        )

        sheet_id = response["replies"][0]["addSheet"]["properties"]["sheetId"]

        # Write data
        series_names = [block.chart.x]
        df_names = [block.chart.x]
        for s in block.chart.series:
            series_names.append(s["name"])
            df_names.append(s["column"])
        values = [series_names] + df[df_names].values.tolist()

        self.sheets.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=f"{sheet_name}!A1", valueInputOption="RAW", body={"values": values}
        ).execute()

        requests = []

        value_axis_tick_format = block.chart.value_axis_tick_format
        if value_axis_tick_format:
            requests.append(
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

        if requests:
            self.sheets.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={"requests": requests},
            ).execute()

        return sheet_name, sheet_id
