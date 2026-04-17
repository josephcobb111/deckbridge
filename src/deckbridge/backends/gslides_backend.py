from ..renderers.gslides.renderer import GSlidesRenderer
from .base import BaseBackend


class GSlidesBackend(BaseBackend):
    def __init__(self, presentation_id, spreadsheet_id, slides_service, sheets_service):
        self.presentation_id = presentation_id
        self.spreadsheet_id = spreadsheet_id
        self.slides_service = slides_service
        self.sheets_service = sheets_service

        self.renderer = GSlidesRenderer(slides_service=slides_service, sheets_service=sheets_service, spreadsheet_id=spreadsheet_id)

    def render(self, deck):
        self.renderer.render(deck, self.presentation_id)
