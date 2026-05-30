from deckbridge.backends.base import BaseBackend
from deckbridge.renderers.gslides.renderer import GSlidesRenderer


class GSlidesBackend(BaseBackend):
    def __init__(self, presentation_id, spreadsheet_id, slides_service, sheets_service, execute_requests=True):
        self.presentation_id = presentation_id
        self.spreadsheet_id = spreadsheet_id
        self.slides_service = slides_service
        self.sheets_service = sheets_service

        self.renderer = GSlidesRenderer(
            slides_service=slides_service,
            sheets_service=sheets_service,
            spreadsheet_id=spreadsheet_id,
            presentation_id=presentation_id,
            execute_requests=execute_requests,
        )

    def render(self, deck):
        self.renderer.theme = deck.config.theme
        self.renderer.layouts = deck.config.layouts

        self.renderer.render(deck)
