from ruamel.yaml import YAML
yaml = YAML()

globalVs = {}

url = {'SBI Bank':'http://localhost:8082/', 'ABC University':'http://localhost:8080/', 'XYZ Company':'http://localhost:8081/'}


CertiName = {
	'ABC University' : 'transcript',
	'XYZ Company' : 'job_application',
	'SBI Bank' : 'loan',
}

merkle_signatures = []

globalVs['url'] = url
globalVs['CertiName'] = CertiName
globalVs['merkle_signatures'] = merkle_signatures

# pkl.dump(globalVs, open('globalVs', 'w'))

with open('globalVs.yaml', 'w') as outfile:
    yaml.dump(globalVs, outfile)

