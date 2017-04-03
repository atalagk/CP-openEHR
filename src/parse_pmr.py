from io import BytesIO
import requests
from lxml import etree
from rdflib.graph import Graph
import pprint
import json
import ontology_lookup

triple = ['', '', '']
cache = []
cache.append(triple)

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


def get_triples(rdfs):
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


def add_labels(triples):
    quadruples = []
    items = []

    for s, p, o in triples:
        items.append(str(s))
        items.append(str(p))
        items.append(str(o))

        try:
            ont, code = ontology_lookup.resolve_identifiers(str(o))
        except:
            label = 'TODO: other ontology label!!!'
            items.append(label)
            quadruples.append(items)
            items = []
            continue
        label = find_label(ont, code)
        items.append(label)
        quadruples.append(items)
        items = []
    return quadruples


def find_label (ont, code):
    global cache
    for triple in cache:
        if triple[0] == ont and triple[1] == code:
            label = triple[2]
            return label

    newtriple = []
    # label = ontology_lookup.get_term_by_code(lookupService='bioportal', ontology=ont, code=encoded_code)
    label = ontology_lookup.get_term_by_code(lookupService='ols', ontology=ont, code=code)
    newtriple.append(ont)
    newtriple.append(code)
    newtriple.append(label)
    cache.append(newtriple)
    return label

# http://identifiers.org/opb/OPB_00340      >>  http://bhi.washington.edu/OPB#OPB_00340     (Chemical concentration)
# http://identifiers.org/fma/FMA:84666      >>  http://purl.org/sig/ont/fma/fma84666        (Apical plasma membrane)
# http://identifiers.org/go/GO:0070489      >>  http://purl.obolibrary.org/obo/GO_0070489   (T cell aggregation)
# http://identifiers.org/chebi/CHEBI:26708  >>  http://purl.obolibrary.org/obo/CHEBI_26708  (sodium atom)
# http://identifiers.org/chebi/CHEBI:17996  >>  can't find in Bioportal, OK in OLS          (chloride)


def get_annots(cellmlname):
    tree = getcellmltree(cellmlname)
    grrdf = xmltree_to_rdfgraph(tree)
    triples = get_triples(grrdf)
    quadruples = add_labels(triples)
    return json.dumps(quadruples)


if __name__ == "__main__":
    from time import time

    start_time = time()
    annots = get_annots('https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/chang_fujita_1999-semgen.cellml')
    #annots = get_annots('..' + chr(92) + 'models' + chr(92) + 'beeler_reuter_1977-sample.cellml')
    pprint.pprint(annots)
    dt = str(time() - start_time)
    print('Finished in seconds: ' + dt)
    #print(annots)

    '''
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/chang_fujita_1999-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/chang_fujita_b_1999-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/eskandari_2005-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/mackenzie_1996-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/moss_2009-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/thomas_2000-semgen.cellml
    https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/weinstein_1995-semgen.cellml
    '''
