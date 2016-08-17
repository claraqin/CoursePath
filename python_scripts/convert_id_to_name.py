# Converts the representation of courses from ID numbers to names by using course_dict.json

import sys
import json
import re

with open('course_dict.json','r') as f:
	course_dict = json.load(f)

pattern = re.compile('|'.join(course_dict.keys()))

for line in sys.stdin:
	print(pattern.sub(lambda x: course_dict[x.group()], line.rstrip('\n')))