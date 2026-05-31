from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RenderContext:
    """Manages the context for rendering presentations.

    This dataclass holds all necessary information and request queues
    for rendering a presentation using various backends (e.g., Google Slides).

    Attributes:
        backend: The rendering backend (e.g., 'google_slides').
        layout_spec: Specification for the presentation layout.
        theme: Dictionary containing theme-related information.
        slide_obj: The current slide object being rendered (backend-specific).
        sheets_service: API service client for Google Sheets.
        slides_service: API service client for Google Slides.
        presentation_id: ID of the presentation being rendered.
        spreadsheet_id: ID of the spreadsheet used for charts/data.
        page_id: ID of the current page/slide.
        chart_compiler: Object responsible for compiling chart data.
        create_sheet_requests: Queue for Google Sheets 'createSheet' requests.
        create_values_requests: Queue for Google Sheets 'updateCells' or 'appendCells' requests.
        format_values_requests: Queue for Google Sheets 'updateCells' requests related to formatting.
        create_chart_requests: Queue for Google Sheets 'addChart' requests.
        embed_chart_requests: Queue for Google Slides 'createImage' or 'createSheetsChart' requests.
        create_text_requests: Queue for Google Slides 'createText' requests.
        create_legend_requests: Queue for Google Slides 'createShape' requests for legends.
    """

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
        """Adds requests to create sheets.

        Args:
            requests: A single request object or a list of request objects.
        """
        if not requests:
            return

        if isinstance(requests, list):
            self.create_sheet_requests.extend(requests)
        else:
            self.create_sheet_requests.append(requests)

    def add_create_values_requests(self, requests):
        """Adds requests to create or update cell values in sheets.

        Args:
            requests: A single request object or a list of request objects.
        """
        if not requests:
            return

        if isinstance(requests, list):
            self.create_values_requests.extend(requests)
        else:
            self.create_values_requests.append(requests)

    def add_format_values_requests(self, requests):
        """Adds requests to format cell values in sheets.

        Args:
            requests: A single request object or a list of request objects.
        """
        if not requests:
            return

        if isinstance(requests, list):
            self.format_values_requests.extend(requests)
        else:
            self.format_values_requests.append(requests)

    def add_create_chart_requests(self, requests):
        """Adds requests to create charts in sheets.

        Args:
            requests: A single request object or a list of request objects.
        """
        if not requests:
            return

        if isinstance(requests, list):
            self.create_chart_requests.extend(requests)
        else:
            self.create_chart_requests.append(requests)

    def add_embed_chart_requests(self, requests):
        """Adds requests to embed charts in slides.

        Args:
            requests: A single request object or a list of request objects.
        """
        if not requests:
            return

        if isinstance(requests, list):
            self.embed_chart_requests.extend(requests)
        else:
            self.embed_chart_requests.append(requests)

    def add_create_text_requests(self, requests):
        """Adds requests to create text boxes in slides.

        Args:
            requests: A single request object or a list of request objects.
        """
        if not requests:
            return

        if isinstance(requests, list):
            self.create_text_requests.extend(requests)
        else:
            self.create_text_requests.append(requests)

    def add_create_legend_requests(self, requests):
        """Adds requests to create legend shapes in slides.

        Args:
            requests: A single request object or a list of request objects.
        """
        if not requests:
            return

        if isinstance(requests, list):
            self.create_legend_requests.extend(requests)
        else:
            self.create_legend_requests.append(requests)
