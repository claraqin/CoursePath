# Takes in lines representing all relevant classes in a given quarter, and returns all possible 
# class schedules in the quarter (i.e. independent sets in the class co-occurrence network)

from datetime import datetime
from collections import namedtuple
import sys
import networkx as nx
from itertools import chain, combinations

weekday_replacements = [
	['Monday', '1 '],
	['Tuesday', '2 '],
	['Wednesday', '3 '],
	['Thursday', '4 '],
	['Friday', '5 '],
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

G = nx.Graph()

prev_courses = {}

for line in sys.stdin:
	parts = line.strip().split('\t')
	cc_id = parts[1] + '-' + parts[11]
	days = parts[17]
	start_time = parts[15]
	end_time = parts[16]

	# If any time parameters are None, skip
	# Since only subsets of output_timecourses.txt should be here, this shouldn't happen anyway
	if (days == 'None') or (start_time == 'None') or (end_time == 'None'):
		continue

	# If the course has already been entered, skip ("continue")
	if cc_id in prev_courses.keys():
		continue
	
	# Get schedule
	schedule = writeSchedule(days, start_time, end_time)

	# Add to dictionary of prev_courses, with schedule as value
	prev_courses[cc_id] = schedule

	G.add_node(cc_id)

	# Loop through all prev. courses;
	# Add edge between current course and any course with which it conflicts
	for pcc_id in prev_courses.keys():
		if checkConflicting(prev_courses[pcc_id], schedule):
			G.add_edge(pcc_id, cc_id)

clique_list = list(nx.find_cliques(G))


# Print all possible schedules consisting of less than 8 courses
# Yes, this assumes a cap on the number of courses that a student may take in a quarter
n = 0
for i in range(len(clique_list)):
	offset = (0, 1)[i > 0] # To avoid printing multiple null sets
	for z in chain.from_iterable(combinations(clique_list[i], r) for r in range(offset,8)): # instead of range(len(clique_list[0]+1))
		print('|'.join(list(z)))
		n += 1

print(n)



