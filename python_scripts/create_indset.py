
# First check schedule overlap

from datetime import datetime
from collections import namedtuple

def checkConflicting(start_dt1, end_dt1, start_dt2, end_dt2):
	later_start = max(start_dt1, start_dt2)
	earlier_end = min(end_dt1, end_dt2)
	return earlier_end > later_start

d1 = datetime.strptime("1 " + "10:00:00 AM", "%d %H:%M:%S %p")
d2 = datetime.strptime("1 " + "11:00:00 AM", "%d %H:%M:%S %p")
d3 = datetime.strptime("2 " + "10:00:00 AM", "%d %H:%M:%S %p")
d4 = datetime.strptime("2 " + "11:00:00 AM", "%d %H:%M:%S %p")
print(d1)
print(d2)
print(d3)
print(d4)

print(checkConflicting(d1,d2,d3,d4))
print(checkConflicting(d1,d3,d2,d4))