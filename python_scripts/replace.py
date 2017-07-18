import sys
import json
import re


filename_courseid2name = '../dict/course_id2name_dict.json'

with open(filename_courseid2name, 'r') as f:
	course_id2name = json.load(f)

for line in sys.stdin:
	replaced = False
	for k,v in iter(course_id2name.items()):
		if k == line.strip():
			print(line.rstrip().replace(k, v))
			replaced = True
	if not replaced:
		print(line.rstrip())