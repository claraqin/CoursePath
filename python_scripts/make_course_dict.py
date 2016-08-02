# Makes course ID dictionary from ExploreCourses data

import json
import sys

course_dict = {}

for line in sys.stdin:
	parts = line.split('\t')
	courseid = parts[1]
	coursename = parts[2] + ' ' + parts[3]

	course_dict[courseid] = coursename

with open('course_dict.json', 'w') as f:
	json.dump(course_dict, f)