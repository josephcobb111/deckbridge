"""Google Slides session creation utilities.

This module provides helper functions for creating a Google Slides presentation
and an associated Google Sheets spreadsheet within a dedicated folder in Google
Drive. The session information (service objects and resource IDs) is returned
as a dictionary for use by the :class:`~deckbridge.backends.gslides_backend.GSlidesBackend`.
"""

from datetime import datetime

from deckbridge.auth.drive_folders import DriveFolderManager
from deckbridge.auth.google_auth import get_google_services
from deckbridge.config import DEFAULT_GSLIDES_TEMPLATE_ID


def copy_presentation_template(drive_service, template_id, new_title):
    """Copy a Google Slides template file.

    This function uses the Google Drive ``files().copy`` endpoint to duplicate a
    Slides template and give the new file the supplied title.

    Args:
        drive_service: An authenticated ``googleapiclient.discovery.Resource``
            instance for the Drive API.
        template_id: The file ID of the Slides template to copy.
        new_title: The desired title for the new presentation.

    Returns:
        str: The file ID of the newly created Slides presentation.
    """
    file = drive_service.files().copy(fileId=template_id, body={"name": new_title}).execute()
    return file["id"]


def create_gslides_session(title: str = "Deckbridge Deck", template_id=None):
    """Create a Google Slides session with a new presentation and spreadsheet.

    The function performs the following steps:

    1. Obtain authenticated Google Slides, Sheets, and Drive service objects.
    2. Ensure a top‑level ``deckbridge`` folder exists in Drive.
    +   3. Create a timestamped sub‑folder for this execution of Deckbridge.
    +   4. Copy the Slides template (or the default one) into the new folder.
    +   5. Create a blank Sheets spreadsheet for data‑driven charts.
    +   6. Move both the presentation and spreadsheet into the execution folder.
    +
    The resulting identifiers and service objects are returned for downstream
    rendering.

    Args:
        title: Human‑readable base title for the presentation and the run
            folder. Defaults to ``"Deckbridge Deck"``.
        template_id: Optional Google Slides file ID to use as the template. If
            omitted, :data:`deckbridge.config.DEFAULT_GSLIDES_TEMPLATE_ID` is
            used.

    Returns:
        dict: A mapping containing the following keys:

        - ``presentation_id`` (str): ID of the created Slides presentation.
        - ``spreadsheet_id`` (str): ID of the created Sheets spreadsheet.
        - ``slides_service``: Authenticated Slides service object.
        - ``sheets_service``: Authenticated Sheets service object.
    """
    # Get authenticated Google API service objects.
    slides_service, sheets_service, drive_service = get_google_services()

    # Initialise a manager for handling Drive folder hierarchy.
    folder_mgr = DriveFolderManager(drive_service)

    # ---------------------------------------------------------------------
    # Root folder ("deckbridge") – created if it does not already exist.
    # ---------------------------------------------------------------------
    root_folder_id = folder_mgr.get_or_create_folder("deckbridge")

    # ---------------------------------------------------------------------
    # Run‑specific folder – unique per execution, includes a timestamp.
    # ---------------------------------------------------------------------
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_folder_name = f"{title}_{timestamp}"
    run_folder_id = folder_mgr.get_or_create_folder(run_folder_name, parent_id=root_folder_id)

    # ---------------------------------------------------------------------
    # Presentation – copy the template (or default) into the new folder.
    # ---------------------------------------------------------------------
    if template_id is None:
        template_id = DEFAULT_GSLIDES_TEMPLATE_ID
    presentation_id = copy_presentation_template(drive_service, template_id, title)
    # Move the newly created presentation into the run folder.
    drive_service.files().update(fileId=presentation_id, addParents=run_folder_id, fields="id, parents").execute()

    # ---------------------------------------------------------------------
    # Spreadsheet – create a blank spreadsheet for chart data.
    # ---------------------------------------------------------------------
    spreadsheet = sheets_service.spreadsheets().create(body={"properties": {"title": f"{title} - Data"}}).execute()
    spreadsheet_id = spreadsheet["spreadsheetId"]
    # Move the spreadsheet into the same run folder.
    drive_service.files().update(fileId=spreadsheet_id, addParents=run_folder_id, fields="id, parents").execute()

    # Return a convenient dictionary for downstream use.
    return {
        "presentation_id": presentation_id,
        "spreadsheet_id": spreadsheet_id,
        "slides_service": slides_service,
        "sheets_service": sheets_service,
    }
