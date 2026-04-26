from deckbridge.deck.deck import Deck
from deckbridge.backends.pptx_backend import PPTXBackend
from deckbridge.backends.gslides_backend import GSlidesBackend
from deckbridge.auth.session import create_gslides_session
from deckbridge.deck.specs import ChartSpec

import pandas as pd


def main():

    df = pd.DataFrame(
        {"month": ["Jan", "Feb", "Mar", "Apr"], "revenue": [10, 14, 9, 18]}
    )

    deck = Deck()

    # -----------------------
    # Title slide
    # -----------------------
    deck.add_title_slide("Demo - Title Slide", "Refactored Package - Author")

    # -----------------------
    # Chart slide (NEW API)
    # -----------------------
    chart = ChartSpec(
        chart_type="line",
        data=df,
        x="month",
        y="revenue",
        title="Revenue Trend - Chart Title"
    )

    deck.add_chart_slide(
        title="Revenue Trend - Slide Title",
        layout="one_chart",
        charts=[chart],
    )

    deck.add_chart_slide(
        title="Revenue Trend - Slide Title",
        layout="two_chart",
        charts=[chart, chart],
    )

    # -----------------------
    # Render PPTX
    # -----------------------
    deck.render(PPTXBackend("demo.pptx"))

    # -----------------------
    # Render Google Slides
    # -----------------------
    session = create_gslides_session("Q4 Deck")

    deck.render(
        GSlidesBackend(**session)
    )


if __name__ == "__main__":
    main()