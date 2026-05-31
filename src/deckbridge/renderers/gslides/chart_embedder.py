"""Utilities for embedding a Google Sheets chart into a Google Slides slide.

This module provides :class:`SlidesChartEmbedder`, which builds the request payload
required by the Slides API to create a linked chart element on a specific slide.
"""

from deckbridge.renderers.gslides.utils import inches_to_emu


class SlidesChartEmbedder:
    """Embeds a Sheets chart into a Google Slides presentation.

    This helper builds the request payload required by the Slides API to
    create a linked chart object on a specific slide page. The resulting request
    list can be merged into the batchUpdate calls managed by
    :class:`~deckbridge.renderers.gslides.renderer.GSlidesRenderer`.
    """

    def __init__(self, slides_service):
        """Initializes the embedder with a Slides service.

        Args:
            slides_service: Authenticated Google Slides service instance used to
                send batchUpdate requests for embedding charts.
        """
        self.slides = slides_service

    def embed_chart(self, spreadsheet_id, chart_id, page_id, position):
        """Create a request to embed a linked Sheets chart in a slide.

        The method constructs the JSON payload required for a ``createSheetsChart``
        request in the Slides API. The chart is linked to the source sheet so that
        updates to the sheet are reflected in the presentation automatically.

        Args:
            spreadsheet_id (str): ID of the Google Spreadsheet containing the chart.
            chart_id (int): Identifier of the chart within the spreadsheet.
            page_id (str): ID of the slide page where the chart should be placed.
            position (dict): Mapping with keys ``x``, ``y``, ``w``, ``h`` specifying
                the chart's top‑left corner (in inches) and its width/height (in
                inches). These values are converted to EMU units using
                :func:`~deckbridge.renderers.gslides.utils.inches_to_emu`.

        Returns:
            list[dict]: A list containing a single ``createSheetsChart`` request
                dictionary that can be added to the batchUpdate payload.
        """
        requests = [
            {
                "createSheetsChart": {
                    "spreadsheetId": spreadsheet_id,
                    "chartId": chart_id,
                    "linkingMode": "LINKED",
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {
                            "height": {"magnitude": inches_to_emu(position["h"]), "unit": "EMU"},
                            "width": {"magnitude": inches_to_emu(position["w"]), "unit": "EMU"},
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": inches_to_emu(position["x"]),
                            "translateY": inches_to_emu(position["y"]),
                            "unit": "EMU",
                        },
                    },
                },
            },
        ]

        return requests
