# Podcast transcription
A transcription pipeline for Radio bubb.la and other podcasts.

Whisper is used for transcription, pyannote for speaker diarization.

The pipeline is organized in a sequence of steps with correspoding data directories:


00-info files with meta information such as speaker names

00-mp3 mp3 files to transcribe

01-wav wav versions of the input files

02-pyannote speaker diarization output

03-whisper transcription output

04-speaker speaker names assigned to time segments

05-text complete transcription with speaker diarization


A make file defines the processing steps.
