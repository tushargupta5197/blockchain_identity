from flask import Flask, request
from flask_restful import Resource, Api 
from flask_jsonpify import jsonify
import rsa
import sys
sys.path.append('../')
from Issuer import Issuer 
import json

app = Flask(__name__)

abc_univ = Issuer(name='ABC University', schema='schemas/transcript.yaml', cert_name = 'transcript')

@app.route("/")
def hello():
	return "<b> Page of ABC University </b>"

@app.route("/pkey")
def get_pkey():
	return jsonify({"pkey":abc_univ.keypair[0].save_pkcs1()})

@app.route("/cert_name")
def get_cert_name():
	return jsonify({"cert_name":"transcript"})

@app.route("/cert_schema")
def get_schema():
	return jsonify(abc_univ.schema)

@app.route("/get_cert", methods = ['POST'])
def issue():
	# dis = {'answer':str(int(request.json['a'])+int(request.json['b']))}

	# print(request.json)

	proofs = request.json['proofs']
	values = request.json['values']
	receiver = request.json['receiver']

	response = json.loads(abc_univ.issue(proofs = proofs, values = values, receiver = receiver))
	if response == {}:
		return response,400
	return jsonify(response),201

if __name__ == '__main__':
	app.run(port=8080)