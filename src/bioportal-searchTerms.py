import bioportal
from pprint import pprint

include = ''
include = "&ontologies=SNOMEDCT"
include += "&display_context=false"
#include += "&cui=C0018799"
include += "&include=prefLabel,cui" # ,cui
#include += "&suggest=true"
include += "&require_exact_match=true"
include += "&display_links=false"

# Get the available resources
resources = bioportal.get_json("/")


# Get list of search terms
#search_terms = ['http%3A%2F%2Fbhi.washington.edu%2FOPB%23OPB_00340', 'http%3A%2F%2Fbhi.washington.edu%2FOPB%23OPB_01023']     #, 'gastritis', 'experiment', 'human', 'brain', 'melanoma']
search_terms = ['Acute Coronary Syndrome']
terms = []
for line in search_terms:
    terms.append(line)

# Do a search for every term
search_results = []
for term in terms:
    search_results.append("You searched: " + term)
    search_results.append(bioportal.get_json("/search?q=" + term + include)["collection"])   #[0]["prefLabel"])

# Print the results
for result in search_results:
    pprint(result)
