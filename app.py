import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import pandas as pd
import numpy as np


import config

################
# DATA LOADING #
################

kluby = pd.read_hdf(config.FILE_KLUBY)
hlasy = {vysledok: pd.read_hdf(config.FILE_STATS_HLASY_PIE, vysledok)
         for vysledok in config.HLASY_STATS_VYSLEDOK}

#####################
# APP SPECIFICATION #
#####################

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(
        options=[{
            "label": "{} ({})".format(name, kluby[name]),
            "value": name
        } for name in kluby.index],
        value=kluby.index[0],
        id="poslanec_selection",
        clearable=False
    ),
    html.Div([
        dcc.Graph(id="pie_positive")
    ], style={"width": "49%", "display": "inline-block"}),
    html.Div([
        dcc.Graph(id="pie_negative")
    ], style={"width": "49%", "display": "inline-block"})
])

######################
# GRAPHING FUNCTIONS #
######################


def pie_hlasy(name, vysledok):
    """Output the hlasy data for a Plotly pie plot."""
    values = hlasy[vysledok][name][config.HLASY_STATS_ORDER].values
    labels = [config.HLASY_STATS_MEANING[s] for s in config.HLASY_STATS_ORDER]
    trace = go.Pie(labels=labels, values=values, sort=False)
    layout = go.Layout(
        title="Hlasovanie v {} prípadoch keď návrh {}".format(
            np.sum(values), vysledok)
    )
    return {"data": [trace], "layout": layout}

#################
# APP CALLBACKS #
#################


@app.callback(
    Output("pie_positive", "figure"),
    [Input("poslanec_selection", "value")]
)
def plot_positives(name):
    return pie_hlasy(name, config.HLASY_STATS_VYSLEDOK[0])


@app.callback(
    Output("pie_negative", "figure"),
    [Input("poslanec_selection", "value")]
)
def plot_negatives(name):
    return pie_hlasy(name, config.HLASY_STATS_VYSLEDOK[1])
