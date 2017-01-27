import tehr_auth
import sys
import requests

class EhrOperations(object):
    def __init__(self):
        header = {'Content-Type': 'application/json;charset=UTF-8'}

    def sendCompOperation(url, para, verb, data=None):
        header = {'Content-Type': 'application/json;charset=UTF-8'}

        from requests.auth import HTTPBasicAuth

        if verb == "POST":
            response = requests.post(url, data, headers=header, params=para, auth=HTTPBasicAuth(tehr_auth.username, tehr_auth.password))
        elif verb == "GET":
            response = requests.get(url, params=para, auth=HTTPBasicAuth(tehr_auth.username, tehr_auth.password))
        return response