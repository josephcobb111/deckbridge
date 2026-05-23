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

    # object IDs
    next_sheet_id: int = 1000
    next_chart_id: int = 1000

    # Request queues
    create_sheet_requests: list = field(default_factory=list)
    create_values_requests: list = field(default_factory=list)
    format_values_requests: list = field(default_factory=list)
    create_chart_requests: list = field(default_factory=list)

    sheet_requests: list = field(default_factory=list)
    sheet_values: list = field(default_factory=list)
    slide_requests: list = field(default_factory=list)

    def allocate_sheet_id(self):
        sheet_id = self.next_sheet_id
        self.next_sheet_id += 1
        return sheet_id

    def allocate_chart_id(self):
        chart_id = self.next_chart_id
        self.next_chart_id += 1
        return chart_id

    def add_create_sheet_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.create_sheet_requests.extend(requests)
        else:
            self.create_sheet_requests.append(requests)

    def add_create_values_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.create_values_requests.extend(requests)
        else:
            self.create_values_requests.append(requests)

    def add_format_values_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.format_values_requests.extend(requests)
        else:
            self.format_values_requests.append(requests)

    def add_create_chart_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.create_chart_requests.extend(requests)
        else:
            self.create_chart_requests.append(requests)

    def add_sheet_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.sheet_requests.extend(requests)
        else:
            self.sheet_requests.append(requests)

    def add_sheet_values(self, values):
        self.sheet_values.append(values)

    def add_slide_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.slide_requests.extend(requests)
        else:
            self.slide_requests.append(requests)
