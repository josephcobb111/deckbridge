class DriveFolderManager:
    def __init__(self, drive_service):
        self.drive = drive_service

    def get_or_create_folder(self, name, parent_id=None):
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

        if parent_id:
            query += f" and '{parent_id}' in parents"

        results = self.drive.files().list(q=query, fields="files(id, name)").execute()

        files = results.get("files", [])

        if files:
            return files[0]["id"]

        body = {"name": name, "mimeType": "application/vnd.google-apps.folder"}

        if parent_id:
            body["parents"] = [parent_id]

        folder = self.drive.files().create(body=body, fields="id").execute()
        return folder["id"]
