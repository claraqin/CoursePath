#### THE BUG: I had each recursion be a while-loop that goes until it reaches the end of
# the file. Instead, I should have it end when it hits the next end-bracket.

import re
import sys

try:
	filename = sys.argv[1]
except:
	quit("ERROR: Must specify filename as Python argument")

# Takes in the manually-typed .txt file representing a degree's requirements
with open(filename, 'r') as f:
	req_lines = [line.strip() for line in f.readlines()]

# Recursive function for looping through the req_lines:
# - curr_n is the current index in the file that we're reading
# - curr_structure is the current nested-AND-OR structure
# - curr_list is current list representing one way to fulfill requirements, which
#   will be converted to a set
# Implemented using 'while' instead of 'for' to allow for skipping multiple lines,
# which is useful for navigating the 'OR{}' sections
def printSets(curr_n, curr_structure, curr_list, recursion_lvl):

	while len(curr_structure) > 0:

		print()
		print("Recursion lvl:" + str(recursion_lvl) + '\t' + "Loop index:" + str(curr_n))
		print("Curr_list: " + ','.join(curr_list))
		print("Curr_structure: " + ','.join(curr_structure))

		line = req_lines[curr_n]

		# By default, next line is assumed to be at index+1, but this may change
		next_n = curr_n + 1

		# If next section will be AND, then update structure accordingly
		if line == 'AND{':
			curr_structure.append('AND')

		# If next section will be OR, then update structure accordingly 
		# (and prepare for recursion)
		elif line == 'OR{':
			curr_structure.append('OR')

		elif line is None:
			continue

		# Otherwise, assume the line is a course name
		else:

			# If currently within an 'OR' section, recurse on next element within section
			# until reaching the end-bracket
			if len(curr_structure) > 0 and curr_structure[-1] == 'OR':
				
				# If the current line is not an end-bracket, recurse on next element using
				# the last curr_structure element, and then append a course to this list
				if line != '}':
					next_n = printSets(curr_n + 1, [curr_structure[-1]], curr_list, recursion_lvl+1)
					curr_list.append(line)

				# Else the current line is in fact an end-bracket, so eventually return 
				# the curr_n but not before completing this recursion
				else:
					curr_structure.pop()
					return_n = curr_n

			# If not 'OR', then 'AND' section:
			elif len(curr_structure) > 0 and curr_structure[-1] == 'AND':

				# If the current line is not an end-bracket, append to course list
				if line != '}':
					curr_list.append(line)

				# Else the current line is an end-bracket, so continue after
				# updating structure
				else:
					curr_structure.pop()

		curr_n = next_n

	# At the end of the recursion, print curr_list, and return return_n to let mother
	# recursion know what line to skip to
	print("Return n:" + str(return_n))
	return return_n

start_structure = [req_lines[0][:-1]] # Assume that the first line gives you the starting structure
printSets(curr_n = 1, curr_structure = start_structure, curr_list = [], recursion_lvl = 1)
