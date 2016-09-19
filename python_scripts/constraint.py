# User-created "constraint" module to represent degree requirements.
# Implemented via classes representing different types of requirements:
# - 'Takes': base class; satisfied if a certain course has been taken
# - 'And': extension of 'Takes'; satisfied if ALL of its components have been taken
# - 'Or': extension of 'Takes'; satisfied if ANY of its components have been taken

import json

class Takes(object):

	def __init__(self, course): # course is formatted as string
		self.type = 'simple'
		self.constraints = course
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


# # Wrapper function for make_constraint.
# # Takes a JSON file representing a set of degree requirements (or course 
# # prerequisites) and returns a Constraint class object that represents those requirements
# def make_constraint_from_JSON(file):
# 	reqs = json.load(file)
# 	return(make_constraint(reqs))

# Recursive function to return a (possibly nested) Constraint class object based
# on a (possibly nested) dict or branch thereof.
def make_constraint(branch):
	for key in branch.keys(): # There should only be one key per dictionary/branch
		val = branch[key]

		# Base case: if key is 'Takes', then just return 'Takes' constraint object
		if key == 'Takes':
			return(Takes(val))

		# Otherwise, recurse!
		else:

			# Get list of constraint objects from recursion upon this branch
			constraint_list = []
			for d in val:
				constraint_list.append(make_constraint(d))

			# Then determine what type of constraint, and return
			if key == 'And':
				return(And(*constraint_list))
			elif key == 'Or':
				return(Or(*constraint_list))
			else:
				quit("Error: Unexpected key not in ('Takes','And','Or')")

