import rsa
from merkletools import *
import datetime

# Initialization of blockchain
issuers = ["birth", "passport_office"]
pkey_dic = {}
skey_dic = {}
keypair_dic = {}
for issuer in issuers:
	keypair = rsa.newkeys(1024)
	skey_dic[issuer] = keypair[1]
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

	def uploadMerkleSignature(self):
		root = self.getMerkleRoot()
		issuer_skey = skey_dic[self.issuer]
		encrypted_root = rsa.sign(root, issuer_skey, 'SHA-256')
		merkle_signatures.append(encrypted_root)
		return merkle_signatures.index(encrypted_root)

	def verifySignature(self, root, pkey, encrypted):
		decrypted = rsa.verify(root, encrypted, pkey)
		return decrypted=='SHA-256'

	# def signAndUploadMerkleRoot()


bc = Certificate(name = "Birth Certificate", issuer = "birth", receiver = "Bob", fields = birth_certificate)
bc.makeMerkleTree()
root = (bc.getMerkleRoot())
leaf = (bc.getMerkleLeaf('mother','Chunni Lal'))
proof = (bc.getMerkleProof('mother','Chunni Lal'))
print(root)
print(leaf)
print(proof)
print(bc.merkleTree.validate_proof(proof, leaf, root))
# bc.uploadMerkleSignature()
index = bc.uploadMerkleSignature()
print(bc.verifySignature(root, pkey_dic[bc.issuer], merkle_signatures[index]))

# signature = rsa.sign(root, skey_dic['birth'], 'SHA-256')
# print(rsa.verify(root, signature, pkey_dic['birth']))