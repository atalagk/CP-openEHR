import json

with open('login.json') as login_details:
    login = json.load(login_details)

# Use local instance of EHRScape Cloud or other

server = login["cdr-server"]
ols = login["ols-server"]

# Server for openEHR Clinical Data Repository (CDR)
baseUrl = login["thinkehr"][server]["baseUrl"]
ehrId = login["thinkehr"][server]["ehrId"]
username = login["thinkehr"][server]["username"]
password = login["thinkehr"][server]["password"]

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