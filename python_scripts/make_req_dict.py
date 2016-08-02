# Makes pre-requisite/co-requisite dictionary from Edusalsa's prereq JSON

import json
import sys
from pprint import pprint

req_dict = {}

for line in sys.stdin:
	entry = json.loads(line)

	req_dict[entry['code']] = [entry['prereq'], entry['coreq']]

with open('req_dict.json', 'w') as f:
	json.dump(req_dict, f)