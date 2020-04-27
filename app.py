# import statements
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import flask_caching

# read csv file of hotel booking data
# create dash app
external_stylesheets = ["https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# cache app
cache = flask_caching.Cache(
    server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache-directory"}
)

TIMEOUT = 60

# pull data
@cache.memoize(timeout=TIMEOUT)
def hotel_data():
    return pd.read_csv(
        "https://raw.githubusercontent.com/mfarris/hotel_data/master/hotel_bookings.csv"
    )


# base config
config = dict({"scrollZoom": True})

# create layout for app
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Hotel Booking Demand</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
app.layout = html.Section(
    [
        html.Div(
            [
                html.H1("Hotel Booking Demand", className="title"),
                html.H2("M. Farris | Dev Project | IT 7113 Data Visualization"),
            ],
            className="container is-fluid has-text-centered",
        ),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    "Country Measure",
                                                    className="title is-6",
                                                ),
                                                dcc.Dropdown(
                                                    id="country_measure",
                                                    options=[
                                                        {
                                                            "label": i.replace(
                                                                "_", " "
                                                            ).title(),
                                                            "value": i,
                                                        }
                                                        for i in [
                                                            "lead_time",
                                                            "stays_in_weekend_nights",
                                                            "stays_in_week_nights",
                                                            "booking_changes",
                                                            "days_in_waiting_list",
                                                            "total_of_special_requests",
                                                        ]
                                                    ],
                                                    value="lead_time",
                                                ),
                                            ]
                                        )
                                    ],
                                    className="tile is-child",
                                    style={"padding-right": "25px"},
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    "Parking Measure",
                                                    className="title is-6",
                                                ),
                                                dcc.Dropdown(
                                                    id="parking_measure",
                                                    options=[
                                                        {
                                                            "label": i.replace(
                                                                "_", " "
                                                            ).title(),
                                                            "value": i,
                                                        }
                                                        for i in [
                                                            "hotel",
                                                            "country",
                                                            "market_segment",
                                                            "distribution_channel",
                                                            "company",
                                                        ]
                                                    ],
                                                    value="hotel",
                                                ),
                                            ]
                                        )
                                    ],
                                    className="tile is-child",
                                    style={
                                        "padding-right": "25px",
                                        "padding-left": "25px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    "Weekends or Weekdays",
                                                    className="title is-6",
                                                ),
                                                dcc.RadioItems(
                                                    id="market_measure",
                                                    options=[
                                                        {
                                                            "label": f" {i.replace('_', ' ').title()} ",
                                                            "value": i,
                                                        }
                                                        for i in [
                                                            "stays_in_week_nights",
                                                            "stays_in_weekend_nights",
                                                        ]
                                                    ],
                                                    value="stays_in_week_nights",
                                                ),
                                            ]
                                        )
                                    ],
                                    className="tile is-child",
                                    style={"padding-left": "25px"},
                                ),
                            ],
                            className="tile is-parent",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            ["Country Map of Guests"],
                                            className="title is-4",
                                        ),
                                        dcc.Graph(id="id_countries", config=config),
                                    ],
                                    className="tile is-child has-text-centered",
                                )
                            ],
                            className="tile is-parent box",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            ["Average Stays per Market Segment"],
                                            className="title is-4",
                                        ),
                                        dcc.Graph(id="id_market", config=config),
                                    ],
                                    className="tile is-child has-text-centered",
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            ["Total Required Parking Spaces"],
                                            className="title is-4",
                                        ),
                                        dcc.Graph(id="id_parking", config=config),
                                    ],
                                    className="tile is-child has-text-centered",
                                ),
                            ],
                            className="tile is-parent box",
                        ),
                    ],
                    className="tile is-vertical is-ancestor",
                )
            ],
            className="container is-fluid",
        ),
    ],
    className="section",
)

# callbacks
@app.callback(Output("id_countries", "figure"), [Input("country_measure", "value")])
def update_countries(country_measure):
    return go.Figure(
        data=go.Choropleth(
            locations=hotel_data()["country"],
            z=hotel_data()[country_measure],
            colorscale="Blues",
            autocolorscale=False,
            reversescale=True,
            marker_line_color="darkgray",
            marker_line_width=0.5,
            colorbar_title=f"<b>{country_measure.replace('_', ' ').title()}</b>",
        ),
        layout=go.Layout(
            geo=dict(showframe=False, showcoastlines=False),
            margin={"r": 10, "t": 10, "l": 10, "b": 10},
        ),
    )


@app.callback(Output("id_parking", "figure"), [Input("parking_measure", "value")])
def update_parking(parking_measure):
    pie_colors = ["#1f77b4", "#17becf"]
    piv_parking = pd.pivot_table(
        hotel_data(),
        values="required_car_parking_spaces",
        index=parking_measure,
        aggfunc="sum",
    )
    pie_d = {}
    for i in piv_parking.index:
        pie_d[i] = piv_parking["required_car_parking_spaces"].xs(i)
    return go.Figure(
        data=[
            go.Pie(
                labels=[i for i in pie_d.keys()],
                values=[pie_d[i] for i in pie_d],
                hole=0.3,
                hoverinfo="label+percent",
                textinfo="value",
                textfont_size=20,
                marker=dict(colors=pie_colors, line=dict(color="#FFFFFF", width=2)),
            )
        ],
        layout=go.Layout(margin={"r": 10, "t": 10, "l": 10, "b": 10}),
    )


@app.callback(Output("id_market", "figure"), [Input("market_measure", "value")])
def update_market(market_measure):
    piv_market = pd.pivot_table(
        hotel_data(), values=market_measure, index="market_segment"
    )
    market_x = piv_market[market_measure].index
    market_y = piv_market[market_measure].values
    market_legend_title = piv_market.columns[0].replace("_", " ").title()
    return px.bar(
        piv_market, x=market_x, y=market_y, template="plotly_white"
    ).update_layout(
        xaxis_title="Market Segment",
        yaxis_title=piv_market.columns[0].replace("_", " ").title(),
        margin={"r": 10, "t": 10, "l": 10, "b": 10},
    )


# run dash app
if __name__ == "__main__":
    app.run_server()
