# Audio References Directory (`assets/audio-references/`)

This directory stores reference audio recordings and transcripts for **Qwen3-TTS 0.6B Voice Cloning**.

Each human voice or accent profile is organized into its own subfolder within `assets/audio-references/`.

---

## Directory Structure

```
assets/audio-references/
├── american/
│   ├── reference_audio.mp3       # 3–10s audio sample (.wav, .mp3, .m4a supported)
│   └── reference_text.txt        # Exact transcript of the reference sample
└── harendra/
    ├── reference_audio.m4a       # 3–10s audio sample
    └── reference_text.txt        # Exact transcript of the reference sample
```

---

## Adding a New Voice or Accent

To add a new speaker or accent:

1. **Create a new folder** named after the person or accent (e.g., `assets/audio-references/sarah/` or `assets/audio-references/british/`).
2. **Add a 3–10 second voice recording**:
   - Save as `reference_audio.wav`, `reference_audio.mp3`, or `reference_audio.m4a`.
   - Audio should be clean and recorded in a quiet room at natural presenting speed.
3. **Add the exact transcript**:
   - Save as `reference_text.txt`.
   - Ensure the text matches every spoken word in the audio clip verbatim.

---

## Command Line Usage

Use the voice name as the `--voice` / `-v` argument:

```bash
# List all registered voices
python scripts/voice_clone_pipeline.py --list-voices

# Synthesize a single sentence with a specific voice
python scripts/voice_clone_pipeline.py --voice harendra --text "Welcome to this deep dive into neural networks." --output voice/scene1.wav

# Batch synthesize scenes for a video
python scripts/voice_clone_pipeline.py --voice american --scenes scripts/scenes.json --output-dir voice/
```

> 🔒 **Privacy Guarantee**: All `reference_audio*` and `reference_text*` files in `assets/` are excluded by `.gitignore` so personal voice samples and transcripts are never committed to public repositories.
