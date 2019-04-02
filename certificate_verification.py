import rsa
from merkletools import *
import datetime

# Initialization of blockchain
issuers = ["birth", "passport_office"]
pkey_dic = {}
keypair_dic = {}
for issuer in issuers:
	keypair = rsa.newkeys(512)
	keypair_dic[issuer] = keypair
	pkey_dic[issuer] = keypair[0]

merkle_signatures = []

certificates = {}
# birth_certificate creating
birth_certificate = {
	'name':'Bob',
	'dob':'05/01/1997',
	'father':'Charan Lal',
	'mother':'Chunni Lal'
}

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

	# def signAndUploadMerkleRoot()


bc = Certificate("Birth Certificate", "Govt", "Bob", birth_certificate)
bc.makeMerkleTree()
root = (bc.getMerkleRoot())
leaf = (bc.getMerkleLeaf('mother','Chunni Lal'))
proof = (bc.getMerkleProof('mother','Chunni Lal'))
print(root)
print(leaf)
print(proof)
print(bc.merkleTree.validate_proof(proof, leaf, root))