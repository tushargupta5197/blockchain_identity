# this file will import all the class files and global variable files called settings.py and will
# handle the entire logic of connecting all individual components together
from User import User
# globalVs.init()

alice = User(name='Alice Garcia', wallet_file='wallet.yaml')

values={
	'first_name' : 'Alice',
	'last_name': 'Garcia',
	'ssn' : 150035, 
	'degree': 'Btech',
	'year' : 2015,
	'status' : 'graduated' 
}

alice.requestCertificate(issuer = 'ABC University', values=values)

values={
	'first_name' : 'Alice',
	'last_name': 'Garcia',
	'phone_number': 1,
	'ssn' : 150035, 
	'degree': 'Btech',
	'status' : 'graduated' 
}

alice.requestCertificate(issuer = 'XYZ Company', values=values)

values = {
	'first_name' : 'Alice',
	'last_name': 'Garcia',
	'phone_number': 1,
	'ssn' : 150035, 
	'salary' : 1
}

alice.requestCertificate(issuer = 'SBI Bank', values=values)