# chanim (Chemistry Animations) Plugin Reference Guide

`chanim` is a chemistry animation framework for Manim Community. Powered by the LaTeX `chemfig` engine, it enables the generation of 2D organic molecular structures, skeletal diagrams, and multi-step chemical reaction pathways.

- **Repository**: [https://github.com/kilacoda/chanim](https://github.com/kilacoda/chanim)
- **Author**: kilacoda
- **Package**: `chanim`
- **Import Namespace**: `chanim`

---

## 1. Installation & Requirements

```bash
pip install chanim
```

### System Requirements
Requires a LaTeX distribution with the `chemfig` package installed (`chemfig.sty`).

---

## 2. Core Chemistry Classes & APIs

### `ChemObject`
Renders a 2D chemical structure using `chemfig` syntax:

```python
from chanim import ChemObject

# Water molecule with bent angle
water = ChemObject("H[5]-O-H[-1]")

# Ethanol
ethanol = ChemObject("H_3C-CH_2-OH")
```

### `ChemWithName`
Pairs a molecular structure with a formatted name label underneath:

```python
from chanim import ChemWithName

caffeine = ChemWithName(
    "*6((=O)-N(-CH_3)-*5(-N=-N(-CH_3)-=)--(=O)-N(-H_3C)-)",
    "Caffeine"
)
```

### `chem.creation_anim()`
Built-in animation that sequentially draws chemical bonds in order of connectivity:
```python
self.play(caffeine.creation_anim(), run_time=2.5)
```

---

## 3. Production Recipe: Synthesis & Reaction Pathway

```python
from manim import *
from chanim import ChemWithName, ChemObject

class EsterificationReactionScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"\textbf{Fischer Esterification Reaction}", font_size=32).to_edge(UP, buff=0.6)
        self.add(title)

        # 1. Reactants: Acetic Acid + Ethanol
        acetic_acid = ChemWithName("H_3C-C(=O)-OH", "Acetic Acid").shift(LEFT * 4)
        plus = MathTex("+", font_size=36).shift(LEFT * 1.8)
        ethanol = ChemWithName("HO-CH_2-CH_3", "Ethanol").shift(LEFT * 0.2)

        # 2. Reaction Arrow with catalyst (H2SO4 / Heat)
        arrow = Arrow(LEFT * 0.8, RIGHT * 0.8, buff=0.1, color=LIGHT_GREY).shift(RIGHT * 1.8)
        catalyst = Tex(r"$\mathrm{H^+,\, \Delta}$", font_size=20, color=YELLOW_C).next_to(arrow, UP, buff=0.1)

        # 3. Product: Ethyl Acetate
        ester = ChemWithName("H_3C-C(=O)-O-CH_2-CH_3", "Ethyl Acetate").shift(RIGHT * 4.2)

        # 4. Animate Reactant Assembly
        self.play(acetic_acid.creation_anim(), run_time=1.5)
        self.play(FadeIn(plus), ethanol.creation_anim(), run_time=1.5)
        self.wait(0.5)

        # 5. Reaction trigger
        self.play(GrowArrow(arrow), FadeIn(catalyst), run_time=1.0)
        self.play(ester.creation_anim(), run_time=1.8)
        self.wait(1.5)
```

---

## 4. Best Practices & 3b1b Aesthetic

1. **Skeletal Notation**: Use standard chemfig bond notation (`-` for single, `=` for double, `~` for triple).
2. **Pure Black Canvas**: Chemical bonds and heteroatom labels (N, O, S, halogens) contrast brilliantly on `BLACK` backgrounds.
3. **Pacing**: Use `chem.creation_anim()` with `run_time=1.5 - 2.5` to give viewers time to appreciate molecular geometry.
