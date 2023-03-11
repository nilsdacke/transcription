import json
import csv
import sys
from pathlib import Path 


def write_info_file(json_file_name, speakers):
    dictionary = {'speakers': speakers}
    with open(json_file_name, 'w') as f:
        json.dump(dictionary, f)


csv_file = sys.argv[1]
output_dir = sys.argv[2]

info_path = Path(output_dir)

with open(csv_file, 'r') as f:
    speaker_lists = csv.reader(f)
    for row in speaker_lists:
        json_file_name = info_path / (row[0] + '.json') 
        speakers = [s.strip() for s in row[1:] if s.strip()]
        write_info_file(json_file_name, speakers)

