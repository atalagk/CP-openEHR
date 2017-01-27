import requests
import json
import os
from pprint import pprint

url = "http://data.bioontology.org"
API_KEY = "fe19a078-5d1a-4b1d-8f91-8319260dc552"

def get_json(url):
    headers = {'Authorization': 'apikey token=' + API_KEY}
    r = requests.get(url, headers=headers)

    return r.json()

# Get the available resources
resources = get_json(url + "/")

# Get list of search terms
search_terms = ['heart', 'lung', 'experiment', 'human', 'brain', 'melanoma']
terms = []
for line in search_terms:
    terms.append(line)

# Do a search for every term
search_results = []
for term in terms:
    search_results.append(get_json(url + "/search?q=" + term)["collection"])

# Print the results
for result in search_results:
    pprint(result)