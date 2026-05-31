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

    presentation_id: Optional[str] = None
    spreadsheet_id: Optional[str] = None
    page_id: Optional[str] = None

    chart_compiler: object = None

    # Request queues - sheets
    create_sheet_requests: list = field(default_factory=list)
    create_values_requests: list = field(default_factory=list)
    format_values_requests: list = field(default_factory=list)
    create_chart_requests: list = field(default_factory=list)

    # Request queues - slides
    embed_chart_requests: list = field(default_factory=list)
    create_text_requests: list = field(default_factory=list)
    create_legend_requests: list = field(default_factory=list)

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

    def add_embed_chart_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.embed_chart_requests.extend(requests)
        else:
            self.embed_chart_requests.append(requests)

    def add_create_text_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.create_text_requests.extend(requests)
        else:
            self.create_text_requests.append(requests)

    def add_create_legend_requests(self, requests):
        if not requests:
            return

        if isinstance(requests, list):
            self.create_legend_requests.extend(requests)
        else:
            self.create_legend_requests.append(requests)
