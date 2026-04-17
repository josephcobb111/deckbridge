from .google_auth import get_google_services


def create_gslides_session(title: str = "Deckbridge Deck"):
    """
    Creates:
    - Google Slides presentation
    - Google Sheet for charts
    - Authenticated services
    """

    slides_service, sheets_service = get_google_services()

    # -----------------------
    # 1. Create presentation
    # -----------------------
    presentation = slides_service.presentations().create(body={"title": title}).execute()

    presentation_id = presentation["presentationId"]

    # -----------------------
    # DELETE default slide
    # -----------------------
    default_slide_id = presentation["slides"][0]["objectId"]

    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": [{"deleteObject": {"objectId": default_slide_id}}]}
    ).execute()

    # -----------------------
    # 2. Create spreadsheet
    # -----------------------
    spreadsheet = sheets_service.spreadsheets().create(body={"properties": {"title": f"{title} - Data"}}).execute()

    spreadsheet_id = spreadsheet["spreadsheetId"]

    # -----------------------
    # RENAME default sheet
    # -----------------------
    sheet_id = spreadsheet["sheets"][0]["properties"]["sheetId"]

    sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": [{"updateSheetProperties": {"properties": {"sheetId": sheet_id, "title": "data"}, "fields": "title"}}]},
    ).execute()

    # -----------------------
    # Return fully wired session
    # -----------------------
    return {
        "presentation_id": presentation_id,
        "spreadsheet_id": spreadsheet_id,
        "slides_service": slides_service,
        "sheets_service": sheets_service,
    }
