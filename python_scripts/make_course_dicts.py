# Makes course ID dictionary from ExploreCourses data
# This is an ID-to-name dictionary

import json
import sys

course_id2name = {}
course_name2id = {}

for line in sys.stdin:
	parts = line.split('\t')
	courseid = parts[1]
	coursename = parts[2] + ' ' + parts[3]

	course_id2name[courseid] = coursename
	course_name2id[coursename] = courseid

with open('../dict/course_id2name_dict.json', 'w') as f:
	json.dump(course_id2name, f)

with open('../dict/course_name2id_dict.json', 'w') as f:
	json.dump(course_name2id, f)