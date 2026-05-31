"""Google Drive folder management utilities.

This module defines :class:`DriveFolderManager`, a small helper class that
encapsulates common operations for locating or creating folders in Google
Drive. It is used by the Google Slides session creation code to ensure a
dedicated namespace exists for each Deckbridge execution.
"""


class DriveFolderManager:
    """Utility for retrieving or creating Google Drive folders.

    The manager works with a pre‑authenticated Drive service object (as
    returned by :func:`deckbridge.auth.google_auth.get_google_services`). It
    provides a thin wrapper around the Drive ``files().list`` and ``files().create``
    endpoints to guarantee that a folder with a given name (and optional parent)
    exists, returning its file ID.
    """

    def __init__(self, drive_service):
        """Create a new :class:`DriveFolderManager`.

        Args:
            drive_service: An authenticated ``googleapiclient.discovery.Resource``
                instance for the Drive API, typically obtained via
                :func:`deckbridge.auth.google_auth.get_google_services`.
        """
        self.drive = drive_service

    def get_or_create_folder(self, name, parent_id=None):
        """Retrieve the ID of a folder, creating it if it does not exist.

        The method searches for a non‑trashed folder with the specified ``name``
        (and optional ``parent_id``). If a matching folder is found, its file ID
        is returned. Otherwise, a new folder is created under the given parent (or
        at the root level) and the new folder's ID is returned.

        Args:
            name: The name of the folder to locate or create.
            parent_id: Optional Drive folder ID that should act as the parent for
                the folder. If ``None`` the folder is created at the top level.

        Returns:
            str: The Google Drive file ID of the existing or newly created folder.
        """
        # Build the query to find a folder with the given name that is not trashed.
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

        if parent_id:
            query += f" and '{parent_id}' in parents"

        results = self.drive.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])

        if files:
            return files[0]["id"]

        # Folder does not exist – create it.
        body = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_id:
            body["parents"] = [parent_id]

        folder = self.drive.files().create(body=body, fields="id").execute()
        return folder["id"]
