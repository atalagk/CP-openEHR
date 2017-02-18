from flask import Flask, request
from flask import make_response
import parse_pmr
app = Flask(__name__)

@app.route("/")
def home():
    return "You hit home"

@app.route('/pmr', methods=['GET', 'POST'])
def pyapi():
    if request.method == 'POST':
        modelname = request.form['cellml']
        annotjson = parse_pmr.get_annots(modelname)
        resp = make_response(annotjson)
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