# colors = ['#00ff00', '#00ffff', '#ff0000', '#ffff00', '#ffffff', '#ff8000',
#           '#ffff80', '#ff80ff', '#80ff00', '#80ffff', '#00ff80', '#8000ff',
#           '#ff0080']

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'width': '19%',
        'float': 'right',
    },
    'cyto': {
        'width': '80%',
        'height': '1200px',
        'float':'left',
        'nodeOverlap':8,
        'gravity': .2,
    },
}

stylesheet = [
    {
        'selector': 'node',
        'style': {
            'width':'80px',
            'text-valign': 'center',
            'text-wrap':'wrap',
            'font-size':'12px',
            'content': 'data(label)',
            'shape': 'rectangle',
        },
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'square',
        },
    },
    {
        'selector': '.inh',
        'style': {
            'line-color': 'blue',
            'target-arrow-color': 'blue',
            'target-arrow-shape': 'circle',
        } }, {
        'selector': '.exc',
        'style': {
            'line-color': 'red',
            'target-arrow-color': 'red',
            'target-arrow-shape': 'triangle',
        }
    },
]
