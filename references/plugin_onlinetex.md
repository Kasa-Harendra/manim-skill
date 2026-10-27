# manim-onlinetex Plugin Reference Guide

`manim-onlinetex` allows Manim Community to render LaTeX formulas for `Tex` and `MathTex` mobjects via cloud-based LaTeX compilation services (LaTeXCluster and QuickLaTeX) without requiring a local installation of TeX Live or MacTeX.

- **Repository**: [https://github.com/ManimCommunity/manim-onlinetex](https://github.com/ManimCommunity/manim-onlinetex)
- **Organization**: Manim Community
- **Package**: `manim-onlinetex`
- **Import Namespace**: `manim_onlinetex`

---

## 1. When to Use

Use `manim-onlinetex` when:
- Rendering Manim scenes on cloud runners, Docker containers, or minimal CI pipelines where installing a 4GB+ TeX Live distribution is prohibitive.
- Developing on developer machines where LaTeX is missing, corrupted, or misconfigured.
- Quick prototyping without local LaTeX toolchains.

---

## 2. Installation & Setup

```bash
pip install manim-onlinetex
```

### Critical Import Rule
Always import `manim_onlinetex` **after** `manim`:

```python
from manim import *
from manim_onlinetex import *  # Must be imported after manim
```

Upon import, the plugin automatically redirects internal LaTeX compilation calls to:
1. **LaTeXCluster** ([latexcluster.org](https://www.latexcluster.org/))
2. **QuickLaTeX** ([quicklatex.com](https://quicklatex.com/)) as a fallback

---

## 3. Production Recipe

```python
from manim import *
from manim_onlinetex import *

class CloudLatexScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Standard MathTex works seamlessly without local TeX installation
        equation = MathTex(
            r"i\hbar \frac{\partial}{\partial t} \Psi(\mathbf{r}, t) = \left[ -\frac{\hbar^2}{2m}\nabla^2 + V(\mathbf{r}, t) \right] \Psi(\mathbf{r}, t)",
            font_size=36,
            color=BLUE_B
        )

        label = Tex(
            r"\textbf{Time-Dependent Schr\"odinger Equation}",
            font_size=28,
            color=WHITE
        ).next_to(equation, UP, buff=0.8)

        self.play(FadeIn(label, shift=DOWN * 0.3))
        self.play(Write(equation), run_time=2.0)
        self.wait(1.5)
```

---

## 4. Best Practices & Caveats

1. **Keep the Media Cache**: Avoid deleting the `media/Tex` directory across runs. Cached `.svg` files prevent redundant network requests and avoid rate limits.
2. **Network Dependency**: Cloud rendering requires an active internet connection on the first compile of each unique LaTeX string.
3. **Local TeX Transition**: For high-volume offline production or air-gapped rendering, install local TeX Live and simply remove `from manim_onlinetex import *`.
