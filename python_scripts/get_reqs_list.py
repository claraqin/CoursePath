# Takes a manually-typed .txt denoting degree requirements (like reqs_geophysics0.txt) and 
# returns the subset of courses in output_courses_w_times.txt that would be relevant. 
# The output of this script can be used in print_pathways.py.

import sys
import re
import json

# Name of all-courses file
filename = '../ec_data/output_courses_w_times.txt'

# First generate list of relevant courses from stdin:
relevant_courses = []
pattern_course = r'\t*([A-Z]+\s\d+[A-Z]?)'

for line in sys.stdin:
	m_course = re.match(pattern_course, line)

	if m_course is not None:
		relevant_courses.append(m_course.group(1))

# Next look up course IDs in dictionary 
with open('../dict/course_name2id_dict.json','r') as f:
	course_name2id = json.load(f)

relevant_course_ids = []
for course in relevant_courses:
	try:
		relevant_course_ids.append(course_name2id[course])
	except KeyError:
		pass

relevant_course_ids = set(relevant_course_ids)

# Now open the file of all courses we could reasonable consider
with open(filename, 'r') as f:
	allcourses = f.readlines()

for candidate in allcourses:
	candidate_course = candidate.strip()
	candidate_id = candidate_course.split('\t')[1]
	if candidate_id in relevant_course_ids:
		print(candidate_course)


