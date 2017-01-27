import auth
import requests

def get_json(url):
    if not url.startswith('http'):
        url = auth.bioportal_url + url
    headers = {'Authorization': 'apikey token=' + auth.api_key}
    r = requests.get(url, headers=headers)

    return r.json()
