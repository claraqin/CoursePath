"""
Takes a manually-typed .txt denoting degree requirements (like reqs_geophysics0.txt) and 
reformats it as a JSON file.
In JSON file, required courses will be represented by course ID, not by name.

Script:
	
	python format_reqs_json.py [-h] [reqs_txt] [reqs_json]

"""

import sys
import re
import json
import argparse

# Import course name-to-ID dict:
with open('../dict/course_name2id_dict.json','r') as f:
	course_dict = json.load(f)

# Regex patterns
pattern_conjunction = r'\t*([A-Z][a-z]+)\['
pattern_course = r'\t*([A-Z]+\s\d+[A-Z]?[A-Z]?)'
pattern_endbracket = r'\t*(\])'

def write_as_json(input_txt):
	"""
	Input: list of strings from manually-typed degree requirements

	Output: JSON object representing degree requirements
	"""
	n = 0
	prev_line = ''
	was_conjunction = False
	within_takes = False

	output_str = ""

	for line in input_txt:

		# Print previous iteration's line
		output_str += prev_line

		# Append a comma to prev. line only if new line is not an end-bracket and prev. line was not a conjunction
		is_endbracket = (line.strip() == ']')
		if n>0 and not is_endbracket and not was_conjunction:
			output_str += ','
		else:
			output_str += '\n'

		# Reset momentary bool
		was_conjunction = False

		# Attempt to match all patterns
		m_conjunction = re.match(pattern_conjunction, line)
		m_course = re.match(pattern_course, line)
		m_endbracket = re.match(pattern_endbracket, line)

		# Make substitutions where possible
		if m_conjunction is not None:
			conjunction = m_conjunction.group(1)
			prev_line = re.sub(conjunction, '{ \"' + conjunction + '\": ', line.rstrip())
			was_conjunction = True

		elif m_course is not None:
			course = m_course.group(1)
			try:
				courseid = course_dict[course]
				prev_line = re.sub(course, '{ "Takes": "' + courseid + '\"', line.rstrip()) + '}'
			except KeyError:
				print("Warning: " + course + " not found in course name-to-ID dictionary;", end=" ")
				print("therefore, effectively removed from degree requirement check.")
				prev_line = re.sub(course, '{ "Takes": "' + course + '\"', line.rstrip()) + '}'

		elif m_endbracket is not None:
			endbracket = m_endbracket.group(1)
			prev_line = re.sub(endbracket, endbracket + '}', line.rstrip())

		else:
			quit('ERROR: Line does not match any regex')

		n = n+1

	output_str += prev_line
	return(json.loads(output_str))

if __name__ in '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('reqs_txt', nargs='?', type=argparse.FileType('r'), default='-',
		help = 'Input: degree requirements data in nested "And"/"Or" format - manually created')
	parser.add_argument('reqs_json', nargs='?', type=argparse.FileType('w'), default='-',
		help = 'Output: file path to JSON-formatted degree reqs')
	args = parser.parse_args()

	input_txt = []
	for line in args.reqs_txt:
		input_txt.append(line)

	parsed_json = write_as_json(input_txt)
	args.reqs_json.write(json.dumps(parsed_json, indent=4))

