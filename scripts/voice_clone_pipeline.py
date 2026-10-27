"""Qwen3-TTS 0.6B Voice Cloning Pipeline for Manim Explainer Videos."""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

# Path resolution: scripts/ -> root/ -> assets/audio-references/
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
AUDIO_REFS_DIR = SKILL_DIR / "assets" / "audio-references"

SUPPORTED_AUDIO_EXTENSIONS = [".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"]

_MODEL = None


def list_available_voices() -> List[str]:
    """Returns a sorted list of available voice profile names found in assets/audio-references/."""
    if not AUDIO_REFS_DIR.exists():
        return []
    voices = []
    for entry in AUDIO_REFS_DIR.iterdir():
        if entry.is_dir() and not entry.name.startswith("."):
            # Check if directory contains at least one audio file
            audio_files = [f for f in entry.iterdir() if f.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS]
            if audio_files:
                voices.append(entry.name)
    return sorted(voices)


def resolve_voice_reference(voice_name: Optional[str] = None) -> Tuple[Path, str]:
    """
    Resolves the reference audio file path and reference transcript for a given voice name.

    Parameters:
    - voice_name: Name of the subdirectory in assets/audio-references/ (e.g. 'harendra', 'american').

    Returns:
    - (ref_audio_path: Path, ref_text: str)
    """
    available_voices = list_available_voices()
    if not available_voices:
        raise FileNotFoundError(
            f"No voice profiles found in '{AUDIO_REFS_DIR}'. "
            "Please create a folder (e.g. assets/audio-references/<voice_name>/) with "
            "reference_audio.<ext> and reference_text.txt."
        )

    if not voice_name:
        # If not specified, default to first available or prompt
        voice_name = available_voices[0]
        print(f"Notice: No voice specified. Defaulting to '{voice_name}'. (Available: {', '.join(available_voices)})")

    voice_dir = AUDIO_REFS_DIR / voice_name
    if not voice_dir.exists() or not voice_dir.is_dir():
        raise ValueError(
            f"Voice '{voice_name}' not found at '{voice_dir}'. "
            f"Available voice profiles in {AUDIO_REFS_DIR}: {', '.join(available_voices)}"
        )

    # Resolve audio file: look for reference_audio.* first, then any supported audio file
    audio_path = None
    for ext in SUPPORTED_AUDIO_EXTENSIONS:
        candidate = voice_dir / f"reference_audio{ext}"
        if candidate.exists():
            audio_path = candidate
            break

    if not audio_path:
        for file in voice_dir.iterdir():
            if file.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS and not file.name.startswith("."):
                audio_path = file
                break

    if not audio_path or not audio_path.exists():
        raise FileNotFoundError(
            f"No reference audio found in '{voice_dir}'. "
            f"Please place an audio file (e.g. reference_audio.wav, .mp3, .m4a) in that directory."
        )

    # Resolve text transcript
    text_path = voice_dir / "reference_text.txt"
    if not text_path.exists():
        # Check for any .txt file
        txt_files = [f for f in voice_dir.iterdir() if f.suffix.lower() == ".txt" and not f.name.startswith(".")]
        if txt_files:
            text_path = txt_files[0]
        else:
            raise FileNotFoundError(
                f"Reference transcript not found at '{text_path}'. "
                "Please provide reference_text.txt containing the exact transcript of the audio sample."
            )

    ref_text = text_path.read_text(encoding="utf-8").strip()
    if not ref_text:
        raise ValueError(f"Reference text file '{text_path}' is empty.")

    return audio_path, ref_text


def get_qwen3_tts_model(model_name: str = "Qwen/Qwen3-TTS-12Hz-0.6B-Base"):
    """Loads and caches the Qwen3-TTS 0.6B Base model."""
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    import torch
    from qwen_tts import Qwen3TTSModel

    # Determine optimal compute device
    if torch.cuda.is_available():
        device = "cuda:0"
        dtype = torch.bfloat16
    elif torch.backends.mps.is_available():
        device = "mps"
        dtype = torch.float32
    else:
        device = "cpu"
        dtype = torch.float32

    print(f"Loading Qwen3-TTS ({model_name}) on {device} ({dtype})...")
    _MODEL = Qwen3TTSModel.from_pretrained(
        model_name,
        device_map=device,
        dtype=dtype,
    )
    print("✓ Qwen3-TTS Model ready!")
    return _MODEL


def clone_voice(
    text: str,
    output_wav_path: str,
    voice: Optional[str] = None,
    ref_audio_path: Optional[str] = None,
    ref_text: Optional[str] = None,
    language: str = "English",
) -> str:
    """
    Clones the voice from the reference audio and synthesizes the given text.

    Parameters:
    - text: Script text to be spoken
    - output_wav_path: Path where the resulting WAV file will be saved
    - voice: Name of the voice in assets/audio-references/ (e.g. 'harendra', 'american')
    - ref_audio_path: Direct path to reference audio sample (overrides voice parameter)
    - ref_text: Exact transcript of the reference sample (overrides voice parameter)
    - language: Language of the speech (English, Chinese, etc.)
    """
    import soundfile as sf

    # Resolve reference audio and text
    if ref_audio_path and ref_text:
        ref_audio = Path(ref_audio_path)
        resolved_text = ref_text
    elif ref_audio_path and not ref_text:
        ref_audio = Path(ref_audio_path)
        # Attempt to read companion txt
        companion_txt = ref_audio.with_suffix(".txt")
        if companion_txt.exists():
            resolved_text = companion_txt.read_text(encoding="utf-8").strip()
        else:
            raise ValueError(f"ref_text not provided and companion file {companion_txt} not found.")
    else:
        ref_audio, resolved_text = resolve_voice_reference(voice)

    if not ref_audio.exists():
        raise FileNotFoundError(f"Reference audio not found at '{ref_audio}'.")

    model = get_qwen3_tts_model()

    voice_desc = f"'{voice}' ({ref_audio.name})" if voice else f"'{ref_audio.name}'"
    print(f"Synthesizing voice clone with voice {voice_desc} ({len(text)} chars)...")
    wavs, sr = model.generate_voice_clone(
        text=text,
        language=language,
        ref_audio=str(ref_audio),
        ref_text=resolved_text,
    )

    out_path = Path(output_wav_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_path), wavs[0], sr)
    print(f"✓ Cloned audio saved to {out_path} (Sample rate: {sr}Hz)")
    return str(out_path)


