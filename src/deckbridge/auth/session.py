from datetime import datetime

from .drive_folders import DriveFolderManager
from .google_auth import get_google_services


def create_gslides_session(title: str = "Deckbridge Deck"):

    slides_service, sheets_service, drive_service = get_google_services()

    folder_mgr = DriveFolderManager(drive_service)

    # -----------------------
    # 1. Root folder
    # -----------------------
    root_folder_id = folder_mgr.get_or_create_folder("deckbridge")

    # -----------------------
    # 2. Run folder (unique per execution)
    # -----------------------
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_folder_name = f"{title}_{timestamp}"

    run_folder_id = folder_mgr.get_or_create_folder(run_folder_name, parent_id=root_folder_id)

    # -----------------------
    # 3. Create presentation
    # -----------------------
    presentation = slides_service.presentations().create(body={"title": title}).execute()

    presentation_id = presentation["presentationId"]

    # remove default slide
    default_slide_id = presentation["slides"][0]["objectId"]

    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": [{"deleteObject": {"objectId": default_slide_id}}]}
    ).execute()

    # move to Drive folder
    drive_service.files().update(fileId=presentation_id, addParents=run_folder_id, fields="id, parents").execute()

    # -----------------------
    # 4. Create spreadsheet
    # -----------------------
    spreadsheet = sheets_service.spreadsheets().create(body={"properties": {"title": f"{title} - Data"}}).execute()

    spreadsheet_id = spreadsheet["spreadsheetId"]

    # rename sheet tab
    sheet_id = spreadsheet["sheets"][0]["properties"]["sheetId"]

    sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": [{"updateSheetProperties": {"properties": {"sheetId": sheet_id, "title": "data"}, "fields": "title"}}]},
    ).execute()

    # move spreadsheet into folder
    drive_service.files().update(fileId=spreadsheet_id, addParents=run_folder_id, fields="id, parents").execute()

    # -----------------------
    # Return session
    # -----------------------
    return {
        "presentation_id": presentation_id,
        "spreadsheet_id": spreadsheet_id,
        "slides_service": slides_service,
        "sheets_service": sheets_service,
    }
