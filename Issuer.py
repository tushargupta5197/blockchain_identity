import rsa
from merkletools import *
from hashlib import sha256
import json
from Certificate import Certificate
from ruamel.yaml import YAML
from base64 import b64decode
import requests


class Issuer:
	def __init__(self, name = None, keypair = None, schema = None, cert_name = None):
		self.name = name
		if keypair == None:
			self.keypair = rsa.newkeys(1024)
		else:
			self.keypair = keypair
		self.yaml = YAML()

		self.cert_name = cert_name
		self.schema = self.yaml.load(open(schema))

	def verify_field(self, key, value, signature, root, proof, pkey):
		mt = MerkleTools()
		root_verified = mt.validate_proof(proof, sha256(str(key)+':'+str(value)).hexdigest(), root)
		if not root_verified:
			print("Incorrect Merkle Root")
			return False

		try:
			rsa.verify(root, b64decode(signature), pkey)
			return True
		except:
			print("Signature mismatch")
			return False

	#proofs : dictionary of field and proof
	#values : dictionary of field and values

	def certi_to_string(self, name=None, receiver=None, attr=None, address=None):
		return json.dumps(
			{
				'Name':name,
				'Issuer': self.name,
				'Receiver': receiver,
				'Attributes': attr,
				'Address': address
			}
		)

	def issue(self, proofs, values, receiver):

		globalVs = self.yaml.load(open('globalVs.yaml'))
		
		if self.schema['Proof_Request']:
			for attr in self.schema['Proof_Request']:
				if attr not in values:
					print("Value not provided: "+attr)
					return '{'+'}'

		if self.schema['Verifiable']:
			for attr in self.schema['Verifiable'].keys():
				if attr not in proofs:
					print("Proof not provided: "+attr)
					return '{'+'}'

				response = requests.get(globalVs['url'][self.schema['Verifiable'][attr]]+'pkey')

				if(not self.verify_field(key = attr, 
									value = values[attr], 
									signature = globalVs['merkle_signatures'][int(proofs[attr]['address'])], 
									root = proofs[attr]['root'], 
									proof = proofs[attr]['proof'],
									pkey = rsa.PublicKey.load_pkcs1(response.json()['pkey'])
									)
				):
					print("Proof Verification Failed: "+attr)
					return '{'+'}'

		fields = {}
		for attr in self.schema['Attributes']:
			if attr in values:
				fields[attr]=values[attr]
			else:
				fields[attr]=str(1)#raw_input(attr+': ') #Will be replaced with random quantity

		newCertificate = Certificate(name=self.cert_name, issuer = self.name, receiver=receiver, fields = fields)
		# Insert into blockchain, return the address

		newCertificate.makeMerkleTree()
		address = newCertificate.uploadMerkleSignature(self.keypair[1], self.keypair[0])
		if address == -1:
			print("Certificate Can't be uploaded to Blockchain")
			return '{'+'}'


		return self.certi_to_string(name = newCertificate.name, receiver = receiver, attr = fields, address=address)


