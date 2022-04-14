import ANNarchy as ann
from dash.dependencies import Input, Output

def callbacks(APP):
    @APP.callback(Output('nodeInfo', 'children'), Input('ann-net', 'tapNodeData'))
    def displayTapNodeData(data):
        if not data:
            return ""
        pop = ann.get_population(data['id'])
        neur = pop.neuron_type
        return f"{data['id']} Shape: {pop.geometry} \n{repr(neur)}"

    @APP.callback(Output('edgeInfo', 'children'), Input('ann-net', 'tapEdgeData'))
    def displayTapNodeData(data):
        if not data:
            return ""
        syn = ann.get_projection(data['label']).synapse_type
        return repr(syn)
