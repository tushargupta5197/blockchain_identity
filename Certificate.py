import rsa
from merkletools import *
import datetime
import globalVs
import yaml


class Certificate:
	def __init__(self, name, issuer, receiver, fields, address = 0x0):
		self.name = name
		self.issuer = issuer
		self.receiver = receiver
		self.fields = fields
		self.fields_list = []
		self.address = address
		self.merkleTree = None
		self.merkleSigAdd = None

		for key in fields:
			self.fields_list.append(str(key) + ':' + str(self.fields[key]))

	def __init__(self, filename):
		cert = yaml.load(open(filename))
		self.name = cert['Name']
		self.issuer = cert['Issuer']
		self.receiver = cert['Receiver']
		self.fields = cert['Attributes']
		self.fields_list = []
		self.address = cert['Address']
		self.merkleTree = None
		self.merkleSigAdd = None

		for key in fields:
			self.fields_list.append(str(key) + ':' + str(self.fields[key]))

	def makeMerkleTree(self):
		self.merkleTree = MerkleTools()
		self.merkleTree.reset_tree()
		self.merkleTree.add_leaf(self.fields_list, True)
		self.merkleTree.make_tree();

	def getMerkleRoot(self):
		return self.merkleTree.get_merkle_root();

	def getMerkleLeaf(self, key, value):
		statement = str(key)+':'+str(value)
		index = self.fields_list.index(statement)
		return self.merkleTree.get_leaf(index)

	def getMerkleProof(self, key, value):
		statement = str(key)+':'+str(value)
		index = self.fields_list.index(statement)
		return self.merkleTree.get_proof(index)

	def uploadMerkleSignature(self, issuer_skey):
		root = self.getMerkleRoot()
		encrypted_root = rsa.sign(root, issuer_skey, 'SHA-256')
		globalVs.merkle_signatures.append(encrypted_root)
		return globalVs.merkle_signatures.index(encrypted_root)

	def verifySignature(self, root, pkey, encrypted):
		decrypted = rsa.verify(root, encrypted, pkey)
		return decrypted=='SHA-256'

	# def signAndUploadMerkleRoot()
