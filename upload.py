from web3 import Web3
import json

class Maker :
	def __init__(self, maker_addr):
		self.infura_url = 'https://ropsten.infura.io/v3/5466c106de5f40678f6b1b3b075bb7d0'
		self.web3 = Web3(Web3.HTTPProvider(self.infura_url))


		self.maker_abi = json.loads(open('maker.abi','r').read())
		self.certi_abi = json.loads(open('Certificate.abi','r').read())

		self.publicKey = '0xa9CaB16aC067306130A7f907fDc7CA51380525df'
		self.privateKey = '0x699a2dac916510b98a79b05a2c4cfae785578caaeadd1b13f41ff6b91eb1ef60'


		self.add = self.web3.toChecksumAddress(maker_addr)

		self.makerContract = self.web3.eth.contract(address= self.add, abi = self.maker_abi)


	def issueCertificate(self, merkelHash):
		txn = self.makerContract.functions.issueCertificate(merkelHash).buildTransaction()
		tx_count = self.web3.eth.getTransactionCount(self.publicKey)
		txn['nonce'] = hex(tx_count)
		# print(txn)
		signed = self.web3.eth.account.signTransaction(txn, self.privateKey)

		txn_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)

		txn_object = self.web3.eth.getTransaction(txn_hash)

		print("Transaction submitted. waiting for confirmation...")


		while(txn_object['blockNumber'] == None):
			txn_object = self.web3.eth.getTransaction(txn_hash)
			
		certificate_address = self.makerContract.functions.getRecentCertificate().call()


		return certificate_address

	def getHash(self, certificate_address):
		certificate_address = str(certificate_address)
		t_certificate_address = self.web3.toChecksumAddress(certificate_address)
		certi_contract = self.web3.eth.contract(address = t_certificate_address, abi = self.certi_abi)
		return certi_contract.functions.getHash().call()


'''
if __name__ == '__main__':
	maker = Maker('0x9e7cd1df366a5d315e0f42d3d3e3100943281cb0')

	# Input String to create Certificate
	# str_input = input("Please enter Merkel Root:")
	str_input = 'Hello!'
	add = maker.issueCertificate(str_input)
	print("New Certificate issued.\nCertificate Address:", add)


	# Print string from the certificate just created
	str_out = maker.getHash(add)
	print(str_input)
	print(str_out == str_input)
	# print("Your daily fortune result is:", string)

'''