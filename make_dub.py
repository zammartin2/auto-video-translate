#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil
import logging
from pathlib import Path
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from pydub import AudioSegment
from tqdm import tqdm
import imageio_ffmpeg as ffmpeg
import whisper

# -------------------------
# Insert your API tokens here!
# -------------------------
DEEPL_API_KEY      = os.getenv("DEEPL_API_KEY")      or "YOUR_DEEPL_API_KEY"
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") or "YOUR_ELEVENLABS_API_KEY"
ELEVENLABS_VOICE   = "21m00Tcm4TlvDq8ikWAM"  # example voice ID

# -------------------------
# Configuration
# -------------------------
VIDEO_PATH     = "WeChat_20250701144439.mp4"
AUDIO_PATH     = "audio.wav"
DUBBED_RAW     = "dubbed_audio.wav"
DUBBED_LOUD    = "dubbed_audio_loud.wav"
OUTPUT_VIDEO   = "WeChat_20250701144439_ru_dubbed.mp4"
TMP_DIR        = Path("tts_segments_tmp")
VOLUME_FACTOR  = 7.0    # amplification multiplier
MAX_WORKERS    = 4      # threads for parallel TTS

os.makedirs(TMP_DIR, exist_ok=True)
FFMPEG = ffmpeg.get_ffmpeg_exe()

# Setup logging to show progress in console
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Load Whisper model for transcription
model = whisper.load_model("small")


# 1. Extract audio from the input video
def extract_audio():
    logger.info("Extracting audio from video...")
    subprocess.run([
        FFMPEG, "-y", "-i", VIDEO_PATH,
        "-ac", "1", "-ar", "16000", "-vn",    # mono, 16kHz, no video
        "-c:a", "pcm_s16le", AUDIO_PATH
    ], check=True)


# 2. Transcribe audio segments with Whisper
def transcribe():
    logger.info("Transcribing audio with Whisper...")
    result = model.transcribe(AUDIO_PATH)
    segments = [
        {"start": seg["start"], "end": seg["end"], "text": seg["text"].strip()}
        for seg in result["segments"]
    ]
    logger.info(f"Found {len(segments)} segments")
    return segments


# 3. Translate text to Russian via DeepL (with in-memory caching)
@lru_cache(maxsize=512)
def translate(text: str) -> str:
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": "RU"
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()["translations"][0]["text"]


# 4. Generate one TTS segment using ElevenLabs and prepend silence
def synth_segment(idx, seg):
    # Translate source text
    ru_text = translate(seg["text"])
    wav_path = TMP_DIR / f"seg_{idx}.wav"

    # Call ElevenLabs TTS API, streaming WAV output
    voice_url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE}/stream"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    json_body = {
        "text": ru_text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    r = requests.post(voice_url, headers=headers, json=json_body, stream=True)
    r.raise_for_status()
    with open(wav_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    # Prepend silence so that this segment aligns to its original timestamp
    audio = AudioSegment.from_file(wav_path, format="wav")
    silence = AudioSegment.silent(duration=int(seg["start"] * 1000))
    (silence + audio).export(wav_path, format="wav")
    return wav_path


# 5. Build full dubbed audio by overlaying all segments
def build_dub_audio(segments):
    logger.info("Building dubbed audio...")
    wav_paths = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(synth_segment, i+1, seg): i+1
            for i, seg in enumerate(segments)
        }
        for fut in tqdm(as_completed(futures), total=len(futures), desc="TTS"):
            wav_paths.append(fut.result())

    logger.info("Merging all segments into one track...")
    final = AudioSegment.silent(duration=0)
    for wav in sorted(wav_paths, key=lambda p: int(p.stem.split("_")[1])):
        segment = AudioSegment.from_file(wav, format="wav")
        # Overlay each segment so longer ones are preserved
        if len(segment) > len(final):
            final = final.overlay(segment)
        else:
            final = final + AudioSegment.silent(duration=len(segment))
            final = final.overlay(segment)

    final.export(DUBBED_RAW, format="wav")


# 6. Amplify volume of the raw dubbed track
def amplify_audio():
    logger.info("Amplifying volume...")
    subprocess.run([
        FFMPEG, "-y", "-i", DUBBED_RAW,
        "-filter:a", f"volume={VOLUME_FACTOR}",
        DUBBED_LOUD
    ], check=True)


# 7. Mux the amplified audio back into the original video
def mux_video():
    logger.info("Muxing dubbed audio into video...")
    subprocess.run([
        FFMPEG, "-y",
        "-i", VIDEO_PATH,
        "-i", DUBBED_LOUD,
        "-c:v", "copy",
        "-map", "0:v",
        "-map", "1:a",
        "-shortest",
        OUTPUT_VIDEO
    ], check=True)


# 8. Cleanup temporary files
def cleanup():
    logger.info("Cleaning up temporary files...")
    shutil.rmtree(TMP_DIR)
    os.remove(AUDIO_PATH)
    os.remove(DUBBED_RAW)


# Main execution flow
if __name__ == "__main__":
    extract_audio()
    segments = transcribe()
    build_dub_audio(segments)
    amplify_audio()
    mux_video()
    cleanup()
    logger.info(f"Done! Output file: {OUTPUT_VIDEO}")
