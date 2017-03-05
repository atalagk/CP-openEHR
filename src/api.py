from flask import Flask, request
from flask import make_response
from flask_cors import CORS, cross_origin
import parse_pmr
import parsetemplate

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "You hit home"

# POST url=http://127.0.0.1:5000/pmr body: cellml=(full model PMR URL or local file path)
@app.route('/pmr', methods=['GET', 'POST'])
def pmrApi():
    if request.method == 'POST':
        location = request.form['cellml']
        annots = parse_pmr.get_annots(location)
        resp = make_response(annots)
        resp.headers['Content-Type'] = "text/json"
        return resp

    if request.method == 'GET':
        result = "you get this from GET to endpoint /pmr"
        resp = make_response(result)
        resp.headers['Content-Type'] = "text/plain"
        return resp

# POST url=http://127.0.0.1:5000/tehr body: template=(model name at ThinkEHR! server or local file path)
@app.route('/tehr', methods=['GET', 'POST'])
def tehrApi():
    if request.method == 'POST':
        location = request.form['template']
        if str(location).startswith('\\') or str(location).startswith('..'):
            annots = parsetemplate.getTermBindings(templateFile=location)
        else:
            annots = parsetemplate.getTermBindings(templateName=location)
        resp = make_response(annots)
        resp.headers['Content-Type'] = "text/json"
        return resp

    if request.method == 'GET':
        result = "you get this from GET to endpoint /tehr"
        resp = make_response(result)
        resp.headers['Content-Type'] = "text/plain"
        return resp


if __name__ == "__main__":
    app.run(debug=True)

# curl -X POST http://127.0.0.1:5000/pmr -d cellml="https://models.physiomeproject.org/workspace/267/rawfile/240aec39cbe4a481af115b02aac83af1e87acf2e/semgen-annotation/chang_fujita_1999-semgen.cellml"
# curl -X POST http://127.0.0.1:5000/tehr -d template="..\\models\KorayClinical4-webtemplate.json"
