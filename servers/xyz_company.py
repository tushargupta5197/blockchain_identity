from flask import Flask, request
from flask_restful import Resource, Api 
from flask_jsonpify import jsonify
import rsa
import sys
sys.path.append('../')
from Issuer import Issuer 
import json

app = Flask(__name__)

xyz_company = Issuer(name='XYZ Company', schema='schemas/job_application.yaml', cert_name = 'job_application')

@app.route("/")
def hello():
	with open("servers/company.html", 'r') as f:
		return f.read().format("XYZ Company", "<p>Degree : BTech</p><p>Status : Graduated</p>", "8081")

@app.route("/pkey")
def get_pkey():
	return jsonify({"pkey":xyz_company.keypair[0].save_pkcs1()})

@app.route("/cert_name")
def get_cert_name():
	return jsonify({"cert_name":"job_application"})

@app.route("/cert_schema")
def get_schema():
	return jsonify(xyz_company.schema)

@app.route("/get_cert", methods = ['POST'])
def issue():
	# dis = {'answer':str(int(request.json['a'])+int(request.json['b']))}

	# print(request.json)

	proofs = request.json['proofs']
	values = request.json['values']
	receiver = request.json['receiver']

	response = json.loads(xyz_company.issue(proofs = proofs, values = values, receiver = receiver))

	return jsonify(response),201

if __name__ == '__main__':
	app.run(port=8081)