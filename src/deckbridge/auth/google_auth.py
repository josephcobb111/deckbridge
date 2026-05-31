"""Utilities for authenticating Google API services.

This module handles OAuth2 credential management for Google Slides, Sheets, and
Drive APIs. It loads cached credentials from ``token.pickle`` when available
and refreshes or obtains new credentials as needed, then builds the service
objects required by the rest of the Deckbridge codebase.
"""

import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes required for the Deckbridge Google Slides backend.
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_google_services():
    """Create and return authenticated Google API service objects.

    The function performs the following steps:

    1. Load cached OAuth2 credentials from ``token.pickle`` if the file exists.
    2. Refresh expired credentials automatically, or run the OAuth flow to
       obtain fresh credentials using ``credentials.json``.
    3. Persist any new or refreshed credentials back to ``token.pickle`` for
       future reuse.
    4. Build and return service objects for Google Slides, Sheets, and Drive.

    Returns:
        tuple: ``(slides_service, sheets_service, drive_service)`` where each
        element is a ``googleapiclient.discovery.Resource`` instance configured
        with the authenticated credentials.
    """
    creds = None

    # Load cached credentials if present.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # Refresh or obtain new credentials as necessary.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run.
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # Build the service objects.
    slides_service = build("slides", "v1", credentials=creds)
    sheets_service = build("sheets", "v4", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    return slides_service, sheets_service, drive_service
