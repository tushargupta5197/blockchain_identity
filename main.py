# this file will import all the class files and global variable files called settings.py and will
# handle the entire logic of connecting all individual components together

import globalVs
from Issuer import Issuer
import Certificate
from User import User


globalVs.init()

alice = User(name='alice', wallet_file='wallet.yaml')

abc_univ = Issuer(name='ABC University', schema='schemas/'+globalVs.CertiName['ABC University'] + '.yaml')


xyz_company = Issuer(name='XYZ Company', schema='schemas/'+globalVs.CertiName['XYZ Company'] + '.yaml')


bank = Issuer(name='SBI bank', schema='schemas/'+globalVs.CertiName['SBI bank'] + '.yaml')


values={
	'first_name' : 'alice',
	'last_name': 'garcia',
	'ssn' : 150035, 
	'degree': 'Btech',
	'year' : 2015,
	'status' : 'graduated' 
}

alice.requestCertificate(issuer = 'ABC University', values=values ,issuer_obj = abc_univ)

values={
	'first_name' : 'alice',
	'last_name': 'garcia',
	'phone_number': 0612,
	'ssn' : 150035, 
	'degree': 'Btech',
	'status' : 'graduated' 
}

alice.requestCertificate(issuer = 'XYZ Company', values=values, issuer_obj=xyz_company)