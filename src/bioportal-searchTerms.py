import bioportal
import requests
from pprint import pprint

include = "&ontologies=SNOMEDCT&include=prefLabel&display_context=false&display_links=false"

# Get the available resources
resources = bioportal.get_json("/")


# Get list of search terms
search_terms = ['arteriosclerosis', 'thumb']     #, 'gastritis', 'experiment', 'human', 'brain', 'melanoma']
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
