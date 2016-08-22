# Takes a manually-typed .txt denoting degree requirements (like reqs_geophysics0.txt) and 
# reformats it as a json file

import sys
import re

pattern_conjunction = r'\t*([A-Z][a-z]+)\['
pattern_course = r'\t*([A-Z]+\s\d+[A-Z]?)'
pattern_endbracket = r'\t*(\])'

n = 0
prev_line = ''
was_conjunction = False
within_takes = False

for line in sys.stdin:

	# Print previous iteration's line
	print(prev_line, end='')

	# Append a comma to prev. line only if new line is not an end-bracket and prev. line was not a conjunction
	is_endbracket = (line.strip() == ']')
	if n>0 and not is_endbracket and not was_conjunction:
		print(',')
	else:
		print()

	# Reset momentary bool
	was_conjunction = False

	# Attempt to match all patterns
	m_conjunction = re.match(pattern_conjunction, line)
	m_course = re.match(pattern_course, line)
	m_endbracket = re.match(pattern_endbracket, line)

	# Make substitutions where possible
	if m_conjunction is not None:
		prev_line = re.sub(m_conjunction.group(1), '{ \"' + m_conjunction.group(1) + '\": ', line.rstrip())
		was_conjunction = True

	elif m_course is not None:
		prev_line = re.sub(m_course.group(1), '{ "Takes": "' + m_course.group(1) + '\"', line.rstrip()) + '}'

	elif m_endbracket is not None:
		prev_line = re.sub(m_endbracket.group(1), m_endbracket.group(1) + '}', line.rstrip())

	else:
		quit('ERROR: Line does not match any regex')

	n = n+1

print(prev_line)

