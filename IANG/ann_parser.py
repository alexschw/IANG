"""
    Parser for the Interactive ANNarchy Network Generator
    @author: alexschw
"""
from pyparsing import (And, alphanums, Dict, Group, Keyword, LineEnd,
                       LineStart, locatedExpr, OneOrMore, Optional, Or,
                       originalTextFor, printables, QuotedString, restOfLine,
                       Suppress, Word, ZeroOrMore)
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


def simplify_parsed_output(output):
    """
        Simplifies the parsed output to [fromidx, toidx, contenttype].
    """
    pptxt = []
    k = 0
    for v in output.items():
        ctyp = list(v[1]['value'].keys())[0]
        name = v[1].get('name')
        if not name:
            name = v[1]['value'].get('KWX')
            if name:
                name = name[0]
        if k != 0 and pptxt[k-1][2] == ctyp:
            pptxt[k-1][1] = v[1]['locn_end']
            if ctyp == "KWX":
                pptxt[k-1][3].append(name)
        else:
            pptxt.append([v[1]['locn_start'], v[1]['locn_end'], ctyp, [name]])
            k += 1
    return pptxt

def kwparser(tokens):
    """
        Generate graph Items for the relevant tokens.
    """
    inxm = 1
    if isinstance(tokens[1], list):
        # No assignment hence use first argument.
        inxm -= 1
    data = dict(list(tokens[inxm+1]))
    data['label'] = data.get('name')
    if data['label'] is None:
        data['label'] = tokens[0]
    # data['label'] = data['label'].replace(r"['\"]", "")
    data['name'] = data['id'] = data['label']
    if tokens[inxm] == 'Population':
        # data['geometry'] = tuple(int(i) for i in data.get('geometry')
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
            kw + _LP + Group(pars + ZeroOrMore(parameter)) + _RP)

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
    kwexpr = NeuSyn | Population | Projection
    otherSC = Group(Word(printables))

    inpline = (imports("IMP") | kwexpr("KWX").addParseAction(kwparser) |
               comment('CMT') | otherSC("OTH"))
    return Dict(OneOrMore(locatedExpr(Group(inpline))))

def file_parser(filename):
    """
        Parse a complete python file returing a simplified output and a graph.
    """
    bf = std_parser().parseFile(filename, parseAll=True).asDict()
    return simplify_parsed_output(bf), G

def string_parser(string):
    """
        Parse a String returing a simplified output and a graph.
    """
    bf = std_parser().parseString(string, parseAll=True).asDict()
    return simplify_parsed_output(bf), G
