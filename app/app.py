# import statements
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# read csv file of hotel booking data
csv_file = os.path.join(os.path.dirname(__file__), "../data/hotel_bookings.csv")
df = pd.read_csv(csv_file)

# create base figures
template="plotly_white"
fig01 = px.bar(df[['market_segment', 'stays_in_week_nights']], x='market_segment', y='stays_in_week_nights', template=template, color='market_segment')

# create dash app
external_stylesheets = ['https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# create layout for app
app.index_string = '''
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
'''
app.layout = html.Section([
    html.Div([
        html.H1('Hotel Booking Demand', className='title'),
        html.H2('Mike Farris | Dev Project | IT 7113 Data Visualization - Kennesaw State University')
    ], className='container is-fluid has-text-centered'),
    html.Hr(),
    html.Div([
        html.Div([
            html.Div([
                html.P('Market Segment by Stays in Week Nights', className='card-header-title')
            ], className='card-header has-text-centered'),
            html.Div([
                dcc.Graph(id="fig01", figure=fig01)
            ], className='card-content')
        ], className='card')
    ], className='container')
], className='section')

# run dash app
if __name__ == "__main__":
    app.run_server(debug=True)
