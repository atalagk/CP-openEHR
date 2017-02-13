import bioportal
import requests
from pprint import pprint

include = "&ontologies=SNOMEDCT&display_context=false"
#include += "&cui=C0018799"
include += "&include=prefLabel,cui"
#include += "&suggest=true"
include += "&require_exact_match=true"
#include += "&display_links=false"

# Get the available resources
resources = bioportal.get_json("/")


# Get list of search terms
search_terms = ['Acute coronary syndrome']     #, 'gastritis', 'experiment', 'human', 'brain', 'melanoma']
terms = []
for line in search_terms:
    terms.append(line)

# Do a search for every term
search_results = []
for term in terms:
    search_results.append("You searched: " + term)
    search_results.append(bioportal.get_json("/search?q=" + term + include)["collection"])

# Print the results
for result in search_results:
    pprint(result)
