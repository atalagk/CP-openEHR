import requests
import json
import xmltodict
from collections import OrderedDict
import pprint

'''
chang_fujita_1999
chang_fujita_b_1999
eskandari_2005
mackenzie_1996
moss_2009
thomas_2000
weinstein_1995
'''

def setpmrurl(cellmlname):
    url = 'https://models.physiomeproject.org'
    url += '/workspace/267/rawfile/59b35d8439d9ea5e9309bc461e2b795dd1d8c796/semgen-annotation/'
    url += cellmlname
    return url

def get_model(url):
    headers = {'Accept': 'Accept: application/vnd.physiome.pmr2.json.1'}
    r = requests.get(url, headers=headers)
    return r.text


if __name__ == "__main__":
    print('you run main')

    url = setpmrurl('chang_fujita_1999-semgen.cellml')
    xml = get_model(url)

    d = xmltodict.parse(xml)

    al = d['model']['rdf:RDF']['rdf:Description']

    an = al[10:len(al):]
    j = json.dumps(an)


    quit()
    o = an[12]  # ['dcterms:title']   #['@rdf:about']
    for v in o:
        x = o[v]
        print(x)

    quit()
    o = d['model']['rdf:RDF']['rdf:Description'][12]  # ['dcterms:title']   #['@rdf:about']
    for v in o:
        x = o[v]
        print(x)



