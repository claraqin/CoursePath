"""
Converts a table of course offerings and their terms (like Courses_terms.txt) into a JSON
file representing the same information.

Script:

	cat [input_txt] | python course_terms_txt2json.py [output_json]

"""

import sys
import json

if len(sys.argv) > 1:
	output_filename = sys.argv[1]
else:
	quit('Error: Must specify output filename as arg1')

terms_dict = {}

for line in sys.stdin:
	linestrip = line.strip()
	linesplit = linestrip.split('\t')
	course_id = linesplit[0]
	course_term = linesplit[2]

	if course_id in terms_dict:
		terms_dict[course_id].append(course_term)
	else:
		terms_dict[course_id] = [course_term]

with open(output_filename, 'w') as f:
	json.dump(terms_dict, f)
