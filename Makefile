MP3_FOLDER := 00-mp3
INFO_FOLDER := 00-info
WAV_FOLDER := 01-wav
PYANNOTE_FOLDER := 02-pyannote
WHISPER_FOLDER := 03-whisper
SPEAKER_FOLDER := 04-speaker
TEXT_FOLDER := 05-text
PYTHON_FOLDER := python

MP3S := $(shell find $(MP3_FOLDER) -name '*.mp3')
TEXTS := $(MP3S:$(MP3_FOLDER)/%.mp3=$(TEXT_FOLDER)/%.txt)
WAVS := $(MP3S:$(MP3_FOLDER)/%.mp3=$(WAV_FOLDER)/%.wav)
DIARIZATIONS := $(MP3S:$(MP3_FOLDER)/%.mp3=$(PYANNOTE_FOLDER)/%.json)
TRANSCRIPTIONS := $(MP3S:$(MP3_FOLDER)/%.mp3=$(WHISPER_FOLDER)/%.json)
INFOS := $(MP3S:$(MP3_FOLDER)/%.mp3=$(INFO_FOLDER)/%.json)

all: $(TEXTS) $(DIARIZATIONS) $(TRANSCRIPTIONS) $(INFOS)
	date

$(TEXT_FOLDER)/%.txt: $(SPEAKER_FOLDER)/%.json $(INFO_FOLDER)/%.json
	python $(PYTHON_FOLDER)/transcription_with_speakers.py $^ $@

$(SPEAKER_FOLDER)/%.json: $(PYANNOTE_FOLDER)/%.json $(WHISPER_FOLDER)/%.json 
	python $(PYTHON_FOLDER)/segments_with_speakers.py $^ $@

$(WHISPER_FOLDER)/%.json: $(MP3_FOLDER)/%.mp3
	date; python $(PYTHON_FOLDER)/whisper_transcription.py $? $@

$(PYANNOTE_FOLDER)/%.json: $(WAV_FOLDER)/%.wav
	date; python $(PYTHON_FOLDER)/pyannote_diarization.py $? $@

$(WAV_FOLDER)/%.wav: $(MP3_FOLDER)/%.mp3
	python $(PYTHON_FOLDER)/mp3_to_wav.py $? $@

$(INFO_FOLDER)/%.json: 
	python $(PYTHON_FOLDER)/info_file.py $@

