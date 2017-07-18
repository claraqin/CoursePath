# Makes pre-requisite/co-requisite dictionary from Ken's edit of Edusalsa's prereq JSON
# Updated so that keys are course IDs, not course names
# Relies on comprehensiveness of output from make_course_dicts.py

import json
import sys

isMissingReference = False

with open('../dict/course_name2id_dict.json', 'r') as f:
	course_name2id = json.load(f)

# def nested_replace(d):
# 	for k, v in iter(d.items()):
# 		if isinstance(v, list):
# 			d[k] = [nested_replace(clause) for clause in v]
# 		else:
# 			d[k] = course_name2id[v]
# 	return d

def nested_replace(input_d):
	copy_d = input_d.copy()
	for k, v in iter(copy_d.items()):
		if isinstance(v, list):
			copy_d[k] = [nested_replace(clause) for clause in v]
		else:
			copy_d[k] = course_name2id[v]
	return copy_d

req_dict = {}

# Piping in from prereqs.json
for line in sys.stdin:
	entry = json.loads(line)
	# if entry['code'] == 'ECON 52' or entry['code'] == 'ECON 78N':
	# 	verbose = True
	# else:
	# 	verbose = False

	try:
		key = course_name2id[entry['code']]
	except KeyError:
		print('Warning: ' + entry['code'] + ' was not offered between Fall 2011 and Spring 2016')
		isMissingReference = True
		continue

	try:
		prereqs = nested_replace(entry['prereq'])
		coreqs = nested_replace(entry['coreq'])
		# prereqs = [course_name2id[prereq] for prereq in entry['prereq']]
		# coreqs = [course_name2id[coreq] for coreq in entry['coreq']]

		req_dict[key] = [prereqs, coreqs]

		# if verbose:
		# 	print(key)
		# 	print(req_dict[key])

	except KeyError:
		# print('Warning: At least one pre- or co-requisite for ' + entry['code'] + ' was not offered between Fall 2011 and Spring 2016')
		isMissingReference = True

if isMissingReference:
	print('Note: Usually the name-to-ID dict will only fail to make a reference to a course if the course or at least one of its pre-/co-requisites was not offered between Fall 2011 and Spring 2016')

with open('../dict/req_dict_nested.json', 'w') as f:
	json.dump(req_dict, f)