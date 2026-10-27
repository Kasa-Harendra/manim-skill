# Qwen3-TTS 0.6B Voice Cloning Directory

This directory stores the user reference audio, reference transcript, and the automated voice cloning pipeline for generating Manim explainer video voiceovers.

---

## Quick Setup

To clone your voice for Manim videos:

1. **Record a 3–10 second voice sample** of yourself speaking clearly in a quiet environment.
2. Save the audio file as:
   ```
   assets/voice_clone/reference_audio.wav
   ```
   *(MP3, M4A, or WAV format are supported)*
3. Save the exact transcript of what you said in that sample as:
   ```
   assets/voice_clone/reference_text.txt
   ```

---

## How It Works During Video Creation

Whenever you ask to generate a video:
1. The script narration is split by scene or paragraph.
2. `voice_clone_pipeline.py` uses `Qwen/Qwen3-TTS-12Hz-0.6B-Base` with your `reference_audio.wav` and `reference_text.txt`.
3. It generates high-fidelity cloned voiceover WAV files for each scene.
4. The audio timestamps are aligned via Faster-Whisper to drive frame-accurate Manim animations!
