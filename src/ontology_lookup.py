import auth
import requests
import json
from urllib import parse
from pyquery import PyQuery as pq


def get_term_by_code(**kwargs):
    lookupService = kwargs.get('lookupService', None)
    ontology = kwargs.get('ontology', None)
    code = kwargs.get('code', None)
    version = kwargs.get('version', 'current')
    newurl = kwargs.get('url_extension', None)

    if not str(code).startswith('http'):
        id_code = resolve_identifiers(id=code, ont=ontology)
        code = id_code

    if lookupService:
        # Generic lookup service with a specified particular ontology service
        if lookupService == 'bioportal':
            url = auth.bioportal_url
            headers = {'Authorization': 'apikey token=' + auth.bioportal_api_key}

            include = ''
            if ontology:
                if ontology != 'go' or ontology != 'chebi':
                    include = '&ontologies=' + str(ontology).upper()
            include += "&display_context=false"
            include += "&include=prefLabel"
            include += "&require_exact_match=true"
            include += "&display_links=false"

            urlnext = url + '/search?q=' + code + include
            r = requests.get(urlnext, headers=headers)
            try:
                label = r.json()["collection"][0]["prefLabel"]
            except:
                label = 'Error in label:' + code
            return label

        elif lookupService == 'umls':
            h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
            params = {'apikey': auth.umls_api_key}
            r = requests.post(auth.umls_tgt_url, data=params, headers=h)
            d = pq(r.text)
            tgt = d.find('form').attr('action')

            params = {'service': auth.umls_st_url}
            h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
            r = requests.post(tgt, data=params, headers=h)
            st = r.text

            url = auth.umls_url
            query = {'ticket': st}
            content_endpoint = "/rest/content/" + str(version) + "/source/" + str(ontology) + "/" + str(code)
            r = requests.get(url + content_endpoint, params=query)
            r.encoding = 'utf-8'
            items = json.loads(r.text)
            result = items["result"]["name"]
            return result
        elif lookupService == 'ols':
            header = {'Accept': 'application/json'}
            encoded_code = url_encode(code, 2)
            url = auth.ols_url + 'ontologies/' + ontology + '/terms/' + encoded_code
            r = requests.get(url, headers=header)
            items = r.json()
            try:
                label = items['label']
            except KeyError:
                label = 'Error in= ' + code
            return label
    else:
        # Without UoA OLS hardcoded ontology lookup that makes use of EBI OLS for FMA, CHEBI, GO and Bioportal for FMA
        if ontology == 'chebi' or ontology == 'go' or ontology == 'fma':
            #return get_label_localowl(ontology, code)
            header = {'Accept': 'application/json'}
            encoded_code = url_encode(code, 2)
            url = auth.ols_url + 'ontologies/' + ontology + '/terms/' + encoded_code
            r = requests.get(url, headers=header)
            items = r.json()
            try:
                label = items['label']
            except KeyError:
                label = 'Error in= ' + code
            return label

        elif ontology == 'opb':
            #return get_label_localowl(ontology, code)  # gets from local OPB.owl
            url = auth.bioportal_url
            headers = {'Authorization': 'apikey token=' + auth.bioportal_api_key}
            include = '&ontologies=OPB'
            include += "&display_context=false"
            include += "&include=prefLabel"
            include += "&require_exact_match=true"
            include += "&display_links=false"

            encoded_code = url_encode(code, 1)
            urlnext = url + '/search?q=' + encoded_code + include
            r = requests.get(urlnext, headers=headers)
            try:
                label = r.json()["collection"][0]["prefLabel"]
            except:
                label = 'Error in label:' + code
            return label

def get_label_localowl(ont, code):
    # Absolutely very slow for large owl files (for OPB it is OK, but for FMA not!!!
    from rdflib import Graph
    from rdflib.namespace import RDFS

    g = Graph()
    ontology = '..' + chr(92) + 'models' + chr(92) + str(ont).upper() + '.owl'
    g.parse(ontology)
    newcode = str(code).rsplit('#')[-1]

    for subj, obj in g.subject_objects(predicate=RDFS.label):
        if newcode in subj:
            label = obj.rsplit('#')[-1]
            return label
    label = 'Label not found in local ontology=' + ont + 'for code=' + code
    return label


def resolve_identifiers(id='', ont=''):

    if id.startswith('http://identifiers.org'):
        ont_end = id.find('/', 23)
        ont = id[23:ont_end]
        code = id[ont_end+1:]
        if ont == 'opb':
            return ont, 'http://bhi.washington.edu/OPB#' + code
        elif ont == 'fma':
            newcode = code.replace(':', '_').upper()
            return ont, 'http://purl.obolibrary.org/obo/' + newcode
        elif ont == 'go':
            newcode = code.replace(':', '_').upper()
            return ont, 'http://purl.obolibrary.org/obo/' + newcode
        elif ont == 'chebi':
            newcode = code.replace(':', '_').upper()
            return ont, 'http://purl.obolibrary.org/obo/' + newcode
        elif ont == 'snomed':
            newcode = code.replace(':', '_').upper()
            return ont, 'http://snomed.info/id/' + newcode
        elif ont == 'loinc':
            newcode = code.replace(':', '_').upper()
            return ont, 'http://purl.bioontology.org/ontology/LNC/' + newcode

    else:   # if just the code
        code = id
        ont_small = ont.lower()
        ont = ont_small

        if ont == 'opb':
            newcode = 'OPB_' + code
            return 'http://bhi.washington.edu/OPB#' + newcode
        elif ont == 'fma':
            newcode = 'FMA_' + code
            return 'http://purl.obolibrary.org/obo/' + newcode
        elif ont == 'go':
            newcode = 'GO_' + code
            return 'http://purl.obolibrary.org/obo/' + newcode
        elif ont == 'chebi':
            newcode = 'CHEBI_' + code
            return 'http://purl.obolibrary.org/obo/' + newcode
        elif ont == 'snomed':
            return 'http://snomed.info/id/' + code
        elif ont == 'loinc':
            return 'http://purl.bioontology.org/ontology/LNC/' + code

def url_encode(code, num):
    if num == 1:
        result = parse.quote_plus(code)
    elif num == 2:
        firstpass = parse.quote_plus(code)
        result = parse.quote(firstpass)
    return result

if __name__ == "__main__":
    #t = get_term_by_code(lookupService='umls', ontology='SNOMEDCT_US', code='9468002')
    #t = get_term_by_code(lookupService='umls', ontology='FMA', code='17705')
    #t = get_term_by_code(lookupService='umls', ontology='GO', codes=['GO:0005254'])
    #t = get_term_by_code(lookupService='umls', ontology='GO', codes=['GO:0005254'])
    #t = get_term_by_code(lookupService='bioportal', ontology='FMA', code='http://purl.org/sig/ont/fma/fma84666')
    #t = get_term_by_code(lookupService='ols', ontology='FMA', code='http://purl.obolibrary.org/obo/FMA_84666') # works!
    #t = get_term_by_code(lookupService='ols', ontology='FMA', code='84666')
    #t = get_term_by_code(lookupService='ols', ontology='OPB', code='00340')
    #t = get_term_by_code(lookupService='ols', ontology='CHEBI', code='17996')
    #t = get_term_by_code(lookupService='ols', ontology='GO', code='0005254')
    #t = get_term_by_code(lookupService='ols', ontology='SNOMED', code='9468002')
    t = get_term_by_code(lookupService='ols', ontology='LOINC', code='26541-3')

    print(t)

