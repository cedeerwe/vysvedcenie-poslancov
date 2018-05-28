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
dur = pd.read_pickle(config.FILE_ROZPRAVY_DURATION)

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
    html.Div([  # HLASOVANIA
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
    html.Div([  # DEMAGOG
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
    ]),
    html.Div([  # ROZPRAVY
        dcc.Markdown(dedent("""
                     ## Štatistiky príspevkov do rozpráv v parlamente
                     Údaje v grafe sú prevzaté zo stránky [tv.nrsr.sk](
                     http://tv.nrsr.sk/).
                     """))], style={"align": "center"}),
    html.Div(id="rozpravy", children=[
        dcc.Graph(id="duration_graph"),
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

def bar_rozpravy_duration(name):
    """Output the rozpravy data for a Plotly bar chart."""
    n = len(dur)
    name_ind = np.arange(n)[dur.index == name][0]
    colors = ["rgba(0,0,255,0.7)"] * n
    colors[name_ind] = "rgba(255,0,0,1)"
    ss = n * [""]
    ss[name_ind] = name
    data = [
        go.Bar(
            x=dur.index,
            y=dur.apply(lambda x: x.total_seconds()) / 60,
            text=dur.index,
            marker={"color": colors})]
    layout = go.Layout(
        xaxis={"ticktext": ss, "tickvals": np.arange(n), "tickangle": 22},
        title="Celková dĺžka vystúpení v rozpravách v minutách")
    return {"data": data, "layout": layout}

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

@app.callback(
    Output("duration_graph", "figure"),
    [Input("poslanec_selection", "value")]
)
def plot_duration(name):
    return bar_rozpravy_duration(name)

if __name__ == '__main__':
    app.run_server(debug=True)
