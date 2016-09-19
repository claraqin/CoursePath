"""
Prepares the output of print_pathways.py so that it can be easily used in R script.

Script:

	python print_pathways.py [args] | python post_awk2.py > output.txt

"""

import sys

for line in sys.stdin:
	line_split = line.split('\t')
	if line_split[4].strip() == 'True':
		path = line_split[3]
		path_split = path.split('|')
		print('\t'.join(path_split[1:]))
