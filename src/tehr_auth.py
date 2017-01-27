import json

isLocal = True

with open('login.json') as login_details:
    login = json.load(login_details)

if isLocal:
    baseUrl = login["thinkehr"]["local"]["baseUrl"]
    ehrId = login["thinkehr"]["local"]["ehrId"]
    username = login["thinkehr"]["local"]["username"]
    password = login["thinkehr"]["local"]["password"]
else:
    baseUrl = login["thinkehr"]["ehrscape-abi"]["baseUrl"]
    ehrId = login["thinkehr"]["ehrscape-abi"]["ehrId"]
    username = login["thinkehr"]["ehrscape-abi"]["username"]
    password = login["thinkehr"]["ehrscape-abi"]["password"]

if __name__ == "__main__":
    print (username)