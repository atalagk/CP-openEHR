import bioportal
import requests
from pprint import pprint

# Get the available resources
resources = bioportal.get_json("/")

# Get list of search terms
search_terms = ['heart', 'lung', 'experiment', 'human', 'brain', 'melanoma']
terms = []
for line in search_terms:
    terms.append(line)

# Do a search for every term
search_results = []
for term in terms:
    search_results.append(bioportal.get_json("/search?q=" + term)["collection"])

# Print the results
for result in search_results:
    pprint(result)
