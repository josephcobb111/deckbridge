from deckbridge.auth.google_auth import get_google_services


def list_charts(service, spreadsheet_id):
    response = (
        service.spreadsheets()
        .get(spreadsheetId=spreadsheet_id, includeGridData=False)
        .execute()
    )

    charts_info = []

    for sheet in response.get("sheets", []):
        sheet_title = sheet["properties"]["title"]
        sheet_id = sheet["properties"]["sheetId"]

        for chart in sheet.get("charts", []):
            chart_id = chart["chartId"]
            title = chart.get("spec", {}).get("title", "(no title)")

            charts_info.append(
                {
                    "chart_id": chart_id,
                    "sheet_title": sheet_title,
                    "sheet_id": sheet_id,
                    "title": title,
                }
            )

    return charts_info


def update_chart_title(service, spreadsheet_id, chart_id, new_title):
    requests = [
        {"updateChartSpec": {"chartId": chart_id, "spec": {"title": new_title}}}
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": requests}
    ).execute()


def main():
    spreadsheet_id = "1WbFTKiGjGwzNmyP-DbloC0xK8uSLQOLvA6q2Xfr3vYI"
    service = get_google_services()[1]

    charts = list_charts(service, spreadsheet_id)

    if not charts:
        print("No charts found.")
        return

    print("\nAvailable charts:\n")
    for i, c in enumerate(charts):
        print(
            f"{i}: Sheet='{c['sheet_title']}' | "
            f"ChartID={c['chart_id']} | Title='{c['title']}'"
        )

    chart_id_to_find = 126902406

    response = (
        service.spreadsheets()
        .get(spreadsheetId=spreadsheet_id, includeGridData=False)
        .execute()
    )
    for sheet in response.get("sheets", []):
        for chart in sheet.get("charts", []):
            if chart["chartId"] == chart_id_to_find:
                print("Found it!")
                print(chart["spec"])

    # example basicChart spec
    # {
    #     "basicChart": {
    #         "chartType": "LINE",
    #         "legendPosition": "BOTTOM_LEGEND",
    #         "axis": [
    #             {
    #                 "position": "BOTTOM_AXIS",
    #                 "title": "month",
    #                 "format": {"fontFamily": "Roboto", "fontSize": 14},
    #                 "viewWindowOptions": {},
    #             },
    #             {
    #                 "position": "LEFT_AXIS",
    #                 "title": "revenue",
    #                 "format": {"fontFamily": "Roboto", "fontSize": 14},
    #                 "viewWindowOptions": {},
    #             },
    #         ],
    #         "domains": [
    #             {
    #                 "domain": {
    #                     "sourceRange": {
    #                         "sources": [
    #                             {
    #                                 "sheetId": 1874146428,
    #                                 "startRowIndex": 0,
    #                                 "endRowIndex": 5,
    #                                 "startColumnIndex": 0,
    #                                 "endColumnIndex": 1,
    #                             }
    #                         ]
    #                     }
    #                 }
    #             }
    #         ],
    #         "series": [
    #             {
    #                 "series": {
    #                     "sourceRange": {
    #                         "sources": [
    #                             {
    #                                 "sheetId": 1874146428,
    #                                 "startRowIndex": 0,
    #                                 "endRowIndex": 5,
    #                                 "startColumnIndex": 1,
    #                                 "endColumnIndex": 2,
    #                             }
    #                         ]
    #                     }
    #                 },
    #                 "targetAxis": "LEFT_AXIS",
    #                 "dataLabel": {
    #                     "type": "NONE",
    #                     "textFormat": {"fontFamily": "Roboto"},
    #                 },
    #             }
    #         ],
    #         "headerCount": 1,
    #     },
    #     "hiddenDimensionStrategy": "SKIP_HIDDEN_ROWS_AND_COLUMNS",
    #     "fontName": "Roboto",
    # }


if __name__ == "__main__":
    main()
