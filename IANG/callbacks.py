"""
    Defines the callbacks for the dash APP.
"""
import base64
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dcc import Textarea
from dash import callback_context
from ann_parser import file_parser, string_parser
from styles import styles

def callbacks(APP):
    """
    Define callback functions for the nodes and edges.
    """
    @APP.callback(Output('network_data', 'data'),
                  Input('upload_btn', 'contents'),
                  Input('ta', 'n_blur'),
                  State('text', 'children'))
    def loadNetworkData(contents, ta, children):
        ctx = callback_context.triggered[0]
        if not ctx:
            return {'content': '', 'data': '', 'graph': ''}
        if contents is None:
            with open('../mininet.py', 'r') as f:
                c = f.read()
        elif ctx["prop_id"] == 'ta.n_blur':
            c = "\n".join([ch['props']['value'] for ch in children])
        else:
            _, contentstr = contents.split(',')
            c = base64.b64decode(contentstr).decode('utf-8')
        data, graph = string_parser(c)
        return {'content': c, 'data': data, 'graph': graph}

    def on_click_highlight(tap, divs):
        """
        Highlight the background textarea of the tapped edge or node.
        """
        for tx in divs:
            if tx['props'].get('name'):
                if tap['name'] in tx['props'].get('name').split(','):
                    tx['props']['style']['background-color'] = '#ffb224'
                else:
                    tx['props']['style']['background-color'] = 'white'

    def generate_textareas(data):
        divs = []
        if "data" in data:
            for val in data['data']:
                ta = Textarea(id="ta")
                subtxt = data['content'][val[0]:val[1]]
                ta.value = subtxt
                ta.style = styles[val[2]]
                if val[3][0]:
                    ta.name = ",".join(val[3][0])
                ta.rows = (subtxt.count('\n') + 1)
                divs.append(ta)
        return divs


    @APP.callback(Output('text', 'children'),
                  Input('network_data', 'data'),
                  Input('ann-net', 'tapNodeData'),
                  Input('ann-net', 'tapEdgeData'),
                  State('text', 'children'))
    def show_elements(data, tND, tED, divs):
        ctx = callback_context.triggered[0]
        if not ctx:
            raise PreventUpdate
        if ctx["prop_id"].split(".")[0] == 'ann-net':
            if ctx["prop_id"] == 'ann-net.tapNodeData':
                tap = tND
            else:
                tap = tED
            on_click_highlight(tap, divs)
        else:
            divs = generate_textareas(data)
        return divs

    @APP.callback(Output('ann-net', 'elements'),
                  Input('network_data', 'data'))
    def show_graph(data):
        return data['graph']

    @APP.callback(Output('ann-net', 'layout'),
                  Input('layout_btn', 'n_clicks'),
                  State('ann-net', 'selectedNodeData'))
    def swap_layout(n_clicks, elem):
        if not n_clicks or not elem:
            raise PreventUpdate
        k = ", ".join("#"+node['id'] for node in elem)
        return {'name':'breadthfirst', 'animate':True, 'roots':k}
