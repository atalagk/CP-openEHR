from io import BytesIO
import requests
from lxml import etree
from rdflib.graph import Graph
import pprint
import json


def getcellmltree(location):
    if str(location).startswith('http'):
        r = requests.get(location)
        cml = r.content
    else:
        with open(location, 'r') as cml:
            cml = bytes(cml.read(), encoding='utf-8')
    return etree.parse(BytesIO(cml))


def xmltree_to_rdfgraph(tree):
    nodes = tree.xpath('..//rdf:RDF', namespaces={'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
    graph = Graph()
    for node in nodes:
        s = BytesIO(etree.tostring(node))
        graph.parse(s, format='xml')
    return graph


def get_json(rdfs):
    tl = []
    tr = {}
    js = []
    for s, p, o in rdfs:
        if s.startswith('http://identifiers.org') or \
        p.startswith('http://identifiers.org') or \
        o.startswith('http://identifiers.org'):
            tl.append(str(s))
            tl.append(str(p))
            tl.append(str(o))
            js.append(tl)
            tl = []
    return js

def get_annots(cellmlname):
    tree = getcellmltree(cellmlname)
    grrdf = xmltree_to_rdfgraph(tree)
    triples = get_json(grrdf)
    pairs = add_labels(triples)
    return json.dumps(pairs)


def add_labels(triples):
    quadruples = []
    items = []

    for s, p, o in triples:
        items.append(str(s))
        items.append(str(p))
        items.append(str(o))
        items.append('label')
        quadruples.append(items)
        items = []

    return quadruples



if __name__ == "__main__":
    annots = get_annots('https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/chang_fujita_1999-semgen.cellml')
    #annots = get_annots('..\\models\chang_fujita_1999-semgen.cellml')
    #pprint.pprint(annots)
    print(annots)

    '''
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/chang_fujita_1999-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/chang_fujita_b_1999-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/eskandari_2005-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/mackenzie_1996-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/moss_2009-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/thomas_2000-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/weinstein_1995-semgen.cellml
    '''
