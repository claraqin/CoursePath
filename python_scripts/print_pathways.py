# Recursively prints all pathways possible in 2011-2016 given a set of relevant courses.
# An extension of get_qtr_schedules.py

########## Currently starts in 2011 and goes for 12 quarters

########## Currently 'offset' has been replaced by 1, 
########## i.e. students cannot take "empty" quarters

########## Currently skips any 'DIS' sections

########## Does not yet check co-requisites

########## Currently skips any course repeats, even potentially repeatable ones

########## Currently only outputs are [current qtr, max qtr, path]

########## Currently only using a course name-to-ID dictionary

########## Currently uses max_courses_per_qtr = 6

from datetime import datetime
import re
import sys
import json
import networkx as nx
import constraint as c
from itertools import chain, combinations

# Student can take no more than this number of courses in a quarter
max_courses_per_qtr = 6

# Load dictionaries:
with open('../dict/course_name2id_dict.json', 'r') as f:
	course_name2id = json.load(f)

with open('../dict/req_dict.json','r') as f:
	req_dict = json.load(f)

# Read input (relevant courses only) for processing via recursive searchPath function
# Arrange courses by term (using dict structure) so each iteration does not have to search through the 
# entire allcourses
allcourses_by_term = {}
for line in sys.stdin:
	term_id = line.split('\t')[9]
	if term_id in allcourses_by_term:
		allcourses_by_term[term_id].append(line)
	else:
		allcourses_by_term[term_id] = [line]

# Create Constraint object to represent degree requirements, based on filename (sys.argv[1])
printDegreeCompletion = False
if len(sys.argv) > 1:
	degree_reqs = c.make_constraint(sys.argv[1])
	printDegreeCompletion = True

# Delimiters to represent pathways 
# delim1 separates quarters, delim2 separates course-class IDs within the same quarter
delim1 = '|'
delim2 = ','

path_split_pattern = r"[^|\t]+"

weekday_replacements = [
	['Monday', '1 '],
	['Tuesday', '2 '],
	['Wednesday', '3 '],
	['Thursday', '4 '],
	['Friday', '5 '],
	['Saturday', '6 '],
	['Sunday', '0 ']
]

# Write weekly schedule as a list of tuples. Each tuple is start_time, end_time:
def writeSchedule(days, start_time, end_time):
	for w_str, w_n in weekday_replacements:
		days = days.replace(w_str, w_n)
	schedule = []
	for day in days.split('|'):
		schedule.append((day + start_time, day + end_time))
	return schedule

def checkConflicting(schedule1, schedule2): # Weekly schedule is a list of tuples
	for block1 in schedule1:
		start1 = datetime.strptime(block1[0], "%w %H:%M:%S %p")
		end1 = datetime.strptime(block1[1], "%w %H:%M:%S %p")
		for block2 in schedule2:
			start2 = datetime.strptime(block2[0], "%w %H:%M:%S %p")
			end2 = datetime.strptime(block2[1], "%w %H:%M:%S %p")

			# If the later start time is before the earlier end time, return True
			later_start = max(start1, start2)
			earlier_end = min(end1, end2)
			if later_start < earlier_end:
				return True

	# If all for-loops completed and still no conflicting blocks,
	return False

def searchPath(startyear, t, T, branch_id, Path):
	step = Path.split('|')[-1] # The step (quarter schedule) that was taken to get here

	# Print the current Path:
	print("t:" + str(t) + "\tT:" + str(T) + "\tbranch_id:" + branch_id + "\tstep:" + step + "\tpathway:" + Path, end='\t')

	# If this is the final quarter, end this recursion branch (AFTER checking degree completion)
	if t == T:
		if printDegreeCompletion:
			prev_cc_id = re.findall(path_split_pattern, Path)
			prev_courses = [i.split('-')[0] for i in prev_cc_id]
			print(degree_reqs.is_satisfied(prev_courses))
		else:
			print()
	
	# Otherwise, run the next recursion
	else:
		print()

		prev_cc_id = re.findall(path_split_pattern, Path)
		prev_courses = [i.split('-')[0] for i in prev_cc_id]

		this_term_id = str((startyear - 1899) * 10 + [2,4,6][(t-1)%3])

		G = nx.Graph()

		cc_schedules = {}

		# For all courses in this term
		for course in allcourses_by_term[this_term_id]:
			parts = course.strip().split('\t')
			term_id = parts[9]

			# If incorrect term, skip
			if term_id != this_term_id:
				continue

			# Else pull the rest of info from line
			course_id = parts[1]
			course_name = parts[2] + ' ' + parts[3]
			cc_id = parts[1] + '-' + parts[11]
			component = parts[12]
			days = parts[17]
			start_time = parts[15]
			end_time = parts[16]

			# If component is DIS, skip ######## MAY WANT TO MAKE MORE PRECISE LATER #####
			if component == 'DIS':
				continue

			# If any time parameters are None, skip
			# Since only subsets of output_timecourses.txt should be here, this shouldn't happen anyway
			if (days == 'None') or (start_time == 'None') or (end_time == 'None'):
				continue

			# Tentative: If course has been taken before, do not take again
			if course_id in prev_courses:
				continue
			##### TO DO: Should only do this for NON-REPEATABLE COURSES

			# If any pre-requisites have not been met, skip
			prereqs = req_dict[course_id][0]
			if not all(course_name2id[prereq] in prev_courses for prereq in prereqs):
				continue
			##### TO DO: Need to implement co-req check as well

			# If the course-class has already been considered, skip
			if cc_id in cc_schedules:
				continue

			# Get weekly schedule
			schedule = writeSchedule(days, start_time, end_time)

			# Add to dictionary of cc_schedules, with weekly schedule as value
			cc_schedules[cc_id] = schedule

			# Create node for current course
			G.add_node(cc_id)

			# Loop through all prev. courses;
			# Add edge between current course and any course with which it DOESN'T conflict,
			# and with which it does NOT have the same course ID
			for cc_id0 in cc_schedules:
				if not checkConflicting(cc_schedules[cc_id0], schedule) and (course_id != cc_id0.split('-')[0]):
					G.add_edge(cc_id0, cc_id)

		# Each clique represents a set of non-conflicting courses
		clique_list = list(nx.find_cliques(G))

		# Iterate over each possible student schedule by the following:
		step_id = 0 # First set step_id counter

		# For each clique (each possible student schedule):
		for i in range(len(clique_list)):
			offset = (0, 1)[i > 0] # To avoid printing multiple null sets
			# For each combination of up to 'max' courses within the clique:
			for z in chain.from_iterable(combinations(clique_list[i], r) for r in range(1,max_courses_per_qtr)): # instead of range(len(clique_list[0]+1))
				step_next = delim2.join(list(z))
				Path_next = Path + delim1 + step_next

				# Recurse!
				searchPath(startyear, t+1, T, branch_id + '.' + str(step_id), Path_next)

				# Update step_id counter
				step_id = step_id + 1

# Run the recursive function
searchPath(2011, 0, 12, '', '')

