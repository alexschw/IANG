# -*- coding: utf-8 -*-
"""
  Interactive ANNarchy Network Generator
  @author: alexschw
"""
from dash import Dash
from dash.html import A, Button, Div
from dash.dcc import Store, Upload
from dash_cytoscape import Cytoscape
from styles import styles, stylesheet
from callbacks import callbacks

APP = Dash(__name__)

def define_dashboard():
    """
    Define the basic dashboard structure.
    """
    network_storage = Store(id='network_data', data={'nodes':[], 'edges':[]},
                            storage_type='local')
    elem = network_storage.data
    scape = Cytoscape(id='ann-net', layout={'name': 'grid'}, elements=elem,
                      style=styles['cyto'], stylesheet=stylesheet)
    txtDiv = Div(id='text', style=styles['txt'])
    upload = Upload(A("Upload File"), id='upload_btn', style=styles['upload'],
                    accept="text/x-python")
    layBtn = Button("Set Graph Root", id='layout_btn', style=styles['upload'])

    APP.layout = Div([upload, layBtn, scape, txtDiv, network_storage])
    return network_storage


if __name__ == '__main__':
    model_file = '../mininet.py'
    store = define_dashboard()
    callbacks(APP)

    APP.run_server(debug=True)
