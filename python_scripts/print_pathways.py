"""
Recursively prints all pathways possible in 2011-2016 given a set of relevant courses.
In doing so, reformats manually-entered degree reqs (.txt) into a JSON file.

Script:

	python print_pathways.py [-h] [manual_degree_reqs] [start_year] [T] [max_courses_per_qtr] [start_path]
	python print_pathways.py ../degree_reqs/ecoevo/reqs_ecoevo_sub.txt 2012 6 6 'MATH 19, MATH 20, MATH 21, MATH 41, MATH 42, PHYSICS 41, CHEM 31X, CHEM 33' | python post_print_pathways.py > ../out_pathways/pathways_ecoevo_sub.txt

Notes:

	Currently skips any 'DIS' sections

	Does not yet check co-requisites

	Currently skips any course repeats, even potentially repeatable ones

	req_dict was made using the 2015-2016 catalogue

"""

from datetime import datetime
import re
import sys
import json
import argparse
import networkx as nx
import constraint as c
import format_reqs_json as format
import relevant_courses as rc
# from pprint import pprint
from itertools import chain, combinations

# Hard-coded filenames:
# (1) prereq dict
# (2) course name-to-ID dict
# (3) course ID-to-name dict
# (4) default allcourses
# (5) json degree req output - depends only on first arg (see main)
filename_prereqs = '../dict/req_dict_nested.json'
filename_coursename2id = '../dict/course_name2id_dict.json'
filename_courseid2name = '../dict/course_id2name_dict.json'
filename_default_allcourses = '../ec_data/output_courses_w_times.txt'

with open(filename_prereqs,'r') as f:
	req_dict = json.load(f)
with open(filename_coursename2id, 'r') as f:
	course_name2id = json.load(f)
with open(filename_courseid2name, 'r') as f:
	course_id2name = json.load(f)


#########
### THIS FUNCTION SHOULD BE REMOVED LATER
def nested_replace(input_d, reference_d):
	copy_d = input_d.copy()
	for k, v in iter(copy_d.items()):
		if isinstance(v, list):
			copy_d[k] = [nested_replace(clause, reference_d) for clause in v]
		else:
			copy_d[k] = reference_d[v]
	return copy_d

# Delimiters to represent pathways 
# delim1 separates quarters, delim2 separates course-class IDs within the same quarter
delim1 = '|'
delim2 = ','

path_split_pattern = r'[\w]+'

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
	# step = Path.split('|')[-1] # The step (quarter schedule) that was taken to get here
	# try:
	# 	step_list = [course_id2name[course] for course in step.split(delim2)]
	# 	step_name = delim2.join(step_list)
	# except KeyError:
	# 	step_name = step

	Path_split = [[course_id2name[p] for p in step.split(delim2) if p is not ''] for step in Path.split(delim1)]
	Path_name = delim1.join([delim2.join(step) for step in Path_split])

	# Print the current Path:
	# print("t:" + str(t) + "\tT:" + str(T) + "\tbranch_id:" + branch_id + 
	# 	"\tstep:" + step_name + "\tpathway:" + Path_name, end='\t')
	print("t:" + str(t) + "\tT:" + str(T) + "\tbranch_id:" + branch_id + 
		"\tpathway:" + Path_name, end='\t')

	# If this is the final quarter, end this recursion branch (AFTER checking degree completion)
	if t == T:
		prev_cc_id = re.findall(path_split_pattern, Path)
		prev_courses = [i.split('-')[0] for i in prev_cc_id]
		print(degree_reqs.is_satisfied(prev_courses))
	
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
			#cc_id = parts[1] + '-' + parts[11]
			cc_id = parts[1]
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

			# If pre-requisites have not been satisfied, skip
			try:
				prereqs = req_dict[course_id][0]
				prereq_constraint = c.make_constraint(prereqs)
				if prereq_constraint is not None:
					if not prereq_constraint.is_satisfied(prev_courses):
						continue
			except KeyError:
				pass
			# ##### TO DO: Need to implement co-req check as well

			# If the course-class has already been considered this quarter, skip
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

		# If graph is empty, no classes can be taken this quarter
		if len(G) == 0:
			Path_next = Path + delim1
			searchPath(startyear, t+1, T, branch_id + '.0', Path_next)

		else:
			# Each clique represents a set of non-conflicting courses
			clique_list = list(nx.find_cliques(G))

			# Iterate over each possible student schedule by the following:
			step_id = 0 # First set step_id counter

			# For each clique (each possible student schedule):
			for i in range(len(clique_list)):
				offset = (0, 1)[i > 0] # To avoid printing multiple null sets
				# For each combination of up to 'max' courses within the clique:
				for z in chain.from_iterable(combinations(clique_list[i], r) for r in range(offset,max_courses_per_qtr)): # instead of range(len(clique_list[0]+1))
					z = [y.split('-')[0] for y in z]
					step_next = delim2.join(list(z))
					Path_next = Path + delim1 + step_next

					# Recurse!
					searchPath(startyear, t+1, T, branch_id + '.' + str(step_id), Path_next)

					# Update step_id counter
					step_id = step_id + 1

if __name__ in '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('manual_degree_reqs', nargs='?', type=argparse.FileType('r'), default='-',
		help='Input: manually-entered degree requirements, e.g. "../degree_reqs/geophysics/reqs_geophysics0.txt"')
	parser.add_argument('start_year', nargs='?', type=int, default=2011,
		help='Calendar year of the fall quarter from which to begin search')
	parser.add_argument('T', nargs='?', type=int, default=12,
		help='Max. no. of quarters (excluding summers) to search through')
	parser.add_argument('max_per_qtr', nargs='?', type=int, default=6,
		help='Max. no. of courses that students may take in any quarter')
	parser.add_argument('start_path', nargs='?', type=str, default='',
		help='"[course_name],[course_name],..." representing previously taken courses')
	args = parser.parse_args()

	# Using 1st argument (manual_degree_reqs), create JSON file of degree reqs and 
	# create Constraint object to represent degree requirements
	printDegreeCompletion = False
	reqs_txt = []
	for line in args.manual_degree_reqs:
		reqs_txt.append(line.strip())

	# Get all relevant courses using manual_degree_reqs
	allcourses_relevant = rc.get_relevant_courses(reqs_txt)

	# Create and write JSON file of degree reqs
	reqs_json = format.write_as_json(reqs_txt)
	filename_json = args.manual_degree_reqs.name.replace('.txt','.json')
	with open(filename_json, 'w') as outfile:
		json.dump(reqs_json, outfile, sort_keys=True, indent=4)

	# Make Constraint object from JSON file
	degree_reqs = c.make_constraint(reqs_json)

	# Read input (relevant courses only) for processing via recursive searchPath function
	# Arrange courses by term (using dict structure) so each iteration does not have to search through the 
	# entire allcourses
	allcourses_by_term = {}

	for line in allcourses_relevant:
		linesplit = line.split('\t')
		term_id = linesplit[9]
		if term_id in allcourses_by_term:
			allcourses_by_term[term_id].append(line)
		else:
			allcourses_by_term[term_id] = [line]

	# searchPath start year
	start_year = args.start_year

	# searchPath start path
	start_path = args.start_path
	start_path_split = start_path.split(',')
	start_path_ids = []
	for name in start_path_split:
		namestrip = name.strip()
		try:
			start_path_ids.append(course_name2id[namestrip])
		except KeyError:
			# print('Warning: Course name-to-ID dictionary does not contain ' + namestrip +
			# 	', so it will not be included in starting path.')
			pass
	start_path_str = ','.join(start_path_ids)

	# No. of quarters to search through
	T = args.T

	# Student can take no more than this number of courses in a quarter
	max_courses_per_qtr = args.max_per_qtr

	try:
		searchPath(start_year, 0, T, '', start_path_str)
	except BrokenPipeError:
		pass


