---
name: manim
description: Comprehensive guide for Manim Community - Python framework for creating highly animated, detailed mathematical and technical explainer videos in the 3Blue1Brown visual craft. Enforces an elite YouTube explainer workflow: mandatory pre-production user intake prompts (duration, topic, tone), script-first tri-fold storyboarding with explicit scene animations, mandatory user review gates, Kokoro studio audio sync, and anti-AI-slop design.
license: MIT
version: 1.0.0
author: manim-community
repo: https://github.com/ManimCommunity/manim
tags:
  - Video
  - Python
  - Animation
  - Manim
  - Mathematical
  - Educational
  - Visualization
  - LaTeX
  - 3Blue1Brown
  - Astronomy
  - Astrophysics
  - Automata
  - Data-Structures
  - Circuits
  - Engineering
  - FontAwesome
  - Typography
  - Meshes
  - Computer-Science
  - Machine-Learning
  - Neural-Networks
  - Transformers
  - LLMs
  - Physics
  - Optics
  - TikZ
  - Chemistry
  - Molecular
  - Brand-Icons
  - AI-Assets
dependencies:
  - manim>=0.19.0
  - python>=3.11
  - manim-brand-icons>=0.1.0
  - simplepycons>=1.16.0
  - cairosvg>=2.7.0
  - manim-Astronomy>=0.0.5
  - manim-automata>=0.2.11
  - manim-data-structures>=0.1.7
  - manim-eng
  - manim-fontawesome>=0.1.0
  - manim-fonts>=0.1.0
  - manim-meshes>=0.1.0
  - manim-neural-network>=0.1.0
  - manim-onlinetex>=0.1.0
  - manim-physics>=0.2.4
  - manim-progress-bar>=0.2.0
  - manim-tikz>=0.1.0
  - manim-weighted-line>=0.1.0
  - chanim>=0.1.0
  - llmanim>=0.1.0
  - vedo
  - trimesh
  - pymunk
  - networkx
  - requests
metadata:
  mcpmarket-version: 1.0.0
---
# Manim Community - Mathematical Animation Engine

Comprehensive skill set for creating rich, highly animated mathematical visualizations using Manim Community, faithfully adhering to the visual craftsmanship of 3Blue1Brown (pure black canvas, continuous transformations, semantic color binding, dynamic updaters, and zero AI slop).

## When to use

Use this skill whenever you are dealing with Manim code to obtain domain-specific knowledge about:

- Creating mathematical animations and visualizations
- Building educational video content programmatically
- Working with geometric shapes and transformations
- Animating LaTeX equations and mathematical formulas
- Creating graphs, charts, and coordinate systems
- Implementing scene-based animation sequences
- Rendering high-quality mathematical diagrams
- Building explanatory visual content for teaching
- Visualizing astronomical bodies, orbital mechanics, and Kepler's laws (`manim-Astronomy`)
- Animating General Relativity, spacetime fabric curvature, and gravitational waves (`manim-Astronomy`)
- Simulating Finite State Machines (FSM), DFA, NFA, and Pushdown Automata from JFLAP (`manim-automata`)
- Animating computer science data structures: memory arrays, sliding windows, and pointers (`manim-data-structures`)
- Drawing and animating engineering circuit schematics, resistors, capacitors, and node currents (`manim-eng`)
- Embedding scalable Font Awesome vector icons for systems and cloud architecture diagrams (`manim-fontawesome`)
- Loading Google Fonts dynamically on-the-fly for guaranteed cross-platform typography (`manim-fonts`)
- Visualizing 3D surface meshes, polyhedral topologies, Delaunay triangulations, and Voronoi duals (`manim-meshes`)
- Visualizing neural networks, multi-layer perceptrons, and forward-pass pulses (`manim-neural-network`)
- Rendering LaTeX formulas in headless / minimal environments without local TeX Live (`manim-onlinetex`)
- Simulating 2D rigid-body mechanics, electromagnetism, lenses/ray tracing, and waves (`manim-physics`)
- Rendering video timeline scrubbers, chapter indicators, and multi-angle progress bars (`manim-progress-bar`)
- Compiling LaTeX TikZ graphics, trees, and commutative diagrams into vector mobjects (`manim-tikz`)
- Building weighted network graphs for routing and graph algorithms with NetworkX (`manim-weighted-line`)
- Animating organic chemistry skeletal structures, chemfig formulas, and reaction mechanisms (`chanim`)
- Visualizing LLM & Transformer architectures, token embeddings, QKV self-attention, and Softmax (`LLManim`)
- Displaying AI & ML brand icons, transparent PNGs, and vector logos (`AIIcon`, `BrandIcon`, `manim-brand-icons`, `simplepycons`)

## Core Concepts

Manim allows you to create animations using:
- **Scenes**: Canvas for your animations where you orchestrate mobjects
- **Mobjects**: Mathematical objects that can be displayed (shapes, text, equations)
- **Animations**: Transformations applied to mobjects (Write, Create, Transform, FadeIn)
- **Transforms**: Morphing between different states of mobjects
- **LaTeX Integration**: Native support for rendering mathematical notation
- **Python Simplicity**: Use Python to programmatically specify animation behavior

## Key Features

- Precise mathematical object positioning and transformations
- Native LaTeX rendering for equations and formulas
- Extensive shape library (circles, rectangles, arrows, polygons)
- Coordinate systems and function graphing
- Boolean operations on geometric shapes
- Camera controls and scene management
- High-quality video rendering
- IPython/Jupyter notebook integration
- VS Code extension with live preview

## Operational Modes

This skill supports two distinct production modes:

1. **Mode 1: Only Animation (Silent / Visual Math)**:
   - For standalone mathematical proofs, geometric visualizations, algorithm walkthroughs, and silent animations.
   - Pacing is guided purely by mathematical clarity (`rate_func=smooth`, calibrated `self.wait(...)`).
   - Requires no audio files or timing JSON.

2. **Mode 2: Audio + Animation (The YouTube Explainer & Masterclass Pipeline)**:
   - For high-retention educational YouTube videos, system architecture deep dives, tutorials, and lecture series.
   - Follows the mandatory 6-phase protocol: **Intake Prompting ➔ Script & Scene Storyboarding ➔ User Review Gate ➔ Studio TTS & Alignment ➔ Manim Choreography ➔ Render & Visual Audit**.
   - Complete guide and templates: **[references/youtube_explainer_workflow.md](references/youtube_explainer_workflow.md)**.

---

## The YouTube Explainer Protocol (Mandatory Workflow for Videos & Explainers)

When asked to create an educational video, tutorial, or explainer using Manim, **NEVER jump straight to code or audio generation**. Follow this strict phased protocol:

### Phase 0: Pre-Production Intake & Prompting for Key Details (MANDATORY GATEWAY)
Before writing any script or code, **prompt the user** for key production variables (or confirm any missing parameters if partially specified):
1. **Topic & Core Thesis**: Exactly what concept, architecture, algorithm, or theorem is being explained? What is the single biggest "aha!" takeaway?
2. **Target Duration & Depth**:
   - *Quick Explainer / Short (2–3 mins)*: High-level mental model, rapid pacing, 3–4 scenes.
   - *Standard YouTube Explainer (5–7 mins)*: Complete conceptual journey, concrete examples, edge cases, 5–7 scenes.
   - *Deep-Dive Masterclass (8–12+ mins)*: Exhaustive architectural/mathematical deconstruction, wire-level inspections, failure modes, trade-offs, 8–10 scenes.
3. **Target Audience & Tone**: Junior / Student vs. Senior / Staff Engineer; high-energy, punchy, conversational YouTuber storytelling (caliber of *3Blue1Brown*, *Veritasium*, *Fireship*).
4. **Visual Style & Animation Priorities**: Pure black canvas (`#000000`), dynamic network packet flows, code wire-inspection boxes, coordinate transforms, etc.
5. **Narration Voice & Audio**: Kokoro voice (`af_bella` crisp modern YouTube tone, or `am_michael` authoritative professorial tone) at `0.98x` pacing.

### Phase 1: Expert YouTuber Scriptwriting & Scene Storyboard
The agent acts as an **Elite YouTube Explainer Scriptwriter and Director**:
- Write and save the complete production script to: `scripts/<Topic_Name>_YouTube_Script.md`.
- **Narrative Arc**:
  - *Scene 1: The Cold Open & The Counter-Intuitive Hook* (First 30–45s: break a common myth, expose a lie, or present an intriguing paradox).
  - *Scene 2: The Core Thesis / Governing Intuition* (Why was this invented? What catastrophic failure happens without it?).
  - *Scenes 3 to N-1: Systematic Deconstructions* (Side-by-side contrasts, failure modes vs solutions, live wire/code inspection).
  - *Final Scene: Architectural Equilibrium & The 3 Golden Rules* (Memorable mental model, actionable takeaways).
- **Mandatory Tri-Fold Table Structure per Scene**:
  - `Scene & Timing Range`
  - `Visual Direction & Scene Animations` (Explicit Manim mobjects, layouts, flows, colors, highlights)
  - `Spoken Narration` (Punchy, conversational, written for the ear)
  - `Sound Design & SFX Cues` (`[Whoosh]`, `[Digital Packet Pulse]`, `[Impact Thud]`, `[Sub-bass Drop]`)

### Phase 2: Mandatory User Review Gate (CRITICAL STOPPING POINT)
⚠️ **DO NOT PROCEED AUTOMATICALLY TO CODE OR AUDIO**:
Present the script file `scripts/<Topic_Name>_YouTube_Script.md` to the user and ask for review:
> *"I have crafted the complete YouTube production script and scene-by-scene visual storyboard at `scripts/<Topic_Name>_YouTube_Script.md`. Please review the narration pacing, visual directions, and scene structure. Would you like to adjust any explanations, animations, or scene durations before we proceed with studio narration and Manim rendering?"*
**Wait for the user's review and explicit approval before continuing.**

### Phase 3: Studio Narration Synthesis & Faster-Whisper Alignment
Once approved, run `generate_audio.py` using Kokoro ONNX (`af_bella` or `am_michael` @ `0.98x`), apply 80Hz Butterworth rumble filter + -1.0 dB peak normalization, and extract word-level timestamps with Faster-Whisper into `timing.json`.

### Phase 4: High-Density Manim Scene Implementation
Implement the scene in `anim/scenes/<topic>.py`:
- Pure black canvas (`#000000`).
- Safe margins: `x ∈ [-6.4, +6.4]` and `y ∈ [-3.5, +3.5]`.
- Programmatic indentation for code boxes (`make_wire_box` with `shift(RIGHT * indent * step)` and invisible line spacers).
- Zero dead screen time: continuous motion, dynamic arrows, live packet flows.
- Timestamp-locked orchestration via `sync_to(cue_time)` and `play_sync(*anims, run_time=..., **kwargs)`.

### Phase 5: Verification, Rendering & Quality Audit
- Monotonicity check on `sync_to`.
- Dry-run validation check (`manim -s`).
- Full 1080p 30fps render with embedded AAC audio track.
- Snapshot frame extraction across key scenes using `ffmpeg` and visual audit via `view_file`.
- Final delivery presentation with clickable links, audio metrics, and timestamp index.

---

## How to use

Read individual reference files for detailed explanations and code examples:

### Production Workflows & Visual Standards (Mandatory)
- **[references/youtube_explainer_workflow.md](references/youtube_explainer_workflow.md)** - **The Complete YouTube Explainer & Masterclass Workflow**: The 6-phase protocol from user intake prompts, tri-fold scriptwriting with scene animations, user review gate, to studio sync and audit.
- **[design.md](design.md)** (or **[references/design.md](references/design.md)**) - **STRICT 3Blue1Brown visual aesthetic & anti-AI-slop rules**: bans rounded boxes/containers for simple text, bans top `//` headings, defines screen composition geometry and centering, the 3b1b color palette, updaters, dynamic motion, and camera choreography.
- **[references/audio_sync.md](references/audio_sync.md)** - **Studio audio generation & animation synchronization**: Kokoro ONNX TTS synthesis, Faster-Whisper word-level alignment, timestamp-locked Manim scene orchestration, and pre-render sync audit.
- **[references/voice_cloning_qwen3.md](references/voice_cloning_qwen3.md)** - **Qwen3-TTS 0.6B Voice Cloning**: Zero-shot voice cloning from 3-10s user reference audio (`reference_audio.wav` + `reference_text.txt`) for personalized studio explainer narration.

### Core Concepts & Mechanics
- **[references/scenes.md](references/scenes.md)** - Creating scenes and organizing animations
- **[references/mobjects.md](references/mobjects.md)** - Understanding mathematical objects and shapes
- **[references/animations.md](references/animations.md)** - Core animation types and techniques
- **[references/latex.md](references/latex.md)** - Rendering LaTeX equations and formulas
- **[references/example_gallery.md](references/example_gallery.md)** - **Official Example Gallery Reference**: Best-practice code snippets covering `ManimCELogo`, `BraceAnnotation`, `VectorArrow`, `BooleanOperations`, continuous updaters (`MovingAngle`, `MovingDots`), function plots (`SinAndCosFunctionPlot`, `GraphAreaPlot`), `MovingCameraScene`, `ThreeDScene` surface plots, non-linear coordinate warping, and unit circle sine unfurling.

### Supported Plugins & Domain Extensions
- **[references/plugin_astronomy.md](references/plugin_astronomy.md)** - **`manim-Astronomy`**: Celestial mechanics, particle-based stars (`Star`), planets with ring debris discs (`Planet`), curved 3D spacetime fabrics (`SpaceTimeFabric`), gravitational wave ripples, and orbital simulations.
- **[references/plugin_automata.md](references/plugin_automata.md)** - **`manim-automata`**: Finite State Machines (FSMs), Deterministic/Nondeterministic Finite Automata (DFA/NFA), Pushdown Automata (PDA) loaded from JFLAP XML files with automated string-stepping animations.
- **[references/plugin_data_structures.md](references/plugin_data_structures.md)** - **`manim-data-structures`**: CS data structure visualizations: configurable memory arrays (`MArray`), sub-element animators (`animate_elem_square`, `animate_elem_value`), dynamic pointers (`MArrayPointer`), sliding windows (`MArraySlidingWindow`), and variable cards (`MVariable`).
- **[references/plugin_circuits_eng.md](references/plugin_circuits_eng.md)** - **`manim-eng`**: Engineering and electrical schematic design: Pythonic circuit assembly (`Circuit`), automatic wire routing, components (`Resistor`, `Capacitor`, `Inductor`, `VoltageSource`, `Diode`, `Node`), and animated LaTeX voltage/current annotations.
- **[references/plugin_fontawesome.md](references/plugin_fontawesome.md)** - **`manim-fontawesome`**: Thousands of Font Awesome (v6.5.1) vector icons (`brand`, `solid`, `regular`) accessible as native `SVGMobject` instances for system architecture, cloud networks, and developer tooling diagrams.
- **[references/plugin_fonts.md](references/plugin_fonts.md)** - **`manim-fonts`**: Dynamic on-the-fly Google Fonts downloading, local caching, and temporary font registration (`with RegisterFont("Font Name") as fonts:`) for guaranteed typography across systems and headless renderers.
- **[references/plugin_meshes.md](references/plugin_meshes.md)** - **`manim-meshes`**: 3D surface meshes, polyhedral topologies (`Mesh`), Delaunay triangulation circumcircles, Voronoi dual diagrams, and `trimesh` integration using the OpenGL renderer.
- **[references/plugin_neural_network.md](references/plugin_neural_network.md)** - **`manim-neural-network`**: Multi-layer perceptron neural network mobjects (`NeuralNetworkMobject`), customizable neuron geometry/colors, mathematical layer labeling, and forward signal pulse animations.
- **[references/plugin_onlinetex.md](references/plugin_onlinetex.md)** - **`manim-onlinetex`**: Cloud-backed LaTeX rendering via LaTeXCluster and QuickLaTeX for seamless math rendering in headless Docker or environments without local TeX Live.
- **[references/plugin_physics.md](references/plugin_physics.md)** - **`manim-physics`**: 2D rigid-body mechanics simulation (`SpaceScene`), electrostatics (`Charge`, `ElectricField`), magnetostatics (`Wire`, `MagneticField`), geometric optics (`Lens`, `Ray`), and wave interference (`Wave`).
- **[references/plugin_progress_bar.md](references/plugin_progress_bar.md)** - **`manim-progress-bar`**: Multi-angle progress bars, video scrubber timelines, and staged pipeline progression (`ProgressBar`, `auto_progress()`, `start()`).
- **[references/plugin_tikz.md](references/plugin_tikz.md)** - **`manim-tikz`**: Direct compilation of LaTeX TikZ code into native `SVGMobject` instances (`Tikz`), supporting commutative diagrams, syntax trees, and TikZ libraries.
- **[references/plugin_weighted_line.md](references/plugin_weighted_line.md)** - **`manim-weighted-line`**: Weighted network graph edges (`WeightedLine`) with numeric badges, integrating directly with Manim `Graph` / `DiGraph` and NetworkX.
- **[references/plugin_chanim.md](references/plugin_chanim.md)** - **`chanim`**: Organic chemistry animations, 2D skeletal structures via `chemfig`, molecular labels (`ChemWithName`), and multi-step chemical reaction pathways.
- **[references/plugin_llmanim.md](references/plugin_llmanim.md)** - **`LLManim`**: Large Language Model and Transformer architecture visual components (`TokenRow`, `MatrixBox`, `VectorBar`, `SoftmaxCurve`, QKV attention arcs, and forward pass pulses).
- **[references/plugin_brand_icons.md](references/plugin_brand_icons.md)** - **`manim-brand-icons`**: Brand & AI icon assets: offline access to 3,000+ vector icons via `simplepycons`, pre-bundled 1024x1024 transparent PNGs (ChatGPT, Gemini, Claude, DeepSeek, Meta, HuggingFace, etc.), and Clearbit/Brandfetch dynamic web fetcher (`AIIcon`, `BrandIcon`).
- **[references/better_icons_guide.md](references/better_icons_guide.md)** - **`better-icons`**: Access 200,000+ icons across 150+ collections (Lucide, MDI, Heroicons, Tabler, Phosphor, Font Awesome) with custom `--color` formatting, Antigravity MCP integration, and on-demand SVG/PNG caching for Manim scenes.

#### Plugin Quick Reference & Import Index

| Plugin | Install Command | Primary Import | Key Classes / Objects |
| :--- | :--- | :--- | :--- |
| **`manim-brand-icons`** | `pip install manim-brand-icons simplepycons` | `from manim_brand_icons import AIIcon, BrandIcon` | `AIIcon("gemini")`, `AIIcon("chatgpt", mode="png")` |
| **`better-icons`** | `npx better-icons setup` | `from manim_brand_icons import BrandIcon` | `BrandIcon("lucide:cpu", color="#10A37F")`, `BrandIcon("mdi:database")` |
| **`manim-Astronomy`** | `pip install manim-Astronomy vedo` | `from manim_Astronomy import *` | `Star`, `Planet`, `SpaceTimeFabric`, `HubbleSpaceTelescope` |
| **`manim-automata`** | `pip install manim-automata` | `from manim_automata import *` | `ManimDeterminsticFiniteAutomaton`, `ManimPushDownAutomaton` |
| **`manim-data-structures`** | `pip install manim-data-structures` | `from manim_data_structures import *` | `MArray`, `MArrayPointer`, `MArraySlidingWindow`, `MVariable` |
| **`manim-eng`** | `pip install manim-eng` | `from manim_eng import *` | `Circuit`, `Resistor`, `Capacitor`, `Inductor`, `VoltageSource`, `Node` |
| **`manim-fontawesome`** | `pip install manim-fontawesome` | `from manim_fontawesome import brand, solid, regular` | `brand.<name>`, `solid.<name>`, `regular.<name>` (SVGMobjects) |
| **`manim-fonts`** | `pip install manim-fonts` | `from manim_fonts import RegisterFont` | `with RegisterFont("Poppins") as fonts:` |
| **`manim-meshes`** | `pip install manim-meshes trimesh` | `from manim_meshes.models.manim_models.basic_mesh import ManimMesh` | `ManimMesh`, `TriangleManim2DMesh`, `create_pyramid` |
| **`manim-neural-network`** | `pip install manim-neural-network` | `from manim_neural_network.neural_network import NeuralNetworkMobject` | `NeuralNetworkMobject` |
| **`manim-onlinetex`** | `pip install manim-onlinetex` | `from manim_onlinetex import *` *(after manim)* | Automatic cloud LaTeX compilation |
| **`manim-physics`** | `pip install manim-physics pymunk` | `from manim_physics import *` | `SpaceScene`, `Charge`, `ElectricField`, `Lens`, `Ray`, `Wave` |
| **`manim-progress-bar`** | `pip install manim-progress-bar` | `from manim_progress_bar.progress_bar import ProgressBar` | `ProgressBar`, `auto_progress()`, `start()` |
| **`manim-tikz`** | `pip install manim-tikz` | `from manim_tikz import Tikz` | `Tikz(code, libraries=[...], use_pdf=True)` |
| **`manim-weighted-line`** | `pip install manim-weighted-line networkx` | `from manim_weighted_line import *` | `WeightedLine`, `Graph(..., edge_type=WeightedLine)` |
| **`chanim`** | `pip install chanim` | `from chanim import *` | `ChemObject`, `ChemWithName`, `Reaction` |
| **`llmanim`** | `pip install llmanim` | `from llmanim.base.shapes import MatrixBox, VectorBar, TokenBox` | `TokenRow`, `MatrixBox`, `VectorBar`, `SoftmaxCurve`, `attention_flow` |

For additional topics including transforms, timing, shapes, coordinate systems, 3D animations, camera movement, and advanced features, refer to the comprehensive [Manim Community documentation](https://docs.manim.community/).

## Visual Standards & 3Blue1Brown Aesthetic

Every animation must adhere strictly to the **[design.md](design.md)** specification.

- ❌ **NO Encapsulating Simple Text or Math in Boxes**: Never wrap individual equations, single labels, or definitions in rounded rectangular "cards", pill badges, or bento boxes. Text and formulas must breathe freely on the canvas using natural spatial layout (`VGroup.arrange`), curly braces (`Brace`), underlines, or focus spotlights (`Circumscribe`, `Indicate`).
- ✅ **ALLOWED: Architectural Component Containers**: You MAY use `RoundedRectangle` purposefully to represent higher-level architectural components or functional subsystems (e.g., API Gateway node, Microservice container, Database cluster) that encapsulate multiple internal sub-entities, keeping borders sleek (`stroke_width=1.5`) and opacity subtle.
- ❌ **NO Top `//` Headings**: Never prefix titles with `//` (e.g., `// 01. INTRODUCTION`). Titles must be natural mathematical/conceptual phrases that enter smoothly and yield to the visual intuition.
- ❌ **NO Static Presentation Slides**: Manim is an animation engine, not PowerPoint. Never present bulleted lists, walls of static text, or disconnected slide-to-slide jumps.
- ❌ **NO Arbitrary Neon or Pastel Palettes**: Never use random rainbow gradients, tacky web colors, or muddy dark grays.

### 2. Mandatory Pure Black Background
- **Always set a pure black background** (`BLACK` / `"#000000"`). Avoid muddy or washed-out dark grays. Pure black delivers maximum contrast and the signature cinematic 3Blue1Brown aesthetic:
  ```python
  self.camera.background_color = BLACK  # or config.background_color = BLACK
  ```

### 3. Highly Animated & Continuous Motion (The 3b1b Standard)
- **Continuous Motion**: Drive live geometric shifts using `ValueTracker`, `always_redraw`, and `.add_updater()` rather than jumping between static poses.
- **Semantic Color Binding**: Equations and geometric elements share exact colors (e.g., variable $x$ in `YELLOW_C` matches its tick and span on the axis in `YELLOW_C`).
- **Seamless Algebraic Morphing**: Transform formulas organically using `TransformMatchingTex` and `TransformMatchingShapes`.
- **Dynamic Attention**: Direct focus with `Indicate()`, `Circumscribe()`, `Flash()`, and animated arrows—never box outlines.

### 4. Professional Typography & LaTeX
- **Primary Text**: Clean sans-serif (`"Helvetica Neue"`, `"Inter"`, `"SF Pro Display"`).
- **Code & Notation**: Clean monospace (`"JetBrains Mono"`, `"Fira Code"`, `"Menlo"`).
- **Mathematics**: Native LaTeX via `MathTex` with `substrings_to_isolate` for fine-grained color matching and animation.

### 5. Screen Alignment & Composition Geometry
- **16:9 Viewport Bounds**: Frame width is `14.22`, height is `8.0`. All elements must remain within safe margins `x ∈ [-6.4, +6.4]` and `y ∈ [-3.5, +3.5]`.
- **Center Anchoring**: Titles, single-focus formulas, central diagrams, and summaries must be centered at `x = 0` (`.set_x(0)` or `.move_to([0, y, 0])`).
- **Symmetrical Multi-Column Layouts**: When presenting side-by-side content (e.g., wire code on left, annotations on right), align all left-column elements to a single shared left guide (e.g., `x = -5.8`) and all right-column elements to a shared left guide (e.g., `x = +0.8`) rather than staggered centers. Never allow asymmetric braces to push text off-screen.
- **Table Grid Alignment**: Use mathematically calculated column X-coordinates rather than arbitrary spacing.

### 6. Code Blocks & Programmatic Visual Indentation
- **The Whitespace Collapse Issue**: In Manim, `Text` mobjects use Pango/Cairo. Leading/trailing whitespace glyphs do not generate ink, so their bounding boxes only encompass printable characters. Calling `.arrange(DOWN, aligned_edge=LEFT)` snaps the first printable character of every line to the exact same X coordinate, completely erasing indentation!
- **Mandatory Helper Pattern**: Always construct code blocks (JSON, XML, YAML, Python) with explicit horizontal shifts (`line.shift(RIGHT * indent * 0.45)`) and `t2c` (text-to-color) token syntax highlighting:
  ```python
  def make_code_block(line_specs, base_x=-5.8, base_y=-0.1, font_size=13, buff=0.08, indent_step=0.45):
      lines = [
          (indent, Text(text, font="Menlo", font_size=font_size, color=WHITE, t2c=t2c_dict))
          for indent, text, t2c_dict in line_specs
      ]
      all_lines = VGroup(*[lm for _, lm in lines]).arrange(DOWN, aligned_edge=LEFT, buff=buff)
      for indent, line_mob in lines:
          line_mob.shift(RIGHT * indent * indent_step)
      min_left = min(lm.get_left()[0] for indent, lm in lines if indent == 0)
      all_lines.shift(RIGHT * (base_x - min_left)).set_y(base_y)
      return all_lines
  ```

## Quick Start Example (3Blue1Brown Style)

```python
from manim import *

class TangentIntuition(Scene):
    def construct(self):
        # 1. Mandatory pure black canvas
        self.camera.background_color = BLACK

        # 2. Mathematical title without AI slop (no "//" headings, no container cards)
        title = Tex(r"\textbf{The Derivative as a Moving Tangent}", font_size=38)
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(0.5)

        # 3. Coordinate system and curve
        axes = Axes(
            x_range=[-0.5, 4.5, 1],
            y_range=[-0.5, 5, 1],
            x_length=7,
            y_length=4.5,
            axis_config={"color": LIGHT_GREY, "stroke_width": 2},
        ).to_edge(DOWN, buff=0.8)

        curve = axes.plot(lambda x: 0.25 * x**2 + 0.3, x_range=[0, 4], color=BLUE_C, stroke_width=3.5)
        curve_label = axes.get_graph_label(curve, label=r"f(x) = \frac{1}{4}x^2 + 0.3", x_val=3.6, direction=UR)

        self.play(Create(axes), run_time=1.2)
        self.play(Create(curve), FadeIn(curve_label), run_time=1.5)
        self.wait(0.5)

        # 4. Continuous animation with ValueTracker & always_redraw (3b1b style)
        x_tracker = ValueTracker(1.0)

        # Dynamic point on curve
        dot = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), curve.underlying_function(x_tracker.get_value())),
            color=YELLOW_C,
            radius=0.08
        ))

        # Dynamic tangent line updating live
        tangent = always_redraw(lambda: axes.get_secant_slope_group(
            x_tracker.get_value(),
            curve,
            dx=0.001,
            secant_line_length=3.5,
            secant_line_color=YELLOW_D,
        ))

        # Dynamic derivative readout
        slope_readout = always_redraw(lambda: MathTex(
            r"x = ", f"{x_tracker.get_value():.2f}",
            r",\quad f'(x) = ", f"{0.5 * x_tracker.get_value():.2f}",
            font_size=28
        ).next_to(axes, UP, buff=0.3))

        self.play(FadeIn(dot), Create(tangent), FadeIn(slope_readout))
        self.wait(0.5)

        # Continuous smooth motion showcasing the rate of change
        self.play(x_tracker.animate.set_value(3.5), run_time=3.5, rate_func=smooth)
        self.wait(0.5)
        self.play(x_tracker.animate.set_value(0.5), run_time=3.0, rate_func=smooth)
        self.wait(0.5)

        # Mathematical spotlight highlight (no box container)
        self.play(Circumscribe(slope_readout, color=YELLOW_C, fade_out=True))
        self.wait(1)
```

Render with: `manim -pql script.py TangentIntuition`

## Best Practices

1. **Mandatory Intake Prompting (Phase 0)** - Before writing any script or code, clarify/confirm key parameters with the user: topic/thesis, target duration/depth (Short 2-3m, Standard 5-7m, Masterclass 8-12m), target audience, visual priorities, and voice preference.
2. **Script-First with Tri-Fold Storyboarding (Phase 1)** - Always generate `scripts/<Topic>_YouTube_Script.md` first. Include explicit visual direction with Manim mobjects/flows, spoken narration written for the ear, and sound design SFX cues.
3. **Mandatory User Review Gate (Phase 2)** - STOP and ask the user for review of the script file before generating audio or writing animation code. Never skip this approval checkpoint.
4. **Mandatory Pure Black Background** - Always set `self.camera.background_color = BLACK` (or `config.background_color = BLACK`).
5. **Proper Screen Centering & Multi-Column Alignment** - Anchor titles, formulas, and primary summaries at `x = 0`. In multi-column displays, align left and right columns to consistent horizontal guides (`x_left`, `x_right`) within `[-6.4, +6.4]` safe margins without lopsided staggering or brace edge overflow.
6. **Recheck Audio-Visual Sync Before Rendering (Mode 2)** - Cross-check every animation trigger against the actual Whisper word/segment timestamps in `timing.json` (no estimated guesses). Ensure `current_time + run_time <= next_cue_time` to prevent drift, and inspect representative frame snapshots with `ffmpeg` before final delivery.
7. **Zero AI Slop** - Never encapsulate simple text or plain math in cards/badges; use rounded containers strictly when delineating architectural components/subsystems. Strictly avoid `//` comment headings and slide decks.
8. **Continuous Animation (3b1b Depth)** - Animate smoothly with `ValueTracker`, `always_redraw`, and updater functions rather than static slide cuts.
9. **Semantic Color Coding** - Bind colors in formulas (`MathTex(..., substrings_to_isolate=...)`) directly to geometric curves, axes, and vectors.
10. **Fluid Algebraic Morphs** - Use `TransformMatchingTex` with `path_arc` for natural algebraic derivations.
11. **Attention Directing** - Guide viewer attention with `Indicate`, `Circumscribe`, `Flash`, and moving arrows instead of boxed outlines.
12. **Code Blocks & Guaranteed Indentation** - When rendering code (JSON, YAML, XML, Python), use explicit programmatic horizontal shifts (`indent_step=0.45`) and `t2c` syntax mapping rather than raw leading spaces in strings that `arrange()` collapses.
13. **Read [references/youtube_explainer_workflow.md](references/youtube_explainer_workflow.md) and [design.md](design.md)** - Follow the complete 6-phase YouTube explainer protocol and 12-point pre-render visual checklist.

## Command Line Usage

```bash
# Preview at low quality (fast)
manim -pql script.py SceneName

# Render at high quality
manim -pqh script.py SceneName

# Save last frame as image
manim -s script.py SceneName

# Render multiple scenes
manim script.py Scene1 Scene2
```

## Resources

- **Documentation**: https://docs.manim.community/
- **Repository**: https://github.com/ManimCommunity/manim
- **Examples Gallery**: https://docs.manim.community/en/stable/examples.html
- **Discord Community**: https://www.manim.community/discord/
- **3Blue1Brown Channel**: https://www.youtube.com/c/3blue1brown
- **License**: MIT
