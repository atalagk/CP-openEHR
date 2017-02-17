from flask import Flask, request
from flask import make_response
app = Flask(__name__)

@app.route("/")
def home():
    return "You hit home"

@app.route('/pmr', methods=['GET', 'POST'])
def login():

    def getpmrurl(cellmlname):
        url = 'https://models.physiomeproject.org'
        url += '/workspace/267/rawfile/59b35d8439d9ea5e9309bc461e2b795dd1d8c796/semgen-annotation/'
        url += cellmlname
        return url

    def get_model(url):
        import requests
        headers = {'Accept': 'Accept: application/vnd.physiome.pmr2.json.1'}
        r = requests.get(url, headers=headers)
        return r.text

    def get_annot(cellml):
        import xmltodict, json
        url = getpmrurl('chang_fujita_1999-semgen.cellml')
        xml = get_model(url)
        d = xmltodict.parse(xml)

        al = d['model']['rdf:RDF']['rdf:Description']

        an = al[10:len(al):]
        j = json.dumps(an)

        return j


    if request.method == 'POST':
        modelname = request.form['cellml']
        pmrurl = getpmrurl(modelname)
        cellmodel = get_model(pmrurl)
        annots = get_annot(cellmodel)
        resp = make_response(annots)
        resp.headers['Content-Type'] = "text/json"
        return resp

    if request.method == 'GET':
        result = "you get this from GET"
        resp = make_response(result)
        resp.headers['Content-Type'] = "text/plain"
        return resp


if __name__ == "__main__":
    app.run(debug = True)

# curl -X POST http://127.0.0.1:5000/pmr -d cellml="chang_fujita_1999-semgen.cellml"