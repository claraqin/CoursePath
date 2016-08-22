# User-created "constraint" module to represent degree requirements.
# Implemented via classes representing different types of requirements:
# - 'Takes': base class; satisfied if a certain course has been taken
# - 'And': extension of 'Takes'; satisfied if ALL of its components have been taken
# - 'Or': extension of 'Takes'; satisfied if ANY of its components have been taken

class Takes(object):

	def __init__(self, course): # course is formatted as string
		self.type = 'simple'
		self.course = course

	def is_satisfied(self, sched):
		return(self.course in sched)


class And(object):

	def __init__(self, *constraints):
		self.type = 'and'
		self.constraints = constraints

	def is_satisfied(self, sched):
		return(all(constraint.is_satisfied(sched) for constraint in self.constraints))


class Or(object):

	def __init__(self, *constraints):
		self.type = 'or'
		self.constraints = constraints

	def is_satisfied(self, sched):
		return(any(constraint.is_satisfied(sched) for constraint in self.constraints))

# Input is the JSON output of format_reqs_json.py, which is used upon a file denoting
# the degree requirements.
# Output is a Constraint-class object.
def parse_course_reqs(lines):
	for line in lines:
		entry = line.strip()
		reqs_this_level = []

		# If the entry is not denoting a start- or end-bracket
		if entry not in ['AND{','OR{','}']:
			reqs_this_level.append(entry)

		elif entry == 'AND{':
			reqs_this_level = 

		elif entry == 'OR{':

		else entry == '}':
			return((Takes(x)) for x in courses_this_level)

	# If somehow the loop ends before the function can return anything,
	# then there were too few end-brackets
	quit('More start-brackets than end-brackets in file denoting degree requirements')




# Test those classes
# math = 'Math'
# physics = 'Physics'
# french = 'French'

# math_reqs = And(Takes(math), Takes(physics))
# complex_reqs = And(Takes(math), Or(Takes(physics), Takes(french)) )

# sched1 = [math, physics] # should satisfy both sets of reqs
# sched2 = [math, french] # should satisfy complex_reqs, but not math_reqs
# sched3 = [french, physics] # should satisfy neither

# print(math_reqs.is_satisfied(sched1))
# print(complex_reqs.is_satisfied(sched1))

# print(math_reqs.is_satisfied(sched2))
# print(complex_reqs.is_satisfied(sched2))

# print(math_reqs.is_satisfied(sched3))
# print(complex_reqs.is_satisfied(sched3))



