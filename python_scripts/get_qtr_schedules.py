# Takes in lines representing all relevant classes in a given quarter, and returns all possible 
# class schedules in the quarter (i.e. independent sets in the class co-occurrence network)

from datetime import datetime
from collections import namedtuple
import sys
# import networkx as nx

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

# G = nx.Graph()

prev_courses = {}

# for line in sys.stdin:
# 	# get cc_id = course_id + class_id
# 	# get days
# 	# get start time
# 	# get end time

#	if cc_id not in prev_courses.keys(): proceed
#	else next input line
	
	# Get schedule
	schedule = writeSchedule(days, start_time, end_time)

	# Add to dictionary of prev_courses, with schedule as value
	prev_courses[cc_id] = schedule

	G.add_node(cc_id)

	# Loop through all prev. courses;
	# Add edge between current course and any course with which it conflicts
	for pc in prev_courses.keys():
		#if conflicts with pc: # Alternatively, if doesn't conflict then just look for cliques instead of independent sets later.
			G.add_edge(pc, cc_id)

print(list(find_cliques(G)))


# days1 = 'Tuesday|Thursday'
# start_time1 = '10:00:00 AM'
# end_time1 = '11:50:00 AM'

# days2 = 'Tuesday|Thursday'
# start_time2 = '11:00:00 AM'
# end_time2 = '12:50:00 PM'

# schedule1 = writeSchedule(days1, start_time1, end_time1)
# schedule2 = writeSchedule(days2, start_time2, end_time2)

# print(schedule1)
# print(schedule2)
# print(checkConflicting(schedule1, schedule2))




