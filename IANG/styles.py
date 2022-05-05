"""
    Dictionary of styles for differnt elements.
"""
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'width': '19%',
        'float': 'right',
    },
    'txt': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'wrap': 'off',
        'width': '49%',
        'height': '90vh',
        'float': 'right',
    },
    'IMP': {
        'border': 'thin lightgrey solid',
        'wrap': 'off',
        'width': '100%',
        'resize': 'none',
        'color': 'blue',
    },
    'KWX': {
        'border': 'thin lightgrey solid',
        'wrap': 'off',
        'width': '100%',
        'resize': 'none',
        'color': 'green',
    },
    'OTH': {
        'border': 'thin lightgrey solid',
        'wrap': 'off',
        'width': '100%',
        'resize': 'none',
    },
    'CMT': {
        'border': 'thin lightgrey solid',
        'wrap': 'off',
        'width': '100%',
        'color': 'grey',
        'resize': 'none',
    },
    'upload': {
        'width': '20%',
        'height': '30px',
        'lineHeight': '30px',
        'borderWidth': '2px',
        'borderStyle': 'dashed',
        'borderRadius': '8px',
        'textAlign': 'center',
    },
    'cyto': {
        'width': '50%',
        'height': '90vh',
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
