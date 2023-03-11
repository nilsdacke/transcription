import whisper
import json
import sys

mp3_file = sys.argv[1]
out_file = sys.argv[2]

model = whisper.load_model("large", device='cuda')
result = model.transcribe(mp3_file, language='sv')
with open(out_file, "w") as f:
    json.dump(result, f)
