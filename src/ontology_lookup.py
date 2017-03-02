import auth
import requests
import json
from pyquery import PyQuery as pq


def get_term_by_code(**kwargs):
    lookupService = kwargs.get('lookupService', None)
    ontology = kwargs.get('ontology', None)
    code = kwargs.get('code', None)
    version = kwargs.get('version', 'current')
    newurl = kwargs.get('url_extension', None)

    if lookupService == 'bioportal':
        url = auth.bioportal_url
        headers = {'Authorization': 'apikey token=' + auth.bioportal_api_key}

        include = ''
        #include = "&ontologies=SNOMEDCT"
        include += "&display_context=false"
        # include += "&cui=C0018799"
        include += "&include=prefLabel"  # ,cui
        # include += "&suggest=true"
        include += "&require_exact_match=true"
        include += "&display_links=false"

        urlnext = url + '/search?q=' + code + include
        r = requests.get(urlnext, headers=headers)
        label = r.json()["collection"][0]["prefLabel"]
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

        url = 'https://uts-ws.nlm.nih.gov'
        query = {'ticket': st}
        content_endpoint = "/rest/content/" + str(version) + "/source/" + str(ontology) + "/" + str(code)
        r = requests.get(url + content_endpoint, params=query)
        r.encoding = 'utf-8'
        items = json.loads(r.text)
        result = items["result"]["name"]
        return result


if __name__ == "__main__":
    # t = get_term_by_code(lookupService='umls', ontology='SNOMEDCT_US', code='9468002')
    #t = get_term_by_code(lookupService='umls', ontology='FMA', code='17705')
    #t = get_term_by_code(lookupService='umls', ontology='GO', codes=['GO:0005254'])
    #t = get_term_by_code(lookupService='umls', ontology='GO', codes=['GO:0005254'])
    t = get_term_by_code(lookupService='bioportal', ontology='FMA', code='http://purl.org/sig/ont/fma/fma84666')

    print(t)

