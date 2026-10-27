# Elite YouTube Explainer & Masterclass Workflow

This guide establishes the mandatory end-to-end production protocol for generating high-retention, YouTube-optimized educational explainer videos using **Manim Community**, **Kokoro ONNX**, and **Faster-Whisper**.

---

## The 6-Phase Production Protocol

Every educational video or explainer request follows this strict 6-phase sequence. **Never skip phases or jump straight to Manim code.**

```
[Phase 0: Intake & Prompting] ──▶ [Phase 1: Script & Storyboard] ──▶ [Phase 2: Mandatory User Review]
                                                                                  │ (User Approves)
                                                                                  ▼
[Phase 5: Audit & Delivery] ◀── [Phase 4: Manim Implementation] ◀── [Phase 3: TTS & Whisper Alignment]
```

---

## Phase 0: Pre-Production Intake & Prompting for Key Details

Before generating any script, audio, or animation code, the agent **MUST** confirm the core production specifications with the user. If any key parameters are unspecified or ambiguous, prompt the user with clear options:

### Key Intake Variables:
1. **Topic & Core Thesis**:
   - What specific concept, architecture, algorithm, or theorem is being explained?
   - What is the single biggest "aha!" moment or counter-intuitive insight the viewer must walk away with?
2. **Target Duration & Depth**:
   - **Quick Explainer / Short (2–3 minutes)**: High-level mental model, rapid pacing, 3–4 scenes.
   - **Standard YouTube Explainer (5–7 minutes)**: Complete conceptual journey, concrete examples, edge cases, 5–7 scenes.
   - **Deep-Dive Masterclass (8–12+ minutes)**: Exhaustive architectural/mathematical deconstruction, wire-level inspections, failure modes, trade-offs, 8–10 scenes.
3. **Target Audience & Tone**:
   - Target level: Junior / Student vs. Senior / Staff Engineer.
   - Tone: Energetic, intellectually stimulating, punchy, conversational (caliber of *3Blue1Brown*, *Veritasium*, *Fireship*, *ByteByteGo*). Zero academic stiffness or corporate jargon.
4. **Visual Direction & Animation Priorities**:
   - 3Blue1Brown pure black canvas (`#000000`).
   - What diagrams are central? (e.g., live packet flows, network topologies, coordinate transforms, dynamic JSON/code wire boxes, state machines).
5. **Narration Voice & Audio Persona**:
   - Kokoro ONNX voice: `af_bella` (crisp, modern, high-engagement YouTube tone) or `am_michael` (authoritative, deep, professorial tone).
   - Target speed: `0.98x` (deliberate, relaxed pacing allowing complex visuals to breathe).

---

## Phase 1: Expert YouTube Scriptwriting & Visual Storyboarding

The agent acts as an **Elite YouTube Explainer Scriptwriter and Creative Director**.

The complete production script must be saved to a dedicated file:
`scripts/<Topic_Name>_YouTube_Script.md`

### 1. High-Retention Narrative Structure (The Hook-to-Synthesis Arc)
- **Scene 1: The Cold Open & The Counter-Intuitive Hook (0:00 - 0:45)**:
  - *Never* start with "Hello guys, welcome back..." or "Today we will learn...".
  - Open with a jarring contradiction, a widespread industry misconception, or an intriguing failure mode (e.g., *"Almost every backend engineer has built scalable REST APIs on their resume. And almost every single one of them is lying."*).
- **Scene 2: The Core Thesis & Governing Intuition (0:45 - 1:30)**:
  - Establish the fundamental problem the concept was invented to solve. Why does this exist? What catastrophic failure happens without it?
- **Scenes 3 to N-1: Progressive Deconstructions & Concrete Scenarios**:
  - Break down principles, mechanics, or proofs one by one.
  - Pair every abstract concept with a concrete visual counterpart (e.g., live network topology, code wire inspection, coordinate morph).
  - Explicitly contrast "The Wrong / Naive Way" vs. "The Scalable / Rigorous Way".
- **Final Scene: Architectural Equilibrium & The 3 Golden Rules**:
  - Synthesize all principles into a memorable mental model or 3 actionable questions.
  - Punchy, high-impact concluding remark.

### 2. Mandatory Tri-Fold Storyboard Table Format
Every scene in `scripts/<Topic_Name>_YouTube_Script.md` must be written in this structured format:

