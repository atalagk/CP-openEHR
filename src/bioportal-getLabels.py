import auth
import requests
import json
import os
from pprint import pprint

def get_json(url):
    headers = {'Authorization': 'apikey token=' + auth.api_key}
    r = requests.get(url, headers=headers)

    return r.json()

# Get all ontologies from the REST service and parse the JSON
ontologies = get_json(auth.url + "/ontologies")

# Iterate looking for ontology with acronym BRO
bro = None
for ontology in ontologies:
    if ontology["acronym"] == "OPB":
        bro = ontology

labels = []

# Using the hypermedia link called `classes`, get the first page
page = get_json(bro["links"]["classes"])

# Iterate over the available pages adding labels from all classes
# When we hit the last page, the while loop will exit
next_page = page
while next_page:
    next_page = page["links"]["nextPage"]
    for bro_class in page["collection"]:
        labels.append(bro_class["prefLabel"])
    if next_page:
        page = get_json(next_page)

# Output the labels
for label in labels:
    print (label)