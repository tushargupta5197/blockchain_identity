import rsa
import yaml
from merkletools import *
from hashlib import sha256
import globalVs

class Issuer:
	def __init__(self, name = None, keypair = None, schema = None):
		self.name = name
		if keypair == None:
			self.keypair = rsa.newkeys(1024)
		else:
			self.keypair = keypair

		self.schema = yaml.load(open(schema))

	def verify_field(self, key, value, signature, root, proof, pkey):
		mt = MerkleTools()
		root_verified = mt.validate_proof(proof, sha256(str(key)+':'+str(value)).hexdigest(), root)
		if not root_verified:
			print("Incorrect Merkle Root")
			return False

		if not rsa.verify(root, signature, pkey):
			print("Signature mismatch")
			return False
		return True

	#proofs : dictionary of field and proof
	#values : dictionary of field and values
	def issue(self, proofs, values, Upubkey):
		
		for attr in self.schema['Proof_Request']:
			if attr not in values:
				print("Value not provided: "+attr)
				return False

		for attr in self.schema['Verifiable']:
			if attr not in proofs:
				print("Proof not provided: "+attr)
				return False

			if(!self.verify_field(key = attr, value = values[attr])):
				print("Proof Verification Failed: "+attr)
				return False

		fields = {}
		for attr in self.certificate['Attributes']:
			if attr in values:
				fields[attr]=values[attr]
			else:
				fields[attr]=1 #Will be replaced with random quantity


		newCertificate = Certificate(name=globalVs.CertiName[self.name], issuer = self.name, receiver=Upubkey, fields = fields)
		# Insert into bloackchain, return the address
		


				



# issuer= Issuer(schema = 'schemas/job_application.yaml')

# m = MerkleTools()
# l = ['name:loda', 'age:15']
# m.add_leaf(l, True)
# m.make_tree()
# leaf = m.get_leaf(1)
# proof = m.get_proof(1)
# root = m.get_merkle_root()

# kp = rsa.newkeys(1024)
# signature = rsa.sign(root, kp[1], 'SHA-256')
# print(issuer.verify_field(key = 'age', value = 15, signature = signature, root = root, proof = proof, pkey = kp[0]))
