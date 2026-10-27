# manim-progress-bar Plugin Reference Guide

`manim-progress-bar` provides customizable, multi-angle progress bar mobjects for Manim. It is used for video timeline scrubbers, chapter indicators, and process completion bars with automatic timing and percentage readouts.

- **Repository**: [https://github.com/zhangzk-code/manim-progress-bar](https://github.com/zhangzk-code/manim-progress-bar)
- **Author**: zhangzk-code
- **Package**: `manim-progress-bar`
- **Import Namespace**: `manim_progress_bar.progress_bar` (or `manim_progress_bar`)

---

## 1. Installation & Setup

```bash
pip install manim-progress-bar
```

Import in your script:
```python
from manim import *
from manim_progress_bar.progress_bar import ProgressBar
```

---

## 2. Core API: `ProgressBar`

```python
progress = ProgressBar(
    width=10,                      # float: Total bar length
    height=0.3,                    # float: Bar thickness
    position=DOWN * 3.5,           # np.array: Screen coordinates
    fill_color=BLUE_C,             # Color: Active fill color
    background_color="#222222",    # Color: Empty track background
    border_color=WHITE,            # Color: Border stroke
    border_width=2.0,              # float: Stroke thickness
    corner_radius=0.1,             # float: Rounded corners
    show_percentage=True,          # bool: Display dynamic % readout
    percentage_font_size=20,       # int: Text scale
    percentage_color=WHITE,        # Color: Readout text color
    angle=0,                       # float: Orientation in degrees (0=horizontal, 90=vertical)
    duration=10.0                  # float: Total duration in seconds for auto-progress
)
```

### Key Methods
- `bar.start()`: Automatically animates from `0%` to `100%` over the initialized `duration`.
- `bar.auto_progress(duration=5.0)`: Advances from `0%` to `100%` over a specified duration in seconds.
- `bar.set_progress(target=0.75, run_time=1.5)`: Animates progress to a specific fraction (`0.0` to `1.0`).
- `bar.update_progress_instant(0.5)`: Instantly sets the progress without an animation transition.

---

## 3. Production Recipes

### Recipe 1: YouTube Chapter Scrubber (Bottom Safe Edge)

Places an unobtrusive, sleek progress indicator at the bottom edge of an explainer video:

```python
from manim import *
from manim_progress_bar.progress_bar import ProgressBar

class VideoScrubberScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Chapter scrubber along bottom safe margin (y = -3.6)
        scrubber = ProgressBar(
            width=13.0,
            height=0.08,
            position=DOWN * 3.65,
            fill_color=RED_C,
            background_color="#1a1a1a",
            border_width=0,
            corner_radius=0.04,
            show_percentage=False,
            duration=12.0
        )
        self.add(scrubber)

        # Start background timer progression
        self.play(scrubber.start(), run_time=12.0)
```

---

### Recipe 2: Multi-Stage Pipeline Progress

```python
from manim import *
from manim_progress_bar.progress_bar import ProgressBar

class PipelineStatusScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"\textbf{Data Pipeline Ingestion}", font_size=32).to_edge(UP, buff=0.8)
        self.add(title)

        bar = ProgressBar(
            width=8.0,
            height=0.4,
            position=ORIGIN,
            fill_color=TEAL_C,
            background_color="#222222",
            border_color=GRAY_C,
            border_width=1.5,
            show_percentage=True,
            percentage_font_size=24
        )
        self.play(FadeIn(bar))
        self.wait(0.5)

        # Stage 1: Extraction (0% -> 35%)
        stage1_label = Text("Extracting raw metrics...", font_size=18, color=GRAY_A).next_to(bar, UP, buff=0.3)
        self.play(FadeIn(stage1_label))
        self.play(bar.set_progress(0.35, run_time=1.5))
        self.wait(0.5)

        # Stage 2: Transformation (35% -> 80%)
        stage2_label = Text("Transforming tensor embeddings...", font_size=18, color=GRAY_A).next_to(bar, UP, buff=0.3)
        self.play(Transform(stage1_label, stage2_label))
        self.play(bar.set_progress(0.80, run_time=2.0))
        self.wait(0.5)

        # Stage 3: Load (80% -> 100%)
        stage3_label = Text("Ingestion complete!", font_size=18, color=GREEN_C).next_to(bar, UP, buff=0.3)
        self.play(Transform(stage1_label, stage3_label))
        self.play(bar.set_progress(1.00, run_time=1.0))
        self.play(Flash(bar, color=GREEN_A))
        self.wait(1.5)
```

---

## 4. Best Practices

1. **No Redundant `run_time`**: When calling `bar.auto_progress(duration=5.0)` or `bar.start()`, do not pass a conflicting `run_time` into `self.play(...)` as it inherits the configured duration automatically.
2. **Safe Margins**: For bottom-edge scrubbers, use `y = -3.65` and `width <= 13.0` to keep within the standard Manim 16:9 safe zone (`y ∈ [-3.5, +3.5]`).
