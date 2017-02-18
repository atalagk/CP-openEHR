from io import BytesIO
import requests
from lxml import etree
from rdflib.graph import Graph
from rdflib import URIRef
import pprint
import json

upstreamneedtolearntoknowwtfisiri = 'rdflibfailsathandlingrelativeirisorurnsoranything://oh/'

def setpmrurl(cellmlname):
    url = 'https://models.physiomeproject.org'
    url += '/workspace/267/rawfile/59b35d8439d9ea5e9309bc461e2b795dd1d8c796/semgen-annotation/'
    url += cellmlname
    return url

def xmltree_to_rdfgraph(tree):
    nodes = tree.xpath('..//rdf:RDF', namespaces={'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
    graph = Graph()
    for node in nodes:
        s = BytesIO(etree.tostring(node))
        graph.parse(s, format='xml', publicID=upstreamneedtolearntoknowwtfisiri)

    def torelative(node):
        if not isinstance(node, URIRef):
            return node
        if node.startswith(upstreamneedtolearntoknowwtfisiri):
            return URIRef(node.replace(upstreamneedtolearntoknowwtfisiri, ''))
        return node

    real_result = Graph()
    for triple in graph:
        s, p, o = triple
        # make sure to exclude non URI stuff
        if str(p) != 'http://purl.org/dc/terms/description' and\
            str(o).startswith('http://') and\
            str(s).startswith('http'):
            real_result.add((torelative(s), torelative(p), torelative(o)))
    return real_result


def get_tree_from_url(url):
    r = requests.get(url)
    return etree.parse(BytesIO(r.content))

def get_json(rdfs):
    tl = []
    tr = {}
    js = []
    i = 1
    for s, p, o in rdfs:
        tl.append(str(s))
        tl.append(str(p))
        tl.append(str(o))
        tr = {str(i): tl}
        i += 1
        js.append(tr)
        tl = []
    return js

def get_annots(cellmlname):
    url = setpmrurl(cellmlname)
    tree = get_tree_from_url(url)
    grrdf = xmltree_to_rdfgraph(tree)
    js = get_json(grrdf)
    return json.dumps(js)


if __name__ == "__main__":
    annots = get_annots('chang_fujita_1999-semgen.cellml')
    print(annots)

    '''
    tree = get_tree_from_url(url)
    grrdf = xmltree_to_rdfgraph(tree)
    js = get_json(grrdf)

        #print('s: ' + str(s))
        #print('p: ' + str(p))
        #print('o: ' + str(o))
        #print()
    #print(js)
    pprint.pprint(js)

    chang_fujita_1999
    chang_fujita_b_1999
    eskandari_2005
    mackenzie_1996
    moss_2009
    thomas_2000
    weinstein_1995
    '''
