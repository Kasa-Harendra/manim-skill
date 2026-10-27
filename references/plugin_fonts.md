# manim-fonts Plugin Reference Guide

`manim-fonts` enables on-the-fly downloading, caching, and runtime registration of Google Fonts for Manim. It guarantees identical typographic fidelity across different developer machines, operating systems (macOS, Linux, Windows), and CI/headless render pipelines without manual OS font installation.

- **Repository**: [https://github.com/naveen521kk/manim-fonts](https://github.com/naveen521kk/manim-fonts)
- **Author**: Naveen M K
- **Package**: `manim-fonts`
- **Import Namespace**: `manim_fonts`

---

## 1. Installation & Setup

```bash
pip install manim-fonts
```

Import in your script:
```python
from manim import *
from manim_fonts import RegisterFont
```

---

## 2. Core API: `RegisterFont`

`RegisterFont` is a Python context manager that takes a font family name available on Google Fonts (e.g., `"Poppins"`, `"Inter"`, `"JetBrains Mono"`, `"Fira Code"`, `"Cinzel"`, `"Roboto Mono"`):

```python
with RegisterFont("Poppins") as fonts:
    # fonts is a list of registered font names, e.g. ['Poppins', 'Poppins-Bold']
    title = Text("Hello World", font=fonts[0])
    self.play(Write(title))
```

### How It Works Under the Hood
1. Checks the local cache (`~/.cache/manim_fonts`). If not cached, downloads the TTF bundle from Google Fonts.
2. Dynamically registers the TTF files with the system font backend via `manimpango.register_font()`.
3. Yields the verified font family names.
4. Cleanly unregisters the fonts upon context exit.

---

## 3. Production Recipes

### Recipe 1: Custom Editorial Header with Editorial Typography

```python
from manim import *
from manim_fonts import RegisterFont

class CustomTypographyScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Register Google Fonts dynamically
        with RegisterFont("Cinzel") as editorial_fonts:
            title = Text(
                "ARCHITECTURAL EQUILIBRIUM",
                font=editorial_fonts[0],
                font_size=36,
                color=GOLD_A
            ).to_edge(UP, buff=0.8)

            subtitle = Text(
                "Phase 1: Foundations of Distributed Consensus",
                font=editorial_fonts[0],
                font_size=18,
                color=GRAY_B
            ).next_to(title, DOWN, buff=0.25)

            self.play(FadeIn(title, shift=DOWN * 0.3), FadeIn(subtitle), run_time=1.5)
            self.wait(1)

        # Monospace font for technical breakdown
        with RegisterFont("Fira Code") as mono_fonts:
            code_label = Text(
                "raft_cluster.election_timeout_ms = 150",
                font=mono_fonts[0],
                font_size=20,
                color=TEAL_C
            ).shift(DOWN * 0.5)

            self.play(Write(code_label), run_time=1.2)
            self.wait(1)
```

---

## 4. Best Practices & Font Recommendations

1. **Hierarchy Matching with `design.md`**:
   - **Editorial Titles / Math Headings**: `"Inter"`, `"Poppins"`, or `"Cinzel"` (for classical / architectural depth).
   - **Code & Network Wire Inspection**: `"JetBrains Mono"` or `"Fira Code"`.
   - **Clean Technical Body**: `"Roboto"` or `"Open Sans"`.
2. **Scoping**: When creating multi-scene videos or functions, wrap the entire `construct()` body or helper builders in `with RegisterFont(...)` to maintain consistent font family availability throughout the render.
3. **Offline Caching**: Once downloaded, fonts reside in the cache. Subsequent renders do not require network calls, making it ideal for offline high-resolution exports.
