"""
Gets the 'length' of the prerequisite chain associated with the course given as argv[1].
Currently, 'length' simply refers to the number of courses in the prereq chain
(preceding the root course).

Script:
	
	python len_prereq_chain.py [course_name] [verbose]

"""

KEY_ERROR_OUTPUT = 9999

import sys
import json

verbose = False
key_errors = []

# Load dictionaries:
with open('../dict/course_name2id_dict.json', 'r') as f:
	course_name2id = json.load(f)

with open('../dict/course_id2name_dict.json', 'r') as f:
	course_id2name = json.load(f)

with open('../dict/req_dict_nested.json', 'r') as f:
	req_dict = json.load(f)


if len(sys.argv) > 1:
	with open(sys.argv[1], 'r') as f:
		input_json = json.load(f)
	if len(sys.argv) > 2:
		verbose = True
else:
	quit('Error: Must specify course name of interest as arg')

def nested_replace(input_d):
	copy_d = input_d.copy()
	for k, v in iter(copy_d.items()):
		if isinstance(v, list):
			copy_d[k] = [nested_replace(clause) for clause in v]
		else:
			copy_d[k] = course_id2name[v]
	return copy_d

# Recursive function to keep counting courses in prereq chain:
# Takes a str representing a course ID, returns an integer
def len_chain(courseid, n=0, tabs=0, ignore_coreqs=False):
	try:
		prereqs = req_dict[courseid][0] # '0' specifies prereqs; 

		# If you did NOT come from coreq branch
		if not ignore_coreqs:
			coreqs = req_dict[courseid][1]  # '1' specifies coreqs

			ignore_next_coreqs = len(coreqs) > 0

			if verbose:
				print('\t' * tabs + 'Course: ' + course_id2name[courseid])
				print('\t' * tabs + 'Prereqs: ' + str(nested_replace(prereqs)))
				print('\t' * tabs + 'Coreqs: ' + str(nested_replace(coreqs)))
				print('\t' * tabs + 'n: ' + str(n))
				print('')

			return max([len_chain2(prereqs, n, tabs, ignore_next_coreqs), 
				len_chain2(coreqs, n, tabs, ignore_next_coreqs) - 1, 0])

		# If you came from coreq branch
		if ignore_coreqs:
			if verbose:
				print('\t' * tabs + 'Course: ' + course_id2name[courseid])
				print('\t' * tabs + 'Prereqs: ' + str(nested_replace(prereqs)))
				print('\t' * tabs + 'n: ' + str(n))
				print('')
				
			return max([len_chain2(prereqs, n, tabs), 0])

	except RuntimeError:
		quit('RuntimeError: Maximum recursion depth reached, probably due to circular reference')

	except KeyError:
		key_errors.append(courseid)
		return(KEY_ERROR_OUTPUT)
		# quit('KeyError: ' + courseid + ' does not appear in prerequisite dictionary')

def len_chain2(branch, n=0, tabs=0, ignore_next_coreqs=False):
	# Passed value (branch) should be a dict containing only one item
	if isinstance(branch, dict):
		# print("Branch: " + str(branch))

		# Check which key the dict contains:
		# 'And' grouping --> return max chain-length of the sub-branches
		# 'Or' grouping --> return min chain-length of the sub-branches
		# 'Takes' --> return chain-length of the course ID, using len_chain()
		if 'And' in branch and branch['And']:
			if verbose:
				print('\t' * tabs + 'AND')
			if len(branch['And']) > 0:
				len_list = [len_chain2(v, n, tabs+1, ignore_next_coreqs) for v in branch['And']]
				return max(len_list)
			else:
				return n

		elif 'Or' in branch and branch['Or']:
			if verbose:
				print('\t' * tabs + 'OR')
			if len(branch['Or']) > 0:
				len_list = [len_chain2(v, n, tabs+1, ignore_next_coreqs) for v in branch['Or']]
				return min(len_list)
			else:
				return n

		elif 'Takes' in branch and branch['Takes']:
			len_single = len_chain(branch['Takes'], n+1, tabs+1, ignore_next_coreqs)
			return len_single

		else:
			return n

	else:
		quit("Error: Input to len_chain2() was not a dict")


print(len_chain2(input_json))

if verbose and len(key_errors) > 0:
	print('Warning: the following courses did not appear in the prerequisite dictionary, perhaps because they were never offered:')
	print(', '.join(key_errors))
	print('Also if you received ' + KEY_ERROR_OUTPUT + ' as output, this may be because at least one of these courses was somehow a hard requirement.')
