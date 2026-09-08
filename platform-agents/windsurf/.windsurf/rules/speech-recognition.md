---
trigger: glob
description: "Transcribes audio to text with OpenAI Whisper and Vosk, converting formats, tuning models, and producing SRT/VTT subtitles. Use when working with whisper transcription, vosk offline, audio preparation or when the user mentions whisper transcription, vosk offline, audio preparation."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

Transcribes audio to text with OpenAI Whisper and Vosk, converting formats, tuning models, and producing SRT/VTT subtitles.

## Agentic Workflow: Read -> Reason -> Act (speech-recognition)

You are **speech-recognition** (ai) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — ai context for `speech-recognition`
- Domain: Transcribes audio to text with OpenAI Whisper and Vosk, converting formats, tuning models, and producing SRT/VTT subtitles.
- **whisper-transcription**: Transcribe audio files with Whisper models and options. — `whisper audio.mp3 --model small`
- **vosk-offline**: Stream and transcribe with the lightweight Vosk models. — `vosk-transcriber -i audio.wav -o transcript.txt`
- **audio-preparation**: Convert and inspect audio before transcription. — `ffmpeg -i input.m4a -ar 16000 -ac 1 output.wav`
- Check `knowledge` and `prerequisites: python, whisper, pyttsx3, vosk`

### 2. Reason — think for `speech-recognition`
- For `whisper-transcription`: Transcribe audio files with Whisper models and options. — decide which checks to run
- For `vosk-offline`: Stream and transcribe with the lightweight Vosk models. — decide which checks to run
- For `audio-preparation`: Convert and inspect audio before transcription. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `speech-recognition` tools
- Tools: `Glob`, `Grep`, `Read`, `Whisper`, `Vosk-transcriber` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `speech-recognition:09bf6477`

# Speech Recognition

Transcribe and subtitle audio with open-source speech-to-text tools.

## What This Skill Does

- Transcribes audio with Whisper in multiple languages
- Produces SRT, VTT, and JSON subtitles
- Uses Vosk for lightweight offline streaming
- Prepares audio (format, rate, chunking) with ffmpeg

## When to Use

- Generating subtitles for media
- Searchable transcripts for meetings and podcasts
- Voice-driven QA or dataset preparation

## Real Commands

```bash
# Whisper
whisper audio.mp3 --model small
whisper meeting.wav --model large-v3 --output_format srt
whisper podcast.m4a --model medium --language de
whisper audio.mp3 --model base --output_dir ./transcripts --output_format vtt

# Preprocess for accuracy
ffmpeg -i input.m4a -ar 16000 -ac 1 output.wav
ffmpeg -i long.mp3 -ss 00:10:00 -t 600 chunk.mp3

# Vosk
vosk-transcriber -i audio.wav -o transcript.txt
vosk-transcriber -i audio.wav --lang de
```

## Best Practices

- Downmix to mono 16kHz before transcription for best accuracy
- Pick model size by accuracy vs speed; large-v3 for demanding output
- Specify --language when known to avoid auto-detection errors
- Chunk long recordings to limit context drift
- Review automated transcripts against the source audio for critical use

## Capabilities

### whisper-transcription
Transcribe audio files with Whisper models and options.

**Parameters:**
- `model` (string): Model size: tiny, base, small, medium, large, large-v3
- `language` (string): Source language code, e.g. en, de, zh
- `outputFormat` (string): Output: txt, vtt, srt, json

**Commands:**
- `whisper audio.mp3 --model small`
- `whisper audio.mp3 --language en --task transcribe`
- `whisper meeting.wav --model large-v3 --output_format srt`
- `whisper podcast.m4a --model medium --language de --fp16 False`
- `whisper audio.mp3 --model base --output_dir ./transcripts --output_format vtt`

**Examples:**
- whisper audio.mp3 --model small
- whisper meeting.wav --model large-v3 --output_format srt
- whisper podcast.m4a --model medium --language de

### vosk-offline
Stream and transcribe with the lightweight Vosk models.

**Parameters:**
- `input` (string): Input audio file
- `lang` (string): Language model, e.g. en-us, de, zh-cn

**Commands:**
- `vosk-transcriber -i audio.wav -o transcript.txt`
- `vosk-transcriber -i audio.wav --model en-us --lang en`
- `vosk-transcriber --list-models`
- `python -m vosk-transcribe audio.wav`

**Examples:**
- vosk-transcriber -i audio.wav -o transcript.txt
- vosk-transcriber -i audio.wav --lang de
- vosk-transcriber --list-models

### audio-preparation
Convert and inspect audio before transcription.

**Parameters:**
- `input` (string): Source media file
- `sampleRate` (number): Target sample rate, e.g. 16000

**Commands:**
- `ffmpeg -i input.m4a -ar 16000 -ac 1 output.wav`
- `ffprobe -show_format input.mp3`
- `ffmpeg -i long.mp3 -ss 00:10:00 -t 600 chunk.mp3`
- `ffmpeg -i video.mp4 -vn audio.wav`

**Examples:**
- ffmpeg -i input.m4a -ar 16000 -ac 1 output.wav
- ffprobe -show_format input.mp3
- ffmpeg -i video.mp4 -vn audio.wav

## References
- [Whisper GitHub](https://github.com/openai/whisper)
- [Vosk Documentation](https://alphacephei.com/vosk/)
- [ffmpeg Documentation](https://ffmpeg.org/documentation.html)
