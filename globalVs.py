def init():
	global issuers
	issuers = ['Passport_Office', 'ABC University', 'XYZ Company']

	global users
	users = ['tg', 'kumar', 'mkant', 'baba', 'khetan']

	global CertiName
	CertiName = {
		'Passport_Office' : 'passport',
		'ABC University' : 'transcript',
		'XYZ Company' : 'job_certificate',
	}

	global merkle_signatures
	merkle_signatures = []

	global public_keys
	public_keys = {}
