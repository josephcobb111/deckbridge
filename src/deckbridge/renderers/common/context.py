from dataclasses import dataclass
from typing import Optional


@dataclass
class RenderContext:
    backend: str  # "pptx" | "gslides"

    # Shared
    layout_spec: Optional[object] = None

    # PPTX
    slide_obj: Optional[object] = None

    # GSlides
    slides_service: Optional[object] = None
    presentation_id: Optional[str] = None
    page_id: Optional[str] = None

    # Shared utilities
    chart_compiler: Optional[object] = None
