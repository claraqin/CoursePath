# Gets the 'time' of the prerequisite chain associated with the course given as argv[1].
# Here, 'time' simply refers to the number of quarters to fulfill the courses in the
# prereq chain, starting from Fall 2011. 

import sys
import json

verbose = False

# Load dictionaries:
with open('../dict/course_name2id_dict.json', 'r') as f:
	course_name2id = json.load(f)

with open('../dict/course_id2name_dict.json', 'r') as f:
	course_id2name = json.load(f)

with open('../dict/req_dict_nested.json', 'r') as f:
	req_dict = json.load(f)

# Get course name of interest from sys.argv
if len(sys.argv) > 1:
	coursename = sys.argv[1]
	courseid = course_name2id[coursename]
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
def len_chain(courseid, n=0):
	try:
		prereqs = req_dict[courseid][0] # '0' specifies prereqs; 
		coreqs = req_dict[courseid][1]  # '1' specifies coreqs

		if verbose:
			print('\t' * n + str(n))
			print('\t' * n + 'Course: ' + course_id2name[courseid] + '\tPrereqs: ' + str(nested_replace(prereqs)))
			print('\t' * n + 'Course: ' + course_id2name[courseid] + '\tCoreqs: ' + str(nested_replace(coreqs)))

		return max([len_chain2(prereqs, n), len_chain2(coreqs,n) - 1, 0])

	except RecursionError:
		quit('RecursionError: Maximum recursion depth reached, probably due to circular reference')

	except KeyError:
		quit('KeyError: ' + courseid + 'does not appear in prerequisite dictionary')

def len_chain2(branch, n):
	# Passed value (branch) should be a dict containing only one item
	if isinstance(branch, dict):
		# print("Branch: " + str(branch))

		# Check which key the dict contains:
		# 'And' grouping --> return max chain-length of the sub-branches
		# 'Or' grouping --> return min chain-length of the sub-branches
		# 'Takes' --> return chain-length of the course ID, using len_chain()
		if 'And' in branch and branch['And']:
			if len(branch['And']) > 0:
				len_list = [len_chain2(v, n) for v in branch['And']]
				return max(len_list)
			else:
				return n

		elif 'Or' in branch and branch['Or']:
			if len(branch['Or']) > 0:
				len_list = [len_chain2(v, n) for v in branch['Or']]
				return min(len_list)
			else:
				return n

		elif 'Takes' in branch and branch['Takes']:
			len_single = len_chain(branch['Takes'], n+1)
			return len_single

		else:
			return n

	else:
		quit("Error: Input to len_chain2() was not a dict")


print(len_chain(courseid))