def synthesize_video_scenes(
    scenes: List[Dict[str, str]],
    output_dir: str,
    voice: Optional[str] = None,
    ref_audio_path: Optional[str] = None,
    ref_text: Optional[str] = None,
    language: str = "English",
) -> List[Dict[str, Any]]:
    """
    Synthesizes narration for all scenes in a Manim video script using cloned voice.

    Parameters:
    - scenes: List of dicts, e.g. [{"id": "scene1", "text": "Welcome to this deep dive..."}, ...]
    - output_dir: Directory to store generated audio files
    - voice: Name of the voice profile directory in assets/audio-references/ (e.g. 'harendra', 'american')
    - ref_audio_path: Optional direct path to reference audio
    - ref_text: Optional direct transcript string
    - language: Speech language
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for sc in scenes:
        scene_id = sc.get("id", f"scene_{len(results)+1}")
        text = sc["text"]
        out_wav = out_dir / f"{scene_id}_narration.wav"

        clone_voice(
            text=text,
            output_wav_path=str(out_wav),
            voice=voice,
            ref_audio_path=ref_audio_path,
            ref_text=ref_text,
            language=language,
        )
        results.append({
            "id": scene_id,
            "text": text,
            "audio_path": str(out_wav)
        })

    return results


def parse_args():
    parser = argparse.ArgumentParser(
        description="Qwen3-TTS 0.6B Voice Cloning CLI for Manim Explainer Videos"
    )
    parser.add_argument(
        "-v", "--voice",
        dest="voice",
        type=str,
        default=None,
        help="Name of the voice profile directory in assets/audio-references/ (e.g., 'american', 'harendra')"
    )
    parser.add_argument(
        "-t", "--text",
        dest="text",
        type=str,
        default=None,
        help="Narration text string to synthesize"
    )
    parser.add_argument(
        "positional_text",
        nargs="?",
        default=None,
        help="Positional narration text (if --text is not specified)"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output",
        type=str,
        default="voice/cloned_voice.wav",
        help="Path for output audio file (default: voice/cloned_voice.wav)"
    )
    parser.add_argument(
        "-s", "--scenes",
        dest="scenes",
        type=str,
        default=None,
        help="Path to JSON file containing scenes list: [{'id': 'scene_1', 'text': '...'}]"
    )
    parser.add_argument(
        "-d", "--output-dir",
        dest="output_dir",
        type=str,
        default="voice",
        help="Output directory for scene batch audio synthesis (default: voice)"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="English",
        help="Language for speech synthesis (default: English)"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List all available voice profiles in assets/audio-references/ and exit"
    )
    parser.add_argument(
        "--ref-audio",
        type=str,
        default=None,
        help="Direct path to reference audio file (overrides --voice)"
    )
    parser.add_argument(
        "--ref-text",
        type=str,
        default=None,
        help="Direct reference transcript (overrides --voice)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.list_voices:
        voices = list_available_voices()
        if voices:
            print("Available Voice Profiles in assets/audio-references/:")
            for v in voices:
                ref_audio, _ = resolve_voice_reference(v)
                print(f"  • {v} (Audio: {ref_audio.name})")
        else:
            print(f"No voice profiles found in {AUDIO_REFS_DIR}.")
        sys.exit(0)

    # Multi-scene batch synthesis
    if args.scenes:
        scenes_path = Path(args.scenes)
        if not scenes_path.exists():
            print(f"Error: Scenes JSON file '{scenes_path}' does not exist.", file=sys.stderr)
            sys.exit(1)
        with open(scenes_path, "r", encoding="utf-8") as f:
            scenes_data = json.load(f)
        if not isinstance(scenes_data, list):
            print("Error: Scenes JSON must contain a list of scene objects.", file=sys.stderr)
            sys.exit(1)

        print(f"Synthesizing {len(scenes_data)} scenes with voice: '{args.voice or 'default'}'...")
        synthesize_video_scenes(
            scenes=scenes_data,
            output_dir=args.output_dir,
            voice=args.voice,
            ref_audio_path=args.ref_audio,
            ref_text=args.ref_text,
            language=args.language,
        )
        print("✓ All scenes synthesized successfully!")
        sys.exit(0)

    # Single text synthesis
    text_to_speak = args.text or args.positional_text
    if text_to_speak:
        clone_voice(
            text=text_to_speak,
            output_wav_path=args.output,
            voice=args.voice,
            ref_audio_path=args.ref_audio,
            ref_text=args.ref_text,
            language=args.language,
        )
    else:
        print("Error: No text or scenes provided to synthesize.", file=sys.stderr)
        print("Usage examples:")
        print("  python scripts/voice_clone_pipeline.py --list-voices")
        print("  python scripts/voice_clone_pipeline.py --voice harendra --text 'Hello world' --output voice/intro.wav")
        print("  python scripts/voice_clone_pipeline.py --voice american --scenes scenes.json --output-dir voice/")
        sys.exit(1)
