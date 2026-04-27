from datetime import datetime

from deckbridge.config import DEFAULT_GSLIDES_TEMPLATE_ID

from .drive_folders import DriveFolderManager
from .google_auth import get_google_services


def copy_presentation_template(drive_service, template_id, new_title):
    file = drive_service.files().copy(fileId=template_id, body={"name": new_title}).execute()

    return file["id"]


def create_gslides_session(title: str = "Deckbridge Deck", template_id=None):

    slides_service, sheets_service, drive_service = get_google_services()

    folder_mgr = DriveFolderManager(drive_service)

    # -----------------------
    # Root folder
    # -----------------------
    root_folder_id = folder_mgr.get_or_create_folder("deckbridge")

    # -----------------------
    # Run folder (unique per execution)
    # -----------------------
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_folder_name = f"{title}_{timestamp}"

    run_folder_id = folder_mgr.get_or_create_folder(run_folder_name, parent_id=root_folder_id)

    # -----------------------
    # Create presentation
    # -----------------------
    if template_id is None:
        template_id = DEFAULT_GSLIDES_TEMPLATE_ID

    presentation_id = copy_presentation_template(drive_service, template_id, title)

    # move to Drive folder
    drive_service.files().update(fileId=presentation_id, addParents=run_folder_id, fields="id, parents").execute()

    # -----------------------
    # Create spreadsheet
    # -----------------------
    spreadsheet = sheets_service.spreadsheets().create(body={"properties": {"title": f"{title} - Data"}}).execute()

    spreadsheet_id = spreadsheet["spreadsheetId"]

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
