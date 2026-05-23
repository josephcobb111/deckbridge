import pandas as pd

from deckbridge.auth.session import create_gslides_session
from deckbridge.backends.gslides_backend import GSlidesBackend
from deckbridge.backends.pptx_backend import PPTXBackend
from deckbridge.deck.blocks import ChartBlock
from deckbridge.deck.deck import Deck, DeckConfig
from deckbridge.deck.specs import ChartSpec

from deckbridge.themes.default import THEME
from deckbridge.layouts.registry import LAYOUTS
from deckbridge.deck.specs import LayoutSpec


def main():

    df = pd.DataFrame(
        {
            "month": ["Jan", "Feb", "Mar", "Apr"],
            "revenue": [10, 14, 9, 18],
            "cost": [2, 4, 3, 1],
        }
    )

    custom_theme = THEME
    custom_theme["slots"]["deck_title"]["font_size"] = 44
    custom_theme["chart"]["layouts"]["four_chart"] = {
        "chart_title": {"font_size": 12},
        "chart_subtitle": {"font_size": 10},
    }

    custom_layouts = LAYOUTS
    custom_layouts["four_chart"] = LayoutSpec(
        name="four_chart",
        slots={
            # Slide title
            "slide_title": {"type": "text", "x": 0.5, "y": 0.1, "w": 12.5, "h": 0.8},
            # Chart 1
            "chart_1": {"type": "chart", "x": 0.5, "y": 1.6, "w": 3.13, "h": 5.25},
            "chart_1_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_1",
                "x": 0.5,
                "y": 1.1,
                "w": 3.13,
                "h": 0.5,
            },
            # Chart 2
            "chart_2": {"type": "chart", "x": 3.63, "y": 1.6, "w": 3.13, "h": 5.25},
            "chart_2_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_2",
                "x": 3.63,
                "y": 1.1,
                "w": 3.13,
                "h": 0.5,
            },
            # Chart 3
            "chart_3": {"type": "chart", "x": 6.76, "y": 1.6, "w": 3.13, "h": 5.25},
            "chart_3_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_3",
                "x": 6.76,
                "y": 1.1,
                "w": 3.13,
                "h": 0.5,
            },
            # Chart 4
            "chart_4": {"type": "chart", "x": 9.89, "y": 1.6, "w": 3.13, "h": 5.25},
            "chart_4_title": {
                "type": "text",
                "content_type": "chart_title",
                "style_key": "chart_title",
                "source": "chart_4",
                "x": 9.89,
                "y": 1.1,
                "w": 3.13,
                "h": 0.5,
            },
            "color_legend": {
                "type": "color_legend",
                "style_key": "color_legend",
                "x": 7.5,
                "y": 6.85,
                "w": 2.0,
                "h": 1.0,
            },
            "dash_legend": {
                "type": "dash_legend",
                "style_key": "dash_legend",
                "x": 11,
                "y": 1.0,
                "w": 2.0,
                "h": 0.8,
            },
            "notes": {"type": "text", "x": 0.5, "y": 6.85, "w": 12.5, "h": 0.4},
        },
    )

    deck = Deck(
        config=DeckConfig(
            theme=custom_theme,
            layouts=custom_layouts,
        )
    )

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
        series=[
            {
                "column": "revenue",
                "name": "Revenue!",
                "color": "#C00000",
                "dash_style": "solid",
            },
            {"column": "cost", "name": "Cost!", "color": "#7030A0"},
        ],
        value_axis_range=(0, 100),
        value_axis_tick_format="$0.0",
    )

    chart2 = ChartSpec(
        chart_type="bar",
        data=df,
        x="month",
        y=["revenue", "cost"],
        value_axis_tick_format="0.0%",
        show_data_labels=True,
    )

    chart3 = ChartSpec(
        chart_type="line",
        data=df * 2,
        x="month",
        y="revenue",
    )

    chart4 = ChartSpec(
        chart_type="line",
        data=df,
        x="month",
        series=[
            {"column": "revenue", "name": "Revenue!"},
            {"column": "cost", "name": "Cost!"},
        ],
        value_axis_range=(0, 100),
        value_axis_tick_format="$0.0",
    )

    long_data = df.melt(id_vars="month")
    long_data["variable"] = pd.Categorical(
        long_data["variable"], categories=["revenue", "cost"], ordered=True
    )
    long_data.sort_values("variable", inplace=True)

    chart5 = ChartSpec(
        chart_type="line",
        data=long_data,
        x="month",
        y="value",
        series_field="variable",
        data_format="long",
        value_axis_range=(0, 100),
        value_axis_tick_format="$0.0",
    )

    chart6 = ChartSpec(
        chart_type="line",
        data=df.melt(id_vars="month"),
        x="month",
        y="value",
        series=[
            {"column": "revenue", "name": "Revenue!"},
            {"column": "cost", "name": "Cost!"},
        ],
        series_field="variable",
        data_format="long",
        value_axis_range=(0, 100),
        value_axis_tick_format="$0.0",
    )

    chart7 = ChartSpec(
        chart_type="area_stacked",
        data=df,
        x="month",
        series=[
            {
                "column": "revenue",
                "name": "Revenue!",
                "color": "#C00000",
                "dash_style": "solid",
            },
            {"column": "cost", "name": "Cost!", "color": "#7030A0"},
        ],
        value_axis_range=(0, 100),
        value_axis_tick_format="$0.0",
    )

    chart8 = ChartSpec(
        chart_type="area_stacked_100",
        data=df,
        x="month",
        series=[
            {
                "column": "revenue",
                "name": "Revenue!",
                "color": "#C00000",
                "dash_style": "solid",
            },
            {"column": "cost", "name": "Cost!", "color": "#7030A0"},
        ],
        value_axis_range=(0, 1),
        value_axis_tick_format="0%",
    )

    chart9 = ChartSpec(
        chart_type="bar_stacked",
        data=df,
        x="month",
        series=[
            {
                "column": "revenue",
                "name": "Revenue!",
                "color": "#C00000",
                "dash_style": "solid",
            },
            {"column": "cost", "name": "Cost!", "color": "#7030A0"},
        ],
        value_axis_range=(0, 100),
        value_axis_tick_format="$0.0",
    )

    chart10 = ChartSpec(
        chart_type="column_stacked",
        data=df,
        x="month",
        series=[
            {
                "column": "revenue",
                "name": "Revenue!",
                "color": "#C00000",
                "dash_style": "solid",
            },
            {"column": "cost", "name": "Cost!", "color": "#7030A0"},
        ],
        value_axis_range=(0, 100),
        value_axis_tick_format="$0.0",
    )

    scatter_df = df.copy()
    scatter_df["month"] = scatter_df["month"].replace(
        {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3}
    )
    chart11 = ChartSpec(
        chart_type="scatter",
        data=scatter_df,
        x="month",
        series=[
            {
                "column": "revenue",
                "name": "Revenue!",
                "color": "#C00000",
                "dash_style": "solid",
            },
            {"column": "cost", "name": "Cost!", "color": "#7030A0"},
        ],
        value_axis_range=(0, 100),
        value_axis_tick_format="$0.0",
    )

    deck.add_slide(
        slide_title="Revenue Trend - Slide Title",
        content={
            "chart_1": ChartBlock(
                chart=chart1,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
        },
        color_legend=[
            {
                "label": "Revenue",
                "color": "#C00000",
            },
            {
                "label": "Cost",
                "color": "#7030A0",
            },
            {
                "label": "Revenue",
                "color": "#C00000",
            },
            {
                "label": "Cost",
                "color": "#7030A0",
            },
        ],
        dash_legend=[
            {
                "label": "Revenue",
                "dash_style": "solid",
                "color": "#C00000",
            },
            {
                "label": "Cost",
                "dash_style": "dash",
                "color": "#7030A0",
            },
        ],
        notes="Notes: Adjusted for recent acquisitions.",
    )

    deck.add_slide(
        slide_title="Revenue Trend - Slide Title",
        content={
            "chart_1": ChartBlock(
                chart=chart1,
                chart_title="Revenue Trend (Line) - Chart Title",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_2": ChartBlock(
                chart=chart2,
                chart_title="Revenue (Bar) - Chart Title",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
        },
    )

    deck.add_slide(
        slide_title="Revenue Trend - Slide Title",
        content={
            "chart_1": ChartBlock(
                chart=chart1,
                chart_title="Revenue Trend (Line) - Chart Title",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_2": ChartBlock(
                chart=chart2,
                chart_title="Revenue (Bar) - Chart Title",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_3": ChartBlock(
                chart=chart3,
                chart_title="Revenue Trend (Line) - Chart Title",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
        },
    )

    deck.add_slide(
        slide_title="These should all be the same (except for legend names)",
        content={
            "chart_1": ChartBlock(
                chart=chart4,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_2": ChartBlock(
                chart=chart5,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_3": ChartBlock(
                chart=chart6,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
        },
        notes="Notes: Adjusted for recent acquisitions.",
    )

    deck.add_slide(
        slide_title="These should all be the same (except for legend names)",
        content={
            "chart_1": ChartBlock(
                chart=chart4,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_2": ChartBlock(
                chart=chart5,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_3": ChartBlock(
                chart=chart6,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
        },
        sync_value_axis=True,
        notes="Notes: Adjusted for recent acquisitions.",
    )

    deck.add_slide(
        slide_title="These should all be the same (except for legend names)",
        content={
            "chart_1": ChartBlock(
                chart=chart4,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_2": ChartBlock(
                chart=chart5,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_3": ChartBlock(
                chart=chart6,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
        },
        sync_value_axis=(0, 30),
        notes="Notes: Adjusted for recent acquisitions.",
    )

    deck.add_slide(
        slide_title="These should all be the same (except for legend names)",
        layout="four_chart",
        content={
            "chart_1": ChartBlock(
                chart=chart4,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_2": ChartBlock(
                chart=chart5,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_3": ChartBlock(
                chart=chart6,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
            "chart_4": ChartBlock(
                chart=chart6,
                chart_title="Revenue Trend (Line) - Chart Title",
                chart_subtitle="2024 Actuals",
                value_axis_title="Month",
                category_axis_title="Revenue",
            ),
        },
        sync_value_axis=(0, 30),
        notes="Notes: Adjusted for recent acquisitions.",
    )

    deck.add_slide(
        slide_title="Revenue Trend - Slide Title",
        layout="four_chart",
        content={
            "chart_1": ChartBlock(chart=chart7),
            "chart_2": ChartBlock(chart=chart8),
            "chart_3": ChartBlock(chart=chart9),
            "chart_4": ChartBlock(chart=chart10),
        },
    )

    deck.add_slide(
        slide_title="Revenue Trend - Slide Title",
        content={
            "chart_1": ChartBlock(chart=chart11),
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