| Column | Description & Contents |
| :--- | :--- |
| **Scene & Timing** | Scene Number, Descriptive Title, and Estimated Time Range (e.g. `Scene 1: The Cold Open [00:00 - 00:43]`). |
| **Visual Direction (Manim Animations)** | Explicit visual storyboard: exact mobjects, coordinate positions, semantic colors (`CLR_BLUE`, `CLR_GREEN`, etc.), entrance animations, live packet flow vectors, circumscribe highlights, and camera focus. |
| **Spoken Narration (Script for the Ear)** | High-retention narration text: short sentences, active verbs, rhythmic pacing, phonetically natural phrasing. |
| **Sound Design & SFX Cues** | Cinematic sound cues: `[Deep Sub-bass Drop]`, `[Digital Packet Whoosh]`, `[Impact Thud]`, `[Neon Ping]`, `[Tape Stop]`. |

---

## Phase 2: Mandatory User Review & Alignment (Crucial Gate)

⚠️ **STOP AND PRESENT THE SCRIPT**:
Before writing any Manim code, generating audio, or running rendering pipelines, the agent **MUST** present the script file to the user and ask for review:

> "I have created the complete production script and scene-by-scene visual storyboard at `scripts/<Topic_Name>_YouTube_Script.md`.
> Please review the narration pacing, visual directions, and scene structure. Would you like to adjust any explanations, animations, or scene durations before we proceed with studio narration and Manim rendering?"

**The agent must wait for user feedback or approval.** Once approved, proceed to Phase 3.

---

## Phase 3: Studio Narration Synthesis & Faster-Whisper Alignment

Once the script is approved:

1. **TTS Synthesis (`generate_audio.py`)**:
   - Use Kokoro ONNX (`af_bella` or `am_michael` @ `0.98x`).
   - Add 0.6s lead-in and 1.0s scene transition silence buffers.
2. **Audio Engineering**:
   - 4th-order Butterworth high-pass filter at 80Hz (eliminates sub-bass rumble).
   - Peak normalization to `-1.0 dB` (guarantees YouTube broadcast loudness without clipping).
3. **Word-Level Alignment**:
   - Run Faster-Whisper (`model_size="base"` or `"small"`).
   - Export `timing.json` with exact start/end timestamps for every scene, segment, and key phrase.

---

## Phase 4: High-Density Manim Scene Implementation

Implement the scene in `anim/scenes/<topic>.py` adhering strictly to 3Blue1Brown visual craft:

1. **Pure Black Canvas**: `config.background_color = BLACK` (`#000000`).
2. **Safe 16:9 Bounds**: Keep all elements within `x ∈ [-6.4, +6.4]` and `y ∈ [-3.5, +3.5]`.
3. **Programmatic Indentation for Code Boxes**:
   - Never rely on raw spaces in `Text` (Cairo/Pango collapses whitespace).
   - Use `make_wire_box()` with explicit `shift(RIGHT * indent * step)` and invisible spacer lines `Text("|").set_opacity(0)` on empty lines.
4. **Precision Audio Synchronization**:
   - Embed audio via `self.add_sound(AUDIO_PATH)`.
   - Maintain `current_time` and use `sync_to(target_time)` before every visual beat.
   - Use `play_sync(*anims, run_time=..., **kwargs)` to advance the timeline accurately.
5. **Zero Dead Screen Time**:
   - Keep visuals alive: moving packet dots, dynamic arrows, morphing equations, pulsing indicators.

---

## Phase 5: Verification, Rendering & Quality Audit

Before presenting the final video to the user:

1. **Timeline Monotonicity Check**:
   - Run an automated check to verify `target_time >= current_time` for all `sync_to()` calls.
2. **Dry-Run Validation**:
   - Run `manim -s <scene_file>.py <SceneClass>` to verify all 100+ animations and mobjects compile without errors.
3. **Full 1080p 30fps Video Render**:
   - Run Manim render in background task.
   - Multiplex with AAC stereo audio track.
4. **Frame Snapshot Visual Audit**:
   - Extract snapshot PNGs across every key scene using `ffmpeg`.
   - Inspect snapshots with `view_file` to confirm typography, centering at `x = 0`, contrast, and zero edge-clipping.
5. **Final Delivery**:
   - Present clickable file links, audio specifications, and a scene-by-scene timestamp navigation index.
