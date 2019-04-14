import rsa
import json
from Certificate import Certificate
import requests
import yaml
from Issuer import Issuer


class User:
	def __init__(self, name = None, wallet_file = None, keypair = None):

		self.name = name
		self.wallet_file = wallet_file
		self.wallet = yaml.load(open(wallet_file, 'w+'))
		if(self.wallet == None):
			self.wallet = {}
		if keypair == None:
			self.keypair = rsa.newkeys(1024)
		else:
			self.keypair = keypair


	def requestCertificate(self, issuer, values = None):
		globalVs = yaml.load(open('globalVs.yaml'))

		schema = requests.get(globalVs['url'][issuer]+'cert_schema')
		if schema.status_code < 300:
			schema = schema.json()
		else:
			print("{} server didn't send certificate Schema". format(issuer))
			print("Aborting....")
			return 

		certificate_requested = requests.get(globalVs['url'][issuer]+'cert_name')

		if certificate_requested.status_code < 300:
			certificate_requested = certificate_requested.json()['cert_name']
		else:
			print("{} server didn't send certificate Name". format(issuer))
			print("Aborting....")
			return

		proof_req = schema['Proof_Request']
		verifiable = schema['Verifiable']

		proof = {}
		if verifiable:
			for verifiable_attr in verifiable:
				proof_issuer = verifiable[verifiable_attr]
				cert_name = requests.get(globalVs['url'][proof_issuer]+'cert_name')
				if cert_name.status_code<300:
					cert_name = cert_name.json()['cert_name']
				else:
					print("{} server didn't send certificate Name". format(proof_issuer))
					print("Aborting....")
					return
				try:
					cert_file = self.wallet[cert_name]
				except:
					print(cert_name + " certificate not found in wallet")
					print("Aborting....")
					return
				cert_obj = Certificate()
				cert_obj.load_from_file(cert_file)
				cert_obj.makeMerkleTree()
				cert_root = cert_obj.getMerkleRoot()
				cert_leaf = cert_obj.getMerkleLeaf(key = verifiable_attr, value = values[verifiable_attr])
				statement = str(verifiable_attr) + ':' + str(values[verifiable_attr])
				if(cert_leaf == -1):
					print("Can't find leaf {}  in the merkle tree".format(statement))
					print("Aborting....")
					return
				cert_proof = cert_obj.getMerkleProof(key = verifiable_attr, value = values[verifiable_attr])
				if(cert_proof == -1):
					print("Can't find the proof of {}  in the merkle tree".format(statement))
					print("Aborting....")
					return

				attr_proof = {}

				attr_proof['address'] = cert_obj.address
				attr_proof['proof'] = cert_proof
				attr_proof['root'] = cert_root

				proof[verifiable_attr] = attr_proof
		response = requests.post(globalVs['url'][issuer]+'get_cert',json = {"proofs":proof, "values":values, "receiver":self.name})

		if( response.status_code < 300):
			cert_dic = response.json()
			cert_filename = 'certificates/'+cert_dic['Name']+'.yaml'
			self.wallet[cert_dic['Name']] = cert_filename

			with open(cert_filename, 'w') as f:
				f.write(json.dumps(cert_dic))

			with open(self.wallet_file, 'w') as f:
				f.write(json.dumps(self.wallet))
			print(cert_filename + " Acquired")
		else:
			print ("Failed to get certificate: ", certificate_requested)


