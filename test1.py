import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
from os import listdir, remove
import pickle
from time import sleep
from helper_functions import *

#check_for_and_del_io_files()

# create an app object of class 'Dash'
app = dash.Dash(__name__)

# Define the layout of the dash page.
app.layout = html.Div([
# Section title
    html.H1("Section 1: Fetch & Display exchange rate historical data"),

# Currency pair text input, within its own div.
    html.Div(dcc.Input(id = 'currency-pair', type = 'text', style={'display': 'inline-block'})),

# Submit button:
    html.Button('Submit', id = 'submit-button', n_clicks = 0),

# Line break
    html.Br(),

# Div to hold the initial instructions and the updated info once submit is pressed
    html.Div(id='output-div0', children='Enter a currency code and press submit'),

    html.Div([
        # Candlestick graph goes here:
        dcc.Graph(id='candlestick-graph')
    ]),

# Another line breaks
    html.Br(),
    # Section title
    html.H1("Section 2: Make a Trade"),
    # Div to confirm what trade was made
    html.Div(id='output-div'),
    # Radio items to select buy or sell
    dcc.RadioItems(
        id='r1',
        options=[
            {'label': 'BUY', 'value': 'BUY'},
            {'label': 'SELL', 'value': 'SELL'}
        ],
        value='MTL'
    ),
    # Text input for the currency pair to be traded
    html.Div(dcc.Input(id = 'currency-pair2', type = 'text', style={'display': 'inline-block'})),
    # Numeric input for the trade amount
    dcc.Input(id='trade-amount', type='number'),
    # Submit button for the trade
    html.Button('Trade', id = 'trade-button', n_clicks = 0),
])


# Callback for what to do when submit-button is pressed
@app.callback(
    [ # there's more than one output here, so you have to use square brackets to pass it in as an array.
    dash.dependencies.Output('output-div0', 'children'),
    dash.dependencies.Output('candlestick-graph','figure')
    ],
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('currency-pair', 'value')]
)
def update_candlestick_graph(n_clicks, value): # n_clicks doesn't get used, we only include it for the dependency.
    # Now we're going to save the value of currency-input as a text file.

    # Wait until ibkr_app runs the query and saves the historical prices csv

    # Read in the historical prices
    df = pd.read_csv('currency_pair_history.csv')
    # Remove the file 'currency_pair_history.csv'

    # Make the candlestick figure
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
            )
        ]
    )
    # Give the candlestick figure a title
    fig.update_layout(title=value)

    # Return your updated text to currency-output, and the figure to candlestick-graph outputs
    return ('Submitted query for ' + value), fig


if __name__ == '__main__':
    app.run_server(debug=True)
