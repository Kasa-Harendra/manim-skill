# manim-tikz Plugin Reference Guide

`manim-tikz` enables Manim Community to compile raw LaTeX TikZ code directly into native `SVGMobject` vector curves. It allows mathematical and technical creators to reuse existing TikZ diagrams (commutative diagrams, trees, Petri nets, automaton graphs, and geometric constructions) seamlessly inside Manim animations.

- **Repository**: [https://github.com/ralphieraccoon/manim-tikz](https://github.com/ralphieraccoon/manim-tikz)
- **Author**: ralphieraccoon
- **Package**: `manim-tikz`
- **Import Namespace**: `manim_tikz`

---

## 1. Installation & Prerequisites

```bash
pip install manim-tikz
```

### System Requirements
Requires a working LaTeX distribution with TikZ (`pgf` / `tikz`). On macOS: `brew install --cask mactex-no-gui` or Ubuntu: `sudo apt install texlive-pictures`.

---

## 2. Core API: `Tikz`

`Tikz` is a subclass of `SVGMobject`:

```python
from manim import *
from manim_tikz import Tikz

tikz_mob = Tikz(
    code=r"\draw[thick, fill=blue!20] (0,0) circle (1.5);",
    packages=[],         # list[str]: Extra LaTeX packages (\usepackage{...})
    libraries=[],        # list[str]: Tikz libraries (\usetikzlibrary{...})
    tikzset=[],          # list[str]: Tikz style options (\tikzset{...})
    preamble="",         # str: Custom preamble overrides
    use_pdf=False        # bool: If True, compiles via PDF rather than DVI
)
```

> [!TIP]
> **Line Width & PDF Mode**: If thin TikZ strokes appear faint or missing in default DVI mode, set `use_pdf=True` or specify an explicit `line width` (e.g. `line width=1.5pt` or `thick`) in your TikZ markup.

---

## 3. Production Recipes

### Recipe 1: Commutative Diagram in Category Theory

```python
from manim import *
from manim_tikz import Tikz

class CommutativeDiagramScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"\textbf{Commutative Diagram via TikZ}", font_size=32).to_edge(UP, buff=0.8)
        self.add(title)

        tikz_code = r"""
        \begin{tikzpicture}[node distance=2.5cm, auto, thick]
          \node (A) {$A$};
          \node (B) [right of=A] {$B$};
          \node (C) [below of=A] {$C$};
          \node (D) [below of=B] {$D$};
          \draw[->] (A) to node {$f$} (B);
          \draw[->] (A) to node [swap] {$g$} (C);
          \draw[->] (B) to node {$h$} (D);
          \draw[->] (C) to node [swap] {$k$} (D);
        \end{tikzpicture}
        """

        diagram = Tikz(
            tikz_code,
            libraries=["positioning", "arrows.meta"],
            use_pdf=True
        ).scale(1.5).shift(DOWN * 0.2)

        # Animate drawing order
        self.play(DrawBorderThenFill(diagram), run_time=2.5)
        self.wait(1)
```

---

## 4. Best Practices

1. **Animation Types**: Because `Tikz` is an `SVGMobject`, you can apply `DrawBorderThenFill`, `Write`, `FadeIn`, and `Transform` just like any native SVG.
2. **Unsupported SVG Features**: Note that TikZ fadings, shadows, and raster transparency patterns are not supported by the underlying SVG converter; keep TikZ diagrams vector-pure (strokes, fills, nodes, and arrows).
