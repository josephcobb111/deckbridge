from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RenderContext:
    backend: str
    layout_spec: object
    theme: dict

    # Optional renderer-specific fields
    slide_obj: object = None
    sheets_service: object = None
    slides_service: object = None

    presentation_id: str = None
    spreadsheet_id: str = None
    page_id: str = None

    chart_compiler: object = None

    # Request queues
    sheet_requests: list = field(default_factory=list)
    slide_requests: list = field(default_factory=list)

    def add_sheet_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.sheet_requests.extend(requests)
        else:
            self.sheet_requests.append(requests)

    def add_slide_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.slide_requests.extend(requests)
        else:
            self.slide_requests.append(requests)
