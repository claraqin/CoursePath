# Recursively prints all pathways possible in 2011-2016 given a set of relevant courses.
# An extension of get_qtr_schedules.py

from datetime import datetime
import re
import sys
import networkx as nx
from itertools import chain, combinations

allcourses = []
for line in sys.stdin:
	allcourses.append(line)

# allcourses = open("../ec_data/output_timecourses.txt", 'r')

max_courses_per_qtr = 6

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

# Write schedule as a list of tuples. Each tuple is start_time, end_time:
def writeSchedule(days, start_time, end_time):
	for w_str, w_n in weekday_replacements:
		days = days.replace(w_str, w_n)
	schedule = []
	for day in days.split('|'):
		schedule.append((day + start_time, day + end_time))
	return schedule

def checkConflicting(schedule1, schedule2): # Schedule is a list of tuples
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


def searchPath(Path, startyear, t, T):
	print(Path)
	prev_cc_id = re.findall(path_split_pattern, Path)
	prev_courses = [i.split('-')[0] for i in prev_cc_id]

	correct_term_id = str((startyear - 1899) * 10 + [2,4,6][(t-1)%3])

	G = nx.Graph()

	cc_schedules = {}

	for course in allcourses:
		parts = course.strip().split('\t')
		term_id = parts[9]

		# If incorrect term, skip
		if term_id != correct_term_id:
			continue

		# Else pull the rest of info from line
		course_id = parts[1]
		cc_id = parts[1] + '-' + parts[11]
		days = parts[17]
		start_time = parts[15]
		end_time = parts[16]


		# If any time parameters are None, skip
		# Since only subsets of output_timecourses.txt should be here, this shouldn't happen anyway
		if (days == 'None') or (start_time == 'None') or (end_time == 'None'):
			continue

		# If the course has already been entered, skip ("continue")
		if cc_id in cc_schedules.keys():
			continue
		
		if course_id in prev_courses:
			continue
		##### TO DO: If course's prereqs have not been met, or if it is a repetition of a 
		#####        NON-REPEATABLE course, then skip.

		# Get schedule
		schedule = writeSchedule(days, start_time, end_time)

		# Add to dictionary of cc_schedules, with schedule as value
		cc_schedules[cc_id] = schedule

		# Create node for current course
		G.add_node(cc_id)

		# Loop through all prev. courses;
		# Add edge between current course and any course with which it DOESN'T conflict
		for cc_id0 in cc_schedules.keys():
			if not checkConflicting(cc_schedules[cc_id0], schedule):
				G.add_edge(cc_id0, cc_id)

	print("Nodes:" + str(len(G)))

	clique_list = list(nx.find_cliques(G))

	# Either continue to next recursion, or if t==T, print all
	if t==(T-1): ########### T-1 is only a temporary fix - I need to fix my recursive step
		for i in range(len(clique_list)):
			offset = (0, 1)[i > 0] # To avoid printing multiple null sets
			for z in chain.from_iterable(combinations(clique_list[i], r) for r in range(offset,max_courses_per_qtr)): # instead of range(len(clique_list[0]+1))
				pass
				#print(Path + '\t' + '|'.join(list(z)))
	else:
		for i in range(len(clique_list)):
			offset = (0, 1)[i > 0] # To avoid printing multiple null sets
			for z in chain.from_iterable(combinations(clique_list[i], r) for r in range(offset,max_courses_per_qtr)): # instead of range(len(clique_list[0]+1))
				Path_next = Path + '\t' + '|'.join(list(z))
				searchPath(Path_next, startyear, t+1, T)

searchPath('', 2015, 1, 3)


