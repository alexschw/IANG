"""
    Parser for the Interactive ANNarchy Network Generator
    @author: alexschw
"""
from pyparsing import And, alphanums, Dict, Group, Keyword, LineEnd,\
    LineStart, Literal, locatedExpr, OneOrMore, Optional, Or, originalTextFor,\
    printables, QuotedString, restOfLine, Suppress, Word, ZeroOrMore
import json

G = {'nodes':[], 'edges':[]}
_LP, _RP = Suppress("("), Suppress(")")
_LB, _RB = Suppress("["), Suppress("]")
_CM = Suppress(",")
_EQ = Suppress("=")
_STR = (QuotedString('"""', multiline=True) |
        QuotedString('"') | QuotedString("\'"))
var = Word(alphanums+"+-_.:")
vs = (var | _STR)
index = originalTextFor(vs + OneOrMore(_LB + OneOrMore(vs + Optional(_CM)) + _RB))
tupl = originalTextFor(_LP + vs + _CM + OneOrMore(vs  + Optional(_CM)) + ")")
value = index | _STR | tupl | var
parameter = Group(Optional(var + _EQ) + value + Optional(_CM))
connector = (Literal(".connect_") + Word(alphanums + "_") + _LP +
             ZeroOrMore(parameter) + _RP)


def simplify_parsed_output(output):
    """
        Simplifies the parsed output to [fromidx, toidx, contenttype].
    """
    pptxt = []
    k = 0
    for v in output.items():
        ctyp = list(v[1]['value'].keys())[0]
        name = v[1]['value'].get(ctyp)
        if name:
            name = name[0]
        if k != 0 and pptxt[k-1][2] == ctyp:
            pptxt[k-1][1] = v[1]['locn_end']
            if ctyp == "KWX":
                pptxt[k-1][3].append(name)
        else:
            pptxt.append([v[1]['locn_start'], v[1]['locn_end'], ctyp, [name]])
            k += 1
    for i in range(len(pptxt)-1):
        pptxt[i][1] = pptxt[i+1][0] - 1
    return pptxt

def kwparser(tokens):
    """
        Generate graph Items for the relevant tokens.
    """
    data = dict(list(tokens[-1]))
    inxm = 1
    if isinstance(tokens[1], list):
        # No assignment hence use only name argument as label
        inxm -= 1
        data['label'] = data.get('name')
    else:
        data['name'], data['label'] = tokens[0], data.get('name', tokens[0])
    data['id'] = data['name']
    if tokens[inxm] == 'Population':
        G['nodes'].append({'data': data })
    elif tokens[inxm] in ['Projection', "Convolution", "Pooling"]:
        data['source'] = data.get('pre')
        classes = data.get('target')
        data['target'] = data.get('post')
        G['edges'].append({'data': data, 'classes': classes})

def opAss(d):
    """ Optional Assignment. """
    return Group(Optional(var + _EQ, default=d) + value) + Optional(_CM)

def ann_kwexp(keywords, params):
    """ ANNarchy Keyword Expression. """
    pars = And(opAss(p) for p in params)
    kw = Or(Keyword(k) for k in keywords)

    return (Optional(var + _EQ) + Optional(Suppress("ann.")|Suppress("ANN.")) +
            kw + _LP + Group(pars + ZeroOrMore(parameter)) + _RP +
            Suppress(Optional(connector)))

def std_parser():
    """
        Parse the ANNarchy Source Code to extract the definitions.
    """
    global G
    G = {'nodes':[], 'edges':[]}
    comment = OneOrMore("#" + restOfLine() | LineStart() + _STR + LineEnd())

    imports = "from" + restOfLine() | "import" + restOfLine()

    Population = ann_kwexp(["Population"], ["geometry", "neuron"])
    Projection = ann_kwexp(["Projection", "Convolution", "Pooling"],
                           ["pre", "post", "target"])

    NeuSyn = ann_kwexp(["Neuron", "Synapse"], ["parameters", "equations"])
    ConMethod = Word(alphanums+"_") + connector
    kwexpr = NeuSyn | Population | Projection
    otherSC = (Group(Word(printables)))+ restOfLine

    inpline = (imports("IMP") | kwexpr("KWX").addParseAction(kwparser) |
               ConMethod("KWX") | comment('CMT') | otherSC("OTH"))
    return Dict(OneOrMore(locatedExpr(Group(inpline))))

def graph_sanity_check():
    """
        Check the graph for dangling edges and replace them.
    """
    nodes = [node['data']['name'] for node in G['nodes']]
    labels = [node['data']['label'] for node in G['nodes']]
    # [e for e in G['edges'] if e in nodes else labels]
    for i, edge in enumerate(G['edges']):
        if edge['data']['source'] not in labels:
            if edge['data']['source'] in nodes:
                ind = nodes.index(edge['data']['source'])
                G['edges'][i]['data']['source'] = labels[ind]
        if edge['data']['target'] not in labels:
            if edge['data']['target'] in nodes:
                ind = nodes.index(edge['data']['target'])
                G['edges'][i]['data']['target'] = labels[ind]
    G['edges'] = [edge for edge in G['edges']
                  if (edge['data']['source'] in labels and
                      edge['data']['target'] in labels)]

def file_parser(filename):
    """
        Parse a complete python file returing a simplified output and a graph.
    """
    bf = std_parser().parseFile(filename, parseAll=True).asDict()
    graph_sanity_check()
    return simplify_parsed_output(bf), G

def string_parser(string):
    """
        Parse a String returing a simplified output and a graph.
    """
    bf = std_parser().parseString(string, parseAll=True).asDict()
    graph_sanity_check()
    return simplify_parsed_output(bf), G
