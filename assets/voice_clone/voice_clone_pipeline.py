"""Qwen3-TTS 0.6B Voice Cloning Pipeline for Manim Explainer Videos."""

import os
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

SKILL_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_REF_AUDIO = Path(__file__).resolve().parent / "reference_audio.mp3"
DEFAULT_REF_TEXT = Path(__file__).resolve().parent / "reference_text.txt"

_MODEL = None


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
    ref_audio_path: Optional[str] = None,
    ref_text: Optional[str] = None,
    language: str = "English",
) -> str:
    """
    Clones the voice from the reference audio and synthesizes the given text.

    Parameters:
    - text: Script text to be spoken
    - output_wav_path: Path where the resulting WAV file will be saved
    - ref_audio_path: Path to user's 3-10s reference audio sample (defaults to assets/voice_clone/reference_audio.wav)
    - ref_text: Exact transcript of the reference sample (defaults to reading assets/voice_clone/reference_text.txt)
    - language: Language of the speech (English, Chinese, etc.)
    """
    import soundfile as sf

    # Resolve reference audio
    ref_audio = Path(ref_audio_path) if ref_audio_path else DEFAULT_REF_AUDIO
    if not ref_audio.exists():
        raise FileNotFoundError(
            f"Reference audio not found at '{ref_audio}'. "
            "Please provide a 3-10s voice recording at assets/voice_clone/reference_audio.wav"
        )

    # Resolve reference text
    if not ref_text:
        if DEFAULT_REF_TEXT.exists():
            ref_text = DEFAULT_REF_TEXT.read_text(encoding="utf-8").strip()
        else:
            raise ValueError(
                "Reference text missing. Provide ref_text parameter or create "
                "assets/voice_clone/reference_text.txt with the exact transcript."
            )

    model = get_qwen3_tts_model()

    print(f"Synthesizing voice clone ({len(text)} chars)...")
    wavs, sr = model.generate_voice_clone(
        text=text,
        language=language,
        ref_audio=str(ref_audio),
        ref_text=ref_text,
    )

    out_path = Path(output_wav_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_path), wavs[0], sr)
    print(f"✓ Cloned audio saved to {out_path} (Sample rate: {sr}Hz)")
    return str(out_path)


def synthesize_video_scenes(
    scenes: List[Dict[str, str]],
    output_dir: str,
    ref_audio_path: Optional[str] = None,
    ref_text: Optional[str] = None,
    language: str = "English",
) -> List[Dict[str, Any]]:
    """
    Synthesizes narration for all scenes in a Manim video script using cloned voice.

    Parameters:
    - scenes: List of dicts, e.g. [{"id": "scene1", "text": "Welcome to this deep dive..."}, ...]
    - output_dir: Directory to store generated audio files
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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_text = sys.argv[1]
        out = "test_cloned_voice.wav"
        clone_voice(test_text, out)
    else:
        print("Usage: python voice_clone_pipeline.py '<text to speak>'")
