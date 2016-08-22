# Makes pre-requisite/co-requisite dictionary from Edusalsa's prereq JSON
# Updated so that keys are course IDs, not course names
# Relies on comprehensiveness of output from make_course_dicts.py

import json
import sys

with open('../dict/course_name2id_dict.json', 'r') as f:
	course_name2id = json.load(f)

req_dict = {}

for line in sys.stdin:
	entry = json.loads(line)

	try:
		key = course_name2id[entry['code']]
		prereqs = entry['prereq']
		coreqs = entry['coreq']

		req_dict[key] = [prereqs, coreqs]

	except KeyError:
		print('Warning: Course name-to-ID dict was not made with reference to ' + entry['code'])
		pass

with open('../dict/req_dict.json', 'w') as f:
	json.dump(req_dict, f)