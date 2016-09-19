# Makes pre-requisite/co-requisite dictionary from Edusalsa's prereq JSON
# Updated so that keys are course IDs, not course names
# Relies on comprehensiveness of output from make_course_dicts.py

import json
import sys

isMissingReference = False

with open('../dict/course_name2id_dict.json', 'r') as f:
	course_name2id = json.load(f)

req_dict = {}

for line in sys.stdin:
	entry = json.loads(line)

	try:
		key = course_name2id[entry['code']]
		prereqs = [course_name2id[prereq] for prereq in entry['prereq']]
		coreqs = [course_name2id[coreq] for coreq in entry['coreq']]

		req_dict[key] = [prereqs, coreqs]

	except KeyError:
		print('Warning: Course name-to-ID dict was not made with reference to ' + entry['code'])
		isMissingReference = True

if isMissingReference:
	print('Note: Usually the name-to-ID dict will only fail to make a reference to a course if it was not offered between 2011 and 2016')
	print('Edit: Or if your input prereqs.json represents its requirements as nested dicts (i.e. to account for "and"/"or" structure)')

with open('../dict/req_dict.json', 'w') as f:
	json.dump(req_dict, f)