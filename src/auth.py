import json
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the relative path to login.json
json_path = os.path.join(script_dir, 'login.json')

with open(json_path) as login_details:
    login = json.load(login_details)

# Use local instance of EHRScape Cloud or other

server = login["cdr-server"]
ols = login["ols-server"]

# Server for openEHR Clinical Data Repository (CDR)
baseUrl = login["cdrs"][server]["baseUrl"]
ehrId = login["cdrs"][server]["ehrId"]
username = login["cdrs"][server]["username"]
password = login["cdrs"][server]["password"]

# Bioportal
bioportal_url = login["bioportal"]["url"]
bioportal_api_key = login["bioportal"]["API_KEY"]

# OLS
ols_url = login["ols"][ols]["url"]

# UMLS
umls_url = login["umls"]["url"]
umls_tgt_url = login["umls"]["tgt_url"]
umls_st_url = login["umls"]["st_url"]
umls_api_key = login["umls"]["API_KEY"]


if __name__ == "__main__":
    print(baseUrl)
    print (username)