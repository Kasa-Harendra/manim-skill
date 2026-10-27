# Audio Generation & Animation Synchronization Guide

This reference defines the dual-mode execution workflow for Manim:
1. **Mode 1: Only Animation (Silent)** - Pure visual mathematics and motion.
2. **Mode 2: Audio + Animation (Studio Narration)** - End-to-end narrated pipeline with Kokoro ONNX TTS, Faster-Whisper alignment, and timestamp-synchronized Manim scenes.

---

## The Two Operational Modes

### Mode 1: Only Animation (Silent / Visual Math)
Use this mode when creating standalone geometric proofs, calculus intuitions, GIFs, silent tutorial clips, or when the user does not request audio.
- Pacing is determined mathematically:
  - Give major transformations room to breathe (`self.wait(0.8)` to `self.wait(1.5)`).
  - Use organic easing (`rate_func=smooth`).
  - No external audio dependencies or timing json required.

### Mode 2: Audio + Animation (The YouTube Explainer & Masterclass Pipeline)
Use this mode when generating narrated instructional videos, tutorials, or YouTube explainers.
- **Master Protocol Reference**: See **[youtube_explainer_workflow.md](youtube_explainer_workflow.md)** for the full 6-phase lifecycle:
  1. **Phase 0 (Intake & Grilling)**: Prompt user for duration, topic/thesis, audience level, visual style, and **always grill the user** on whether to proceed with **Kokoro TTS** or **Voice-Clone**. If voice clone, ask which accent or person voice profile from `assets/audio-references/` (e.g. `american`, `harendra`) to pass via `--voice <voice_name>` to `scripts/voice_clone_pipeline.py`.
  2. **Phase 1 (Script & Storyboard)**: Write `scripts/<Topic>_YouTube_Script.md` with tri-fold table (Visual Direction with Manim mobjects, Spoken Narration, Sound Design SFX).
  3. **Phase 2 (User Review Gate)**: Present script to user and STOP for review/approval before proceeding.
  4. **Phase 3 (Studio Narration & Alignment)**: Synthesize audio via Kokoro ONNX (`generate_audio.py`) or Qwen3-TTS Voice Cloning (`scripts/voice_clone_pipeline.py --voice <name>`), filter with 80Hz rumble cut, peak normalize, and align with Faster-Whisper to `timing.json`.
  5. **Phase 4 (Manim Choreography)**: Orchestrate scene with `sync_to(target_time)` and programmatic indentation code boxes (`make_wire_box`).
  6. **Phase 5 (Verification & Delivery)**: Monotonicity check, dry-run `manim -s`, full 1080p render, and snapshot visual audit.

---

## Audio Pipeline Implementation (`generate_audio.py`)

When generating audio from scratch for Mode 2, use this exact, verified architecture:

