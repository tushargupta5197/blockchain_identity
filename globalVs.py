def init():
	global issuers
	issuers = ['SBI bank', 'ABC University', 'XYZ Company']

	global users
	users = ['alice']

	global CertiName
	CertiName = {
		'ABC University' : 'transcript',
		'XYZ Company' : 'job_application',
		'SBI bank' : 'loan',
	}

	global merkle_signatures
	merkle_signatures = []

	global public_keys
	public_keys = {}


def save():
	pass
