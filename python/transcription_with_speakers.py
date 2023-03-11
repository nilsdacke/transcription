import json
import sys

segments_file = sys.argv[1]
info_file = sys.argv[2]
output_file = sys.argv[3]

with open(segments_file, 'r') as f:
    segments_with_speakers = json.load(f)

with open(info_file, 'r') as f:
    info = json.load(f)

speakers = segments_with_speakers['speakers']
segments = segments_with_speakers['segments']
real_names = info['speakers']
speaker_dict = { generic_name: real_name for generic_name, real_name in zip(speakers, real_names) }

last_speaker = None
last_break = 0
last_ending_char = None

text = []
for segment in segments:
    generic_speaker = segment['speaker']
    main = speaker_dict.get(generic_speaker, generic_speaker)
    # main = speaker_dict[segment['speaker']]
    if main != last_speaker:
        if last_speaker is not None:
            text.append("\n\n")
            
        text.append(f"{main}:\n")
        last_speaker = main
        last_break = segment['start']
        text.append(segment['text'][1:])
    elif segment['start'] - last_break > 60 and last_ending_char in '.?!':
        text.append("\n\n")
        last_break = segment['start']
        text.append(segment['text'][1:])
    else:
        text.append(segment['text'])
        
    last_ending_char = segment['text'][-1]
    
output = ''.join(text)
with open(output_file, "w") as f:
    f.write(output)
