class SheetsDataWriter:
    def __init__(self, sheets_service, spreadsheet_id):
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

    def write_dataframe(self, df, sheet_name):

        # 1. Create new sheet
        add_sheet_request = {"addSheet": {"properties": {"title": sheet_name}}}

        response = (
            self.sheets.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body={"requests": [add_sheet_request]}).execute()
        )

        sheet_id = response["replies"][0]["addSheet"]["properties"]["sheetId"]

        # 2. Write data
        values = [df.columns.tolist()] + df.values.tolist()

        self.sheets.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=f"{sheet_name}!A1", valueInputOption="RAW", body={"values": values}
        ).execute()

        return sheet_name, sheet_id
