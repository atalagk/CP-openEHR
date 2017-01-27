import requests
import pprint

isLocal = True  #if false defaults to Ehrscape
data = None

if isLocal:
    baseUrl = 'http://130.216.208.42:8081/rest/v1'
    ehrId = 'd7725334-4e54-4cb1-81d7-501891449bbc'  #Local
    username = "koray"
    password = "123456"
else:
    baseUrl = 'https://rest.ehrscape.com/rest/v1'
    ehrId = '6f81d77a-26ef-4cf4-926f-40ccfafd8a1f'  #Ehrscape
    username = "k.atalag@auckland.ac.nz"   #"guidemo"
    password = "ehr4k.atalag"     #"gui?!demo123"

def getEhr():
    url = baseUrl + '/ehr/' + ehrId
    from requests.auth import HTTPBasicAuth
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    return response

def getView():
    url = baseUrl + "/view/" + ehrId + "/body_temperature"
    #url = baseUrl + "/view/" + ehrId + "/blood_pressure"
    #url = baseUrl + "/view/" + ehrId + "/pulse"
    #data = {'from':'2014-3-1'}
    from requests.auth import HTTPBasicAuth
    response = requests.get(url, data, auth=HTTPBasicAuth(username, password))
    return response

def getComp():
    url = baseUrl + "/composition/" + 'e9f628af-6721-4ea1-8e1f-5225c1aa2beb::default::1'    #"ehrId": "99aaaac3-9fbd-4dca-a130-20355c50df12" (148-152, step 4, break 10)
    from requests.auth import HTTPBasicAuth
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    return response

def getForms(**kwargs):
    formName = kwargs.get('formName', None)
    formVersion = kwargs.get('formVersion', None)
    formResources = kwargs.get('formResources', None)
    url = baseUrl + "/form/"
    if formName:
        url += formName
    if formVersion:
        url += '/' + formVersion
    if formResources:
        formResources = {'resources': formResources}
    from requests.auth import HTTPBasicAuth
    response = requests.get(url, params=formResources, auth=HTTPBasicAuth(username, password))
    print(response.url)
    return response

def getWebTemplate(**kwargs):
    #http://130.216.208.42:8081/rest/v1/template/DogAPTrace-annot
    templateName = kwargs.get('templateName', None)
    templatePath = kwargs.get('templatePath', None)
    url = baseUrl + "/template/"
    if templateName:
        url += templateName
    if templatePath:
        url += '/' + templatePath
    from requests.auth import HTTPBasicAuth
    response = requests.get(url, params=templatePath, auth=HTTPBasicAuth(username, password))
    #print(response.url)
    return response


if __name__ == "__main__":
    #r = getWebTemplate(templateName='DogAPTrace-annot')
    #r = getComp().json()
    #r = getEhr().json()
    #r = getView().json()
    #r = getForms().json()
    #r = getForms(formName='ABI1', formVersion='1.0.0', formResources='ALL').json()

    #print(r)

    #for items in r['composition']:
        #print(items)
        #print(items + ": ", r['composition'][items])
        #print(items, r[items])
        #print(r['composition'])
        #print('temp:' + str(items['temperature']))

    r = getEhr().json()
    print(r['ehrId'])
    for k, v in r['ehrStatus'].items():
        print(k, v)
