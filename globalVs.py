from ruamel.yaml import YAML

def init():

	global yaml
	yaml = YAML()

	global issuers
	issuers = ['SBI Bank', 'ABC University', 'XYZ Company']

	global users
	users = ['alice']

	global CertiName
	CertiName = {
		'ABC University' : 'transcript',
		'XYZ Company' : 'job_application',
		'SBI Bank' : 'loan',
	}

	global merkle_signatures
	merkle_signatures = []

	global public_keys
	public_keys = {}


def save():
	pass
