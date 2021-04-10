from flask import Flask, request
from beebotte import *
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app, support_credentials=True)

_hostname  = 'api.beebotte.com'
_token = 'token_QltKufEJDKvMudky'
bbt = BBT(token = _token, hostname = _hostname)

@app.route('/to_pi',methods = ['POST'])
@cross_origin(supports_credentials=True)
def login():
    coords = request.json['coords']

    bbt.publish("DogLaser", "position", coords)
    return ""



if __name__ == '__main__':
    app.run()