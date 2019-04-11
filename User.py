import rsa
import globalVs
import yaml
import json
from Certificate import Certificate

from Issuer import Issuer


class User:
	def __init__(self, name = None, wallet_file = None, keypair = None):
		self.name = name
		self.wallet_file = wallet_file
		self.wallet = yaml.load(open(wallet_file))

		if keypair == None:
			self.keypair = rsa.newkeys(1024)
		else:
			self.keypair = keypair


	def requestCertificate(self, issuer, values = None, issuer_obj):
		schema = yaml.load(open('schemas/' + globalVs.CertiName[issuer]+'.yaml'))
		proof_req = schema['Proof_Request']
		verifiable = schema['Verifiable']

		proof = {}

		for verifiable_attr in verifiable.keys():
			proof_issuer = verifiable[verifiable_attr]
			cert_name = globalVs.CertiName[proof_issuer]
			cert_file = self.wallet[cert_name]
			cert_obj = Certificate(filename = cert_file)
			cert_obj.makeMerkleTree()
			cert_root = cert_obj.getMerkleRoot()
			cert_leaf = cert_obj.getMerkleLeaf(key = verifiable_attr, value = values[verifiable_attr])
			cert_proof = cert_obj.getMerkleProof(key = verifiable_attr, value = values[verifiable_attr])
			attr_proof = {}

			attr_proof['address'] = cert_obj.address
			attr_proof['proof'] = cert_proof
			attr_proof['root'] = cert_root

			proof[verifiable_attr] = attr_proof

		cert_str = issuer_obj.issue(proof, values, self.name)
		cert_dic = json.loads(cert_str)
		cert_filename = 'certificates/'+cert_dic['name']+'.yaml'
		self.wallet[cert_dic['name']] = cert_filename

		with open(cert_filename, 'w') as f:
			f.write(cert_str)

		with open(self.wallet_file, 'w') as f:
			f.write(json.dumps(self.wallet))



