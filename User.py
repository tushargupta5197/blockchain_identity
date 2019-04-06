import rsa


class User:
	def __init__(self, name = None, wallet = [], keypair = None):
		self.name = name
		self.wallet = wallet

		if keypair == None:
			self.keypair = rsa.newkeys(1024)
		else:
			self.keypair = keypair


	def requestCerti(self, )