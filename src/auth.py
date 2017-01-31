import json

isLocal = True

with open('login.json') as login_details:
    login = json.load(login_details)

# openEHR Clinical Data Repository (CDR)
if isLocal:
    baseUrl = login["thinkehr"]["local-tehr"]["baseUrl"]
    ehrId = login["thinkehr"]["local-tehr"]["ehrId"]
    username = login["thinkehr"]["local-tehr"]["username"]
    password = login["thinkehr"]["local-tehr"]["password"]
else:
    baseUrl = login["thinkehr"]["ehrscape-abi"]["baseUrl"]
    ehrId = login["thinkehr"]["ehrscape-abi"]["ehrId"]
    username = login["thinkehr"]["ehrscape-abi"]["username"]
    password = login["thinkehr"]["ehrscape-abi"]["password"]

# Bioportal
bioportal_url = login["bioportal"]["url"]
api_key = login["bioportal"]["API_KEY"]

if __name__ == "__main__":
    print(baseUrl)
    print (username)