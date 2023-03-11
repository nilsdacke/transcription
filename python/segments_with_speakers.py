import json
import sys


class SpeechSegment:
    def __init__(self, start, end, speakers=None):
        self.start = start
        self.end = end

    def intersection_length(self, other):
        return max(0, min(self.end, other.end) - max(self.start, other.start))

    def intersection_sum(self, segments):
        return sum([self.intersection_length(s) for s in segments])


class DiarizationSegment(SpeechSegment):
    def __init__(self, start, end, speaker):
        super().__init__(start, end)
        self.speaker = speaker

    @staticmethod
    def list_speakers(diarization):
        return DiarizationSegment._remove_duplicates([segment.speaker for segment in diarization])

    @staticmethod
    def _remove_duplicates(list_with_duplicates):
        return list(dict.fromkeys(list_with_duplicates))  # Assumes python >= 3.7


class WhisperSegment(SpeechSegment):
    def __init__(self, start, end, text, speakers=None):
        super().__init__(start, end)
        self.text = text
        self.speakers = speakers if speakers is not None else {}

    def intersection_sums(self, diarization, speakers):
        sums = {}
        for speaker in speakers:
            total = self.intersection_sum([segment for segment in diarization if segment.speaker == speaker])
            if total > 0:
                sums[speaker] = total
        return sums

    def main_speaker(self):
        return max(self.speakers, key=self.speakers.get) if self.speakers else ""


diarization_file = sys.argv[1]
transcription_file = sys.argv[2]
output_file = sys.argv[3]

with open(diarization_file, 'r') as f:
    diarization = json.load(f)

with open(transcription_file, 'r') as f:
    transcription = json.load(f)

diarization = [DiarizationSegment(s['start'], s['end'], s['speaker']) for s in diarization]
speakers = DiarizationSegment.list_speakers(diarization)
whisper_segments = [WhisperSegment(r['start'], r['end'], r['text']) for r in transcription['segments']]
whisper_segments = [WhisperSegment(w.start, w.end, w.text, w.intersection_sums(diarization, speakers)) for w in whisper_segments]
output = {'speakers': speakers, 'segments': [{"start": w.start, "end": w.end, "text": w.text, "speaker": w.main_speaker()} for w in whisper_segments]}

with open(output_file, "w") as f:
    json.dump(output, f)
