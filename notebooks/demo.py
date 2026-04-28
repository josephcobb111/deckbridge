import pandas as pd

from deckbridge.auth.session import create_gslides_session
from deckbridge.backends.gslides_backend import GSlidesBackend
from deckbridge.backends.pptx_backend import PPTXBackend
from deckbridge.deck.blocks import ChartBlock
from deckbridge.deck.deck import Deck
from deckbridge.deck.specs import ChartSpec


def main():

    df = pd.DataFrame(
        {"month": ["Jan", "Feb", "Mar", "Apr"], "revenue": [10, 14, 9, 18]}
    )

    deck = Deck()

    # -----------------------
    # Title slide
    # -----------------------
    deck.add_slide(
        deck_title="Demo - deck_title", deck_author="deckbridge - deck_author"
    )

    # -----------------------
    # Chart slide
    # -----------------------
    chart1 = ChartSpec(
        chart_type="line",
        data=df,
        x="month",
        y="revenue",
    )

    chart2 = ChartSpec(
        chart_type="bar",
        data=df,
        x="month",
        y="revenue",
    )

    chart3 = ChartSpec(
        chart_type="line",
        data=df * 2,
        x="month",
        y="revenue",
    )

    deck.add_slide(
        slide_title="Revenue Trend - Slide Title",
        content={
            "chart_1": ChartBlock(chart=chart1, chart_title="Revenue Trend (Line) - Chart Title"),
        },
    )

    deck.add_slide(
        slide_title="Revenue Trend - Slide Title",
        content={
            "chart_1": ChartBlock(chart=chart1, chart_title="Revenue Trend (Line) - Chart Title"),
            "chart_2": ChartBlock(chart=chart2, chart_title="Revenue (Bar) - Chart Title"),
        },
    )

    deck.add_slide(
        slide_title="Revenue Trend - Slide Title",
        content={
            "chart_1": ChartBlock(chart=chart1, chart_title="Revenue Trend (Line) - Chart Title"),
            "chart_2": ChartBlock(chart=chart2, chart_title="Revenue (Bar) - Chart Title"),
            "chart_3": ChartBlock(chart=chart3, chart_title="Revenue Trend (Line) - Chart Title"),
        },
    )

    # -----------------------
    # Render PPTX
    # -----------------------
    deck.render(PPTXBackend("demo.pptx"))

    # -----------------------
    # Render Google Slides
    # -----------------------
    session = create_gslides_session("Q4 Deck")

    deck.render(GSlidesBackend(**session))


if __name__ == "__main__":
    main()
