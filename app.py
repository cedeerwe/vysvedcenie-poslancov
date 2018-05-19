import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import pandas as pd
import numpy as np

from textwrap import dedent

import config

################
# DATA LOADING #
################

kluby = pd.read_hdf(config.FILE_KLUBY)
sorted_names = sorted(kluby.index, key=lambda x: " ".join(x.split(" ")[::-1]))
hlasy = {vysledok: pd.read_hdf(config.FILE_STATS_HLASY_PIE, vysledok)
         for vysledok in config.HLASY_STATS_VYSLEDOK}
dg = pd.read_hdf(config.FILE_DEMAGOG_PIE)

#####################
# APP SPECIFICATION #
#####################

app = dash.Dash()
server = app.server

app.layout = html.Div([
    dcc.Dropdown(
        options=[{
            "label": "{} ({})".format(name, kluby[name]),
            "value": name
        } for name in sorted_names],
        value=sorted_names[0],
        id="poslanec_selection",
        clearable=False
    ),
    html.Div([
        dcc.Markdown(dedent("""
                     ## Štatistiky z hlasovaní v parlamente
                     Nasledujúce grafy vznikli spracovaním dát zo stránky
                     [nrsr.sk](
                     https://www.nrsr.sk/web/default.aspx?SectionId=108).
                     """))], style={"align": "center"}),
    html.Div([
        html.Div([
            dcc.Graph(id="pie_positive")
            ], style={"width": "49%", "display": "inline-block"}),
            html.Div([
            dcc.Graph(id="pie_negative")
            ], style={"width": "49%", "display": "inline-block"})]),
    html.Div([
        dcc.Markdown(dedent("""
                     ## Štatistiky pravdivosti výrokov v politických debatách
                     Údaje v grafoch sú prevzaté zo stránky [demagog.sk](
                     http://www.demagog.sk/).
                     """))], style={"align": "center"}),
    html.Div(id="graph_demagog", children=[
        dcc.Graph(id="pie_demagog"),
        ]),
    html.Div(id="replacement_text_demagog", children=[
        html.P("Nie sú registrované žiadne vystúpenia v debatách."),
    ])
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
            int(np.sum(values)), vysledok)
    )
    return {"data": [trace], "layout": layout}


def pie_demagog(name):
    """Output the demagog data for a Plotly pie plot."""
    values = dg[name].values
    labels = dg.index.values
    trace = go.Pie(labels=labels, values=values, sort=False)
    layout = go.Layout(
        title="Pravdivosť z {} diskusných výrokov.".format(
            int(np.sum(values))
        )
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


@app.callback(
    Output("replacement_text_demagog", "style"),
    [Input("poslanec_selection", "value")]
)
def toggle_demagog_text(name):
    if name in dg.columns:
        return {"display": "none"}
    else:
        return {"display": "block"}


@app.callback(
    Output("graph_demagog", "style"),
    [Input("poslanec_selection", "value")]
)
def toggle_demagog_graph(name):
    if name not in dg.columns:
        return {"display": "none"}
    else:
        return {"display": "block"}


@app.callback(
    Output("pie_demagog", "figure"),
    [Input("poslanec_selection", "value")]
)
def plot_demagog(name):
    if name in dg.columns:
        return pie_demagog(name)
    else:
        return {"data": []}


if __name__ == '__main__':
    app.run_server(debug=True)
