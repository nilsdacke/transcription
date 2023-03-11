from pyannote.audio import Pipeline
from pydub import AudioSegment
import json
import sys

wav_file = sys.argv[1]
out_file = sys.argv[2]
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="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")

diarization = pipeline(wav_file)
data = [{"start": turn.start, "end": turn.end, "speaker": speaker} for turn, _, speaker in diarization.itertracks(yield_label=True)]
with open(out_file, "w") as f:
    json.dump(data, f)

