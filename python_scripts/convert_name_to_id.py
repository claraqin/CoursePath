# Converts the representation of courses from names to ID by using course_name2id_dict.json

import sys
import json
import re

with open('../dict/course_name2id_dict.json','r') as f:
	course_dict = json.load(f)

pattern = re.compile('|'.join(course_dict.keys()))

for line in sys.stdin:
	print(pattern.sub(lambda x: course_dict[x.group()], line.rstrip('\n')))