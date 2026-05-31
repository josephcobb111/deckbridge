"""Utilities for writing chart data to Google Sheets.

This module provides the :class:`SheetsDataWriter` which creates a new sheet
in a spreadsheet and writes a pandas ``DataFrame`` representing chart data to
it. The writer works with the surrounding rendering context to accumulate the
necessary batchUpdate requests for the Google Sheets API.
"""

from deckbridge.renderers.gslides.utils import text_to_number


class SheetsDataWriter:
    """Writes data to Google Sheets.

    This class handles creating new sheets in a spreadsheet and writing chart
    data (provided as a pandas DataFrame) to those sheets.
    """

    def __init__(self, sheets_service, spreadsheet_id):
        """Initializes the writer with a Google Sheets service.

        Args:
            sheets_service: Authenticated Google Sheets service instance used to
                send batchUpdate requests.
            spreadsheet_id: ID of the spreadsheet where new sheets will be
                created and data written.
        """
        self.sheets = sheets_service
        self.spreadsheet_id = spreadsheet_id

    def write_dataframe(self, ctx, block, sheet_name):
        """Writes a DataFrame to a new sheet in the spreadsheet.

        This creates a new sheet with a deterministic ``sheet_id`` derived from
        ``sheet_name`` and populates it with the chart data contained in
        ``block.chart``.

        Args:
            ctx: Context object that accumulates batchUpdate requests for the
                Sheets API. It must provide ``add_create_sheet_requests``,
                ``add_create_values_requests`` and ``add_format_values_requests``
                methods.
            block: A chart block that contains a ``chart`` attribute. The chart
                must have ``data`` (a pandas ``DataFrame``), ``x`` (name of the
                x‑axis column), ``series`` (list of series dictionaries with
                ``name`` and ``column`` keys), and optionally ``value_axis_tick
                _format`` for number formatting.
            sheet_name: Desired name of the new sheet.

        Returns:
            tuple: ``(sheet_name, sheet_id)`` where ``sheet_id`` is the numeric
                identifier used in subsequent formatting requests.
        """
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

        ctx.add_create_values_requests({"range": f"{sheet_name}!A1", "values": values})

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
