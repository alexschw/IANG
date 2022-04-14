# -*- coding: utf-8 -*-
"""
  Interactive ANNarchy Network Generator
  @author: alexschw
"""
import plotly.graph_objects as go
import json
import dash
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
from styles import styles, stylesheet
from callbacks import callbacks
from generate_graph import Graph

APP = dash.Dash(__name__)

def define_dashboard(elem):
    scape = cyto.Cytoscape(
        id='ann-net',
        layout={'name': 'grid'},
        style=styles['cyto'],
        elements=elem,
        stylesheet=stylesheet,
    )
    APP.layout = dash.html.Div([ scape,
        dash.html.Pre(id='nodeInfo', style=styles['pre']),
        dash.html.Pre(id='edgeInfo', style=styles['pre']),
    ])

if __name__ == '__main__':
    model_file = "../mininet.py"
    with open(model_file) as f:
        # code = compile(f.read(), model_file,'exec')
        exec(f.read())
    model = Graph().get_graph()

    print(dash.html.Textarea)
    define_dashboard(model)
    callbacks(APP)
    APP.run_server(debug=True)
