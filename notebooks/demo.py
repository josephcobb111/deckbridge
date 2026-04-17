from deckbridge.deck.deck import Deck
from deckbridge.backends.pptx_backend import PPTXBackend
from deckbridge.backends.gslides_backend import GSlidesBackend
from deckbridge.auth.session import create_gslides_session

import pandas as pd


def main():

    df = pd.DataFrame(
        {"month": ["Jan", "Feb", "Mar", "Apr"], "revenue": [10, 14, 9, 18]}
    )

    deck = Deck()

    deck.add_title_slide("Demo", "Refactored Package")
    deck.add_chart_slide("Revenue Trend", "line", df, "month", "revenue")

    deck.render(PPTXBackend("demo.pptx"))

    session = create_gslides_session("Q4 Deck")
    deck.render(GSlidesBackend(**session))


if __name__ == "__main__":
    main()
