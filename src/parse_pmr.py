from io import BytesIO
import requests
from lxml import etree
from rdflib.graph import Graph
from urllib import parse
import pprint
import json
import ontology_lookup


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


def add_labels(triples):
    quadruples = []
    items = []

    for s, p, o in triples:
        items.append(str(s))
        items.append(str(p))
        items.append(str(o))

        try:
            ont, code = resolve_identifiers(str(o))
        except:
            label = 'TODO: other ontology label!!!'
            items.append(label)
            quadruples.append(items)
            items = []
            continue
        encoded_code = parse.quote_plus(code)
        label = ontology_lookup.get_term_by_code(lookupService='bioportal', ontology=ont, code=encoded_code)
        items.append(label)

        quadruples.append(items)
        items = []
    return quadruples

# http://identifiers.org/opb/OPB_00340      >>  http://bhi.washington.edu/OPB#OPB_00340     (Chemical concentration)
# http://identifiers.org/fma/FMA:84666      >>  http://purl.org/sig/ont/fma/fma84666        (Apical plasma membrane)
# http://identifiers.org/go/GO:0070489      >>  http://purl.obolibrary.org/obo/GO_0070489   (T cell aggregation)
# http://identifiers.org/chebi/CHEBI:26708  >>  http://purl.obolibrary.org/obo/CHEBI_26708  (sodium-23 atom)

def resolve_identifiers(id=''):
    if id.startswith('http://identifiers.org'):
        ont_end = id.find('/', 23)
        ont = id[23:ont_end]
        code = id[ont_end+1:]

        if ont == 'opb':
            return ont, 'http://bhi.washington.edu/OPB#' + code
        elif ont == 'fma':
            newcode = code.replace(':', '').lower()
            return ont, 'http://purl.org/sig/ont/fma/' + newcode
        elif ont == 'go':
            newcode = code.replace(':', '_')
            return ont, 'http://purl.obolibrary.org/obo/' + newcode
        elif ont == 'chebi':
            newcode = code.replace(':', '_')
            return ont, 'http://purl.obolibrary.org/obo/' + newcode


def get_annots(cellmlname):
    tree = getcellmltree(cellmlname)
    grrdf = xmltree_to_rdfgraph(tree)
    triples = get_json(grrdf)
    quadruples = add_labels(triples)
    return json.dumps(quadruples)


if __name__ == "__main__":
    #annots = get_annots('https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/chang_fujita_1999-semgen.cellml')
    annots = get_annots('..\\models\eeler_reuter_1977-sample1.cellml')
    pprint.pprint(annots)
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
