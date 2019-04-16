import rsa
from merkletools import *
from hashlib import sha256
import json
from Certificate import Certificate
import yaml
from base64 import b64decode
import requests
from upload import Maker
import random
import sqlite3
from contextlib import closing


class Issuer:
	def __init__(self, name = None, keypair = None, schema = None, cert_name = None, db=None):
		self.name = name
		if keypair == None:
			self.keypair = rsa.newkeys(1024)
		else:
			self.keypair = keypair

		self.cert_name = cert_name
		self.schema = yaml.load(open(schema))
		self.db = db

	def verify_field(self, key, value, signature, root, proof, pkey):
		mt = MerkleTools()
		val = str(key)+':'+str(value)
		val =val.encode('utf-8')
		root_verified = mt.validate_proof(proof, sha256(val).hexdigest(), root)
		if not root_verified:
			print("Incorrect Merkle Root")
			return False

		try:
			print(root)
			print(signature)

			rsa.verify(root.encode('utf-8'), b64decode(signature), pkey)
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

	def issue(self, proofs, values, receiver, maker_addr, recv_ssn):

		# globalVs = yaml.load(open('globalVs.yaml'))
		# conn = sqlite3.connect('GlobalVs.db')
		# c = conn.cursor()

		
		if self.schema['Proof_Request']:
			for attr in self.schema['Proof_Request']:
				if attr not in values:
					print("Value not provided: "+attr)
					return '{'+'}'
		maker = Maker(maker_addr)
		if self.schema['Verifiable']:
			for attr in self.schema['Verifiable'].keys():
				if attr not in proofs:
					print("Proof not provided: "+attr)
					return '{'+'}'
				with closing(sqlite3.connect('GlobalVs.db')) as con, con, closing(con.cursor()) as c:
					query = """SELECT url FROM GlobalVs WHERE InstituteName = '{}';""".format(self.schema['Verifiable'][attr])
					# c = conn.cursor()
					c.execute(query)
					result = c.fetchall()
					url = result[0][0]
				print(result)
				response = requests.get(url+'pkey')
				addr = proofs[attr]['address']
				
				sig = maker.getHash(addr)
				if(not self.verify_field(key = attr, 
									value = values[attr], 
									signature = sig, 
									root = proofs[attr]['root'], 
									proof = proofs[attr]['proof'],
									pkey = rsa.PublicKey.load_pkcs1(response.json()['pkey'])
									)
				):
					print("Proof Verification Failed: "+attr)
					return '{'+'}'

		fields = {}
		for attr in self.schema['Attributes']:
			if attr == 'ssn':
				fields[attr] = recv_ssn
			elif attr in values:
				fields[attr]=values[attr]
			else:
				fields[attr]=self.db[recv_ssn][attr]
			fields['nonce'] = hex(random.getrandbits(256))

		newCertificate = Certificate(name=self.cert_name, issuer = self.name, receiver=receiver, fields = fields, maker=maker)
		# Insert into blockchain, return the address

		newCertificate.makeMerkleTree()
		address = newCertificate.uploadMerkleSignature(self.keypair[1], self.keypair[0])
		if address == -1:
			print("Certificate Can't be uploaded to Blockchain")
			return '{'+'}'


		return self.certi_to_string(name = newCertificate.name, receiver = receiver, attr = fields, address=address)