```python
#!/usr/bin/env python3
"""
Generates clean, studio-grade narration using Kokoro ONNX,
cleans the audio with an 80Hz rumble cut, and extracts word-level timestamps using Faster-Whisper.
"""

import os
import json
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt
import kokoro_onnx
from faster_whisper import WhisperModel

# Standard Cache Paths
MODEL_PATH = "/Users/kasaharendra/.cache/hyperframes/tts/models/kokoro-v1.0.onnx"
VOICES_PATH = "/Users/kasaharendra/.cache/hyperframes/tts/voices/voices-v1.0.bin"
OUTPUT_DIR = "voice"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Structured Scene Decomposition
SCENES = [
    {
        "id": "scene_1_intro",
        "title": "Introduction & Concept Anchor",
        "text": "Every API interaction begins with an address: the Uniform Resource Locator. But to build scalable backends, we must deconstruct what is actually happening across the wire."
    },
    # Add subsequent scenes...
]

def highpass_filter(data, sample_rate, cutoff=80):
    """80Hz 4th-order Butterworth high-pass filter to eliminate sub-bass rumble."""
    sos = butter(4, cutoff, 'hp', fs=sample_rate, output='sos')
    return sosfilt(sos, data)

def main():
    print("=== Step 1: Initializing Kokoro ONNX ===")
    kokoro = kokoro_onnx.Kokoro(MODEL_PATH, VOICES_PATH)
    
    sample_rate = 24000
    voice = "am_michael"  # Clear, authoritative instructional voice
    speed = 0.98          # Deliberate, relaxed pacing
    
    full_audio = []
    scene_markers = []
    current_sample = 0
    
    # Lead-in silence (0.6s)
    lead_silence = int(sample_rate * 0.6)
    full_audio.append(np.zeros(lead_silence, dtype=np.float32))
    current_sample += lead_silence
    
    for i, scene in enumerate(SCENES):
        start_time = current_sample / sample_rate
        print(f"Synthesizing [{scene['id']}]: {scene['title']}...")
        
        samples, _ = kokoro.create(scene["text"], voice=voice, speed=speed, lang="en-us")
        full_audio.append(samples)
        current_sample += len(samples)
        end_time = current_sample / sample_rate
        
        scene_markers.append({
            "id": scene["id"],
            "title": scene["title"],
            "start": round(start_time, 3),
            "end": round(end_time, 3),
            "duration": round(end_time - start_time, 3),
            "text": scene["text"]
        })
        
        # Inter-scene breathing room (1.1s pause between concepts)
        if i < len(SCENES) - 1:
            pause_samples = int(sample_rate * 1.1)
            full_audio.append(np.zeros(pause_samples, dtype=np.float32))
            current_sample += pause_samples
        else:
            # Trailing silence (1.0s)
            trail_samples = int(sample_rate * 1.0)
            full_audio.append(np.zeros(trail_samples, dtype=np.float32))
            current_sample += trail_samples

    total_audio_arr = np.concatenate(full_audio)
    total_duration = len(total_audio_arr) / sample_rate
    
    print("=== Step 2: Audio Engineering ===")
    cleaned_audio = highpass_filter(total_audio_arr, sample_rate, cutoff=80)
    
    # Peak normalization to -1.0 dB (~0.891)
    max_val = np.max(np.abs(cleaned_audio))
    if max_val > 0:
        target_peak = 10 ** (-1.0 / 20)
        cleaned_audio = cleaned_audio * (target_peak / max_val)
        
    master_wav_path = os.path.join(OUTPUT_DIR, "master_narration.wav")
    sf.write(master_wav_path, cleaned_audio, sample_rate)
    
    print("=== Step 3: Extracting Word-Level Timestamps ===")
    whisper_model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segments, info = whisper_model.transcribe(master_wav_path, word_timestamps=True)
    
    all_words = []
    transcript_segments = []
    for segment in segments:
        seg_dict = {
            "start": round(segment.start, 3),
            "end": round(segment.end, 3),
            "text": segment.text.strip(),
            "words": []
        }
        for word in segment.words:
            w_dict = {
                "word": word.word.strip(),
                "start": round(word.start, 3),
                "end": round(word.end, 3),
                "probability": round(word.probability, 3)
            }
            seg_dict["words"].append(w_dict)
            all_words.append(w_dict)
        transcript_segments.append(seg_dict)
        
    timing_data = {
        "audio_file": master_wav_path,
        "sample_rate": sample_rate,
        "total_duration": round(total_duration, 3),
        "scenes": scene_markers,
        "segments": transcript_segments,
        "words": all_words
    }
    
    timing_json_path = os.path.join(OUTPUT_DIR, "timing.json")
    with open(timing_json_path, "w") as f:
        json.dump(timing_data, f, indent=2)
        
    print(f"Saved exact timestamps to {timing_json_path}")

if __name__ == "__main__":
    main()
```

---

## Manim Synchronization Engine

In the Manim scene class, load the narration and lock all animations to `timing.json`:

```python
from manim import *
import json
import os

config.background_color = BLACK
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30

class NarratedScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Load Timing and Audio
        timing_path = os.path.join("voice", "timing.json")
        with open(timing_path, "r") as f:
            timing_data = json.load(f)

        audio_file = os.path.join("voice", "master_narration.wav")
        self.add_sound(audio_file)

        # 2. Precision Synchronization Harness
        current_time = 0.0

        def sync_to(target_time):
            """Fast-forward / wait until the exact timestamp in the narration."""
            nonlocal current_time
            if target_time > current_time:
                gap = target_time - current_time
                self.wait(gap)
                current_time = target_time

        def play_sync(*anims, run_time=1.0):
            """Play animations and advance the timeline counter."""
            nonlocal current_time
            self.play(*anims, run_time=run_time)
            current_time += run_time

        # 3. Synchronizing Scenes to Markers
        # Scene 1: Intro (0.6s)
        sync_to(0.6)
        title = Text("Concept Architecture", font="Helvetica Neue", font_size=32, weight=BOLD)
        play_sync(FadeIn(title, shift=DOWN * 0.2), run_time=1.5)

        # Scene 2: Concept Shift (17.2s)
        sync_to(17.2)
        play_sync(
            FadeOut(title, shift=UP * 0.2),
            # Transition to next stage...
            run_time=1.2
        )

        # Final Alignment: Hold to end of narration audio
        total_duration = timing_data["total_duration"]
        sync_to(total_duration - 1.0)
        play_sync(
            # Final graceful fadeout
            run_time=0.9
        )
        self.wait(0.1)
```

---

## Mandatory Pre-Render Audio-Sync & Screen Alignment Audit

Before rendering any Mode 2 video or delivering results to the user, you **MUST** execute this 3-step audit:

### Step 1: Word-Level Keyword Verification
Never guess animation trigger timestamps. Grep or parse `timing.json` to find the exact timestamp where the speaker begins pronouncing the key phrase or concept:
```python
# Verify exact segment/word timestamps from timing.json
# Example: If the speaker says "Directly below, key value headers..." at 33.70s:
# Use sync_to(33.7) -- NOT an arbitrary estimated time like 30.0s or 35.0s.
```

### Step 2: Timeline Math & Anti-Drift Verification
Timeline drift occurs when animation run times exceed the gap between narration cues:
- For every transition: verify `current_time + run_time <= next_cue_time`.
- If an animation has `run_time=2.0s` but the next concept begins in `1.5s`, shorten `run_time` to `1.2s` so the timeline remains locked to the audio track.
- Verify `play_sync` forwards `**kwargs` (e.g., `rate_func`) cleanly to `self.play(...)`:
  ```python
  def play_sync(*anims, run_time=1.0, **kwargs):
      nonlocal current_time
      self.play(*anims, run_time=run_time, **kwargs)
      current_time += run_time
  ```

### Step 3: Screen Centering & Visual Layout Audit
Extract representative frame screenshots using `ffmpeg` across every scene and inspect them:
```bash
ffmpeg -y -ss <cue_time> -i output.mp4 -frames:v 1 -update 1 frame_scene.png
```
- **Check 1: Single-Focus Elements**: Are titles, subtitles, formulas, and summary banners centered at `x = 0`?
- **Check 2: Multi-Column Geometry**: Are left-column items anchored to a common guideline (e.g. `x = -5.8`) and right-column items to a common guideline (e.g. `x = +0.8`) without lopsided staggering?
- **Check 3: Safe Margins**: Is all content contained inside `[-6.4, +6.4]` horizontally and `[-3.5, +3.5]` vertically, with zero edge clipping?

---

## Critical Rules for Audio + Animation Mode

1. **Always Use `sync_to`**: Never use arbitrary `self.wait(5)` in audio mode; always synchronize with `sync_to(marker["start"])` or specific word timestamps.
2. **Recheck Audio Sync Before Rendering**: Cross-reference every visual trigger against the actual Whisper segment/word timestamps in `timing.json`.
3. **Proper Screen Centering & Multi-Column Alignment**: Center titles and main elements (`.set_x(0)`). Align multi-column layouts to consistent horizontal guides.
4. **Explicit Mobject Cleanup**: Any transient helper mobjects (`p1`, `p2`, indicators, temporary labels) must be explicitly faded out in `FadeOut(...)`. Never leave particles or callout text lingering on screen across scene changes.
5. **No Drift**: Ensure `run_time` of animations does not exceed the gap between timestamps (`target_time - current_time`).
6. **Zero AI Slop**: Retain strict 3Blue1Brown standards at all times (pure black canvas, no rounded cards, no top `//` headers, semantic color binding).
