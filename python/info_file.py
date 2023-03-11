import json
import sys

info_file = sys.argv[1]
with open(info_file, 'w') as f:
	json.dump({'speakers': ["Martin", "Boris"]}, f)

