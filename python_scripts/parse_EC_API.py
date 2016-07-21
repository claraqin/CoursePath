# -*- coding: utf-8 -*- 
"""Parse ExploreCourses XML."""
from collections import OrderedDict
import json
import time
import sys
import urllib.request
import xmltodict # must install at https://anaconda.org/asmeurer/xmltodict

# Unless year is specified as an additional argument to the command-line call, this script
# will parse the 2015-2016 catalog
if(len(sys.argv)>1):
	parse_year = sys.argv[1]
else:
	parse_year = 20152016

#EC_url = "http://explorecourses.stanford.edu/search?view=xml-20140630&academicYear=" + str(parse_year) + "&page=0&q=STATS&filter-departmentcode-STATS=on&filter-coursestatus-Active=on&filter-term-Summer=on"
EC_url = "http://explorecourses.stanford.edu/search?view=xml-20140630&academicYear=" + str(parse_year) + "&filter-coursestatus-Active=on&q=%25"

# string_replacements = [ 
# 	["\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t", "|"],
# 	["\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t", "|"],
# 	["\\n", "\\\\n"],
# 	["\\r", "\\\\r"],
# 	["\\t", "\\\\t"],
# 	["'", "\\'"]
# ]

header = ['year','course_id','subject','catalog_nbr','school','gers','units_min','units_max','repeatable','term_id','section_nbr','class_id','component','enrollment','instructors','start_time','end_time','days']
print('\t'.join(header))

# "collapse" is a helper function that simplifies a JSON object that has been converted from XML by xmltodict.
# field2 is nested under field1 and is redundant. We want to combine them.
# 
# Example input 1:
#    the_dict = {field1: {field2: [a,b,c]}}, where, e.g., field1 = "attributes" and field2 = "attribute"
# That's just how the dict looks like when we convert XML to JSON.
# 
# Example output 1:
#     the_dict = {field1: [a,b,c]}
# 
# Even worse, if field2 has only one element in the list, the parser removes the list and make it a direct child.
# The end users then have to check the type of the object whether it's a list or not, which is undesirable.
# 
# Example input 2:
#    the_dict = {field1: {field2: a}}
# 
# Example output 2:
#    the_dict = {field1: [a]}
def collapse(the_dict, field1, field2):
	if (
		the_dict
		and field1 in the_dict
		and the_dict[field1]
		and field2 in the_dict[field1]
	):
		if type(the_dict[field1][field2]) is list:
			the_dict[field1] = the_dict[field1][field2]
		else:
			the_dict[field1] = [the_dict[field1][field2]]

if __name__ == '__main__':
	init_time = time.time()
	with urllib.request.urlopen(EC_url) as the_file:
		doc = xmltodict.parse(the_file.read())
		the_file.close()

		for course in doc["xml"]["courses"]["course"]:

			# parsing xml into json has some redundancies. We'll collapse those 
			# to make the final object easier to read through
			collapse(course, "sections", "section")
			collapse(course, "attributes", "attribute")
			collapse(course, "tags", "tag")
			collapse(course, "learningObjectives", "learningObjective")

			if "sections" in course and course["sections"]:
				for section in course["sections"]:
					collapse(section, "schedules", "schedule")
					if "schedules" in section and section["schedules"]:
						for schedule in section["schedules"]:
							collapse(schedule, "instructors", "instructor")

			# json_data = json.dumps(course, indent=2)
			# for find_string, replaced_string in string_replacements:
			#     json_data = json_data.replace(find_string, replaced_string)

			# print(json_data)

			year = course["year"]
			subject = course["subject"]
			catalog_nbr = course["code"]
			repeatable = course["repeatable"]
			units_min = course["unitsMin"]
			units_max = course["unitsMax"]
			gers = course["gers"]

			course_id = course["administrativeInformation"]["courseId"]
			school = course["administrativeInformation"]["academicGroup"]

			if course["sections"] is None:
				course["sections"] = []

			for section in course["sections"]:
				term_id = section["termId"]
				section_nbr = section["sectionNumber"]
				class_id = section["classId"]
				component = section["component"]
				enrollment = section["currentClassSize"]

				for schedule in section["schedules"]:
					start_time = None
					end_time = None
					days = None
					instructors = []

					if "startTime" in schedule and schedule["startTime"]:
						start_time = schedule["startTime"]
					if "endTime" in schedule and schedule["endTime"]:
						end_time = schedule["endTime"]
					if "days" in schedule and schedule["days"]:
						days = schedule["days"]
						days = days.replace("\n\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t", "|")
						days = days.replace("\n\t\t\t\t\t\t\t\t\t\t\t", "|")
					if "instructors" in schedule and schedule["instructors"]:
						for instructor in schedule["instructors"]:
							instructors.append(instructor["sunet"])

					print(year, end='\t')
					print(course_id, end='\t')
					print(subject, end='\t')
					print(catalog_nbr, end='\t')
					print(school, end='\t')
					print(gers, end='\t')
					print(units_min, end='\t')
					print(units_max, end='\t')
					print(repeatable, end='\t')

					print(term_id, end='\t')
					print(section_nbr, end='\t')
					print(class_id, end='\t')
					print(component, end='\t')
					print(enrollment, end='\t')
					print('|'.join(instructors), end='\t')

					print(start_time, end='\t')
					print(end_time, end='\t')
					print(days)

	#elapsed_time = time.time() - init_time
	#print(">> Checking done. Time spent = {:.01f} s ({:.01f} hrs)".format(elapsed_time, elapsed_time/3600))