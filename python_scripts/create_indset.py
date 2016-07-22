# Takes in lines from EC output, and returns large JSON file representing all pathways

from datetime import datetime
from collections import namedtuple
import sys
# import networkx

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

def checkConflictingCourse(schedule1, schedule2): # Schedule is a list of tuples
	for block1 in schedule1:
		start1 = datetime.strptime(block1[0], "%w %H:%M:%S %p")
		end1 = datetime.strptime(block1[1], "%w %H:%M:%S %p")
		for block2 in schedule2:
			start2 = datetime.strptime(block2[0], "%w %H:%M:%S %p")
			end2 = datetime.strptime(block2[1], "%w %H:%M:%S %p")
			if checkConflicting(start1, end1, start2, end2):
				return True
	# If all for-loops completed and still no conflicting blocks,
	return False

def checkConflicting(start_dt1, end_dt1, start_dt2, end_dt2):
	later_start = max(start_dt1, start_dt2)
	earlier_end = min(end_dt1, end_dt2)
	return earlier_end > later_start


prev_schedules = []

days1 = 'Tuesday|Thursday'
start_time1 = '10:00:00 AM'
end_time1 = '11:50:00 AM'

days2 = 'Tuesday|Thursday'
start_time2 = '11:00:00 AM'
end_time2 = '12:50:00 PM'

schedule1 = writeSchedule(days1, start_time1, end_time1)
schedule2 = writeSchedule(days2, start_time2, end_time2)

print(schedule1)
print(schedule2)
print(checkConflictingCourse(schedule1, schedule2))



# for w_str, w_n in weekday_replacements:
# 	days2 = days2.replace(w_str, w_n) 

# start_dts2 = [day + start_time2 for day in days2.split('|')]
# end_dts2 = [day + end_time2 for day in days2.split('|')]

# print(start_dts2)

# for schedule in prev_schedules:

# 	for block in schedule:

#for line in sys.stdin:
	# somehow get days and start_time and end_time


