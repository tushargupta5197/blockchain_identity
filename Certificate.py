import rsa
from merkletools import *
import datetime
import yaml
import json
from base64 import b64encode, b64decode
from upload import Maker
class Certificate:
	def __init__(self, name=None, issuer=None, receiver=None, fields=None, address = 0x0, maker=None):
		self.name = name
		self.issuer = issuer
		self.receiver = receiver
		self.fields = fields
		self.fields_list = []
		self.address = address
		self.merkleTree = None
		self.merkleSigAdd = None

		if fields:
			for key in fields:
				self.fields_list.append(str(key) + ':' + str(self.fields[key]))
		self.fields_list.sort()

		self.maker = maker

	def load_from_file(self, filename):
		try:
			cert = yaml.load(open(filename))
		except:
			print("Can't open file {} for opening".format(filename))
			return False
		self.name = cert['Name']
		self.issuer = cert['Issuer']
		self.receiver = cert['Receiver']
		self.fields = cert['Attributes']
		self.fields_list = []
		self.address = cert['Address']
		self.merkleTree = None
		self.merkleSigAdd = None

		if self.fields:
			for key in self.fields:
				self.fields_list.append(str(key) + ':' + str(self.fields[key]))
		self.fields_list.sort()

		return True

	def makeMerkleTree(self):
		self.merkleTree = MerkleTools()
		self.merkleTree.reset_tree()
		self.merkleTree.add_leaf(self.fields_list, True)
		self.merkleTree.make_tree();

	def getMerkleRoot(self):
		return self.merkleTree.get_merkle_root();

	def getMerkleLeaf(self, key, value):
		statement = str(key)+':'+str(value)
		try:
			index = self.fields_list.index(statement)
		except:
			return -1
		return self.merkleTree.get_leaf(index)

	def getMerkleProof(self, key, value):
		statement = str(key)+':'+str(value)
		try:
			index = self.fields_list.index(statement)
		except:
			return -1
		return self.merkleTree.get_proof(index)

	def uploadMerkleSignature(self, issuer_skey, pkey):
		# try:
		# 	globalVs = self.yaml.load(open('globalVs.yaml'))
		# except:
		# 	print("Can't open globalVs file")
		# 	return -1

		root = self.getMerkleRoot()
		
		encrypted_root = b64encode(rsa.sign(root.encode('utf-8'), issuer_skey, 'SHA-256'))
		# globalVs['merkle_signatures'].append(encrypted_root)
		addr = self.maker.issueCertificate(encrypted_root)
		# 	with open('globalVs.yaml','w') as f:
		# 		f.write(json.dumps(globalVs, ensure_ascii=False))
		# except:
		# 	return -1

		# return globalVs['merkle_signatures'].index(encrypted_root)
		return addr



	def verifySignature(self, root, pkey, encrypted):
		decrypted = rsa.verify(root, encrypted, pkey)
		return decrypted=='SHA-256'

