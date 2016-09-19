"""
Takes a manually-typed .txt denoting degree requirements (like reqs_geophysics0.txt) and 
returns the subset of courses in output_courses_w_times.txt that would be relevant. 
The output of this script can be used in print_pathways.py.

Note: CURRENTLY DOES NOT CONSIDER COREQUISITES.

Script:

  python get_relevant_courses.py [-h] [degree_reqs] [output]

"""

import sys
import re
import json
import argparse

# Hard-coded filenames:
# (1) all-courses
# (2) prereq dict
# (3) course name-to-ID dict
filename_allcourses = '../ec_data/output_courses_w_times.txt'
filename_prereqs = '../dict/req_dict_nested.json'
filename_coursename2id = '../dict/course_name2id_dict.json'

with open(filename_allcourses, 'r') as f:
	allcourses = f.readlines()
with open(filename_prereqs, 'r') as f:
	prereq_dict = json.load(f)
with open(filename_coursename2id, 'r') as f:
	course_name2id = json.load(f)

# Takes a course ID, returns a list
def get_all_prereqs1(courseid):
	try:
		prereqs = prereq_dict[str(courseid)][0]
		return get_all_prereqs2(prereqs)
	except KeyError:
		return []

# Takes a dict, returns a list
def get_all_prereqs2(branch):
	course_list = []
	for k, v in iter(branch.items()):
		if isinstance(v, list):
			local_result = [get_all_prereqs2(next) for next in v] # list of lists
			course_list.extend([item for sublist in local_result for item in sublist])
		else:
			course_list.append(v)
			course_list.extend(get_all_prereqs1(v))
	return course_list


if __name__ in '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('degree_reqs', nargs='?', type=argparse.FileType('r'), default='-',
		help = 'Input: degree requirements data in nested "And"/"Or" format - probably manually created')
	parser.add_argument('output', nargs='?', type=argparse.FileType('w'), default='-',
		help = 'Output: set of relevant course IDs to consider in print_pathways')
	args = parser.parse_args()

	# Generate list of relevant courses from args.degree_reqs:
	relevant_courses = []
	pattern_course = r'\t*([A-Z]+\s\d+[A-Z]*)'

	for line in args.degree_reqs:
		m_course = re.match(pattern_course, line)

		if m_course is not None:
			relevant_courses.append(m_course.group(1))

	# Next look up course IDs in name-to-ID dictionary 
	relevant_course_ids = []
	for course in relevant_courses:
		try:
			relevant_course_ids.append(course_name2id[course])
		except KeyError:
			pass

	relevant_course_ids = set(relevant_course_ids)

	# Also include all prereqs of each relevant course ID
	prereq_course_ids = []
	for i in relevant_course_ids:
		prereq_course_ids.extend(get_all_prereqs1(i))

	relevant_course_ids = relevant_course_ids | set(prereq_course_ids)

	# Write output:
	output = []
	for candidate in allcourses:
		candidate_course = candidate.strip()
		candidate_id = candidate_course.split('\t')[1]
		if candidate_id in relevant_course_ids:
			output.append(candidate_course)

	for line in output:
		args.output.write(line + '\n')

