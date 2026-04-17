class SheetsDataWriter:
    def __init__(self, sheets_service, spreadsheet_id):
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

    def write_dataframe(self, df, sheet_name="data"):
        values = [df.columns.tolist()] + df.values.tolist()

        body = {"values": values}

        self.sheets.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=f"{sheet_name}!A1", valueInputOption="RAW", body=body
        ).execute()

        return sheet_name
