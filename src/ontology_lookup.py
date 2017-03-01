import auth
import requests
import json
import pprint
from pyquery import PyQuery as pq


def get_json(url):
    if not url.startswith('http'):
        url = auth.bioportal_url + url
    headers = {'Authorization': 'apikey token=' + auth.api_key}
    r = requests.get(url, headers=headers)

    return r.json()

def get_term_by_code(**kwargs):
    lookupService = kwargs.get('lookupService', None)
    ontology = kwargs.get('ontology', None)
    codes = kwargs.get('codes', None)
    version = kwargs.get('version', 'current')

    if lookupService == 'bioportal':
        url = auth.bioportal_url
        key = auth.bioportal_api_key
    elif lookupService == 'umls':
        url = 'https://utslogin.nlm.nih.gov'
        key = '3490a7de-1062-46e8-a577-701855ba35c8'    #auth.umls_api_key

        auth_endpoint = "/cas/v1/api-key"
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        params = {'apikey': key}
        r = requests.post(url + auth_endpoint, data=params, headers=h)
        d = pq(r.text)
        tgt = d.find('form').attr('action')

        results = []
        for code in codes:
            params = {'service': 'http://umlsks.nlm.nih.gov'}
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
    #t = get_term_by_code(lookupService='umls', ontology='FMA', codes=['17705', '84669', '84666', '71132', '7131'])
    #t = get_term_by_code(lookupService='umls', ontology='GO', codes=['GO:0005254'])
    t = get_term_by_code(lookupService='umls', ontology='GO', codes=['GO:0005254'])
    for term in t:
        print(term)

