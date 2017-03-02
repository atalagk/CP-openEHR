import auth
import requests
import json
from pyquery import PyQuery as pq


def get_term_by_code(**kwargs):
    lookupService = kwargs.get('lookupService', None)
    ontology = kwargs.get('ontology', None)
    codes = kwargs.get('codes', None)
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

        results = []
        for code in codes:
            urlnext = url + '/search?q=' + code + include
            r = requests.get(urlnext, headers=headers)
            js = r.json()["collection"][0]["prefLabel"]
            results.append(js)
        return results

    elif lookupService == 'umls':
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        params = {'apikey': auth.umls_api_key}
        r = requests.post(auth.umls_tgt_url, data=params, headers=h)
        d = pq(r.text)
        tgt = d.find('form').attr('action')

        results = []
        for code in codes:
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
            results.append(result)
        return results


if __name__ == "__main__":
    # t = get_term_by_code(lookupService='umls', ontology='SNOMEDCT_US', code='9468002')
    t = get_term_by_code(lookupService='umls', ontology='FMA', codes=['17705', '84669', '84666', '71132', '7131'])
    #t = get_term_by_code(lookupService='umls', ontology='GO', codes=['GO:0005254'])
    #t = get_term_by_code(lookupService='umls', ontology='GO', codes=['GO:0005254'])
    #t = get_term_by_code(lookupService='bioportal', ontology='FMA', codes=['http://purl.org/sig/ont/fma/fma84666', 'http://purl.org/sig/ont/fma/fma84669'])

    for term in t:
        print(term)

