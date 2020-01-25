import json
from flask import jsonify
import naveen
from naveen import centreFinder
from flask import request
from flask import Flask

app = Flask(__name__)
app.debug=True

@app.route('/maps',methods = ['POST'])
def maps():
    j = request.get_json()
    a = j['data'][0]
    b = j['data'][1]
    c = j['data'][2]
    d = j['data'][3]
    output = centreFinder(a,b,c,d)

    return jsonify(output)

@app.route('/test',methods = ['GET'])
def test():
    return 'done'

app.run(host='0.0.0.0')