import sys
from pydub import AudioSegment

mp3_file = sys.argv[1]
wav_file = sys.argv[2]

mp3_audio = AudioSegment.from_mp3(mp3_file)
mp3_audio.export(wav_file, format='wav')
