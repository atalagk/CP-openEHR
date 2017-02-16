import requests
import json
import xmltodict
from collections import OrderedDict
import pprint


url = 'https://models.physiomeproject.org'

url += '/workspace/267/rawfile/59b35d8439d9ea5e9309bc461e2b795dd1d8c796/semgen-annotation/chang_fujita_1999-semgen.cellml'


def get_model(url):
    headers = {'Accept': 'Accept: application/vnd.physiome.pmr2.json.1'}
    r = requests.get(url, headers=headers)
    return r.text




xml = get_model(url)

namespaces = {'http://www.cellml.org/cellml/1.1#': None} #,
              #'http://a.com/': 'ns_a'} # collapse "http://a.com/" -> "ns_a"

d = xmltodict.parse(xml)

#j = json.dumps(d, indent=4)

i = OrderedDict(d)

o = i['model']['rdf:RDF']['rdf:Description'][100]   #['@rdf:about']

for x in o:
    print(o['semsim:hasPhysicalDefinition'])

quit()

print(o)

quit()

for k, v in o:
    print(k)
