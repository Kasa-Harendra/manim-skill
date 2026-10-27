# manim-eng Plugin Reference Guide

`manim-eng` is an electrical and engineering schematic plugin for Manim Community. It brings CircuiTikZ-level precision to Manim with Pythonic component layout, automatic wire routing, and animated voltage/current indications.

- **Repository**: [https://github.com/overegneered/manim-eng](https://github.com/overegneered/manim-eng)
- **Author**: overegneered
- **Package**: `manim-eng`
- **Import Namespace**: `manim_eng`

---

## 1. Installation & Setup

```bash
pip install manim-eng
```

Import in your script:
```python
from manim import *
from manim_eng import *
```

---

## 2. Core Electrical Components

| Component | Description | Terminals |
| :--- | :--- | :--- |
| `Resistor()` | Standard electrical resistor | `.left`, `.right` |
| `Capacitor()` | Two-plate capacitor | `.left`, `.right` |
| `Inductor()` | Coiled inductor | `.left`, `.right` |
| `VoltageSource()` | DC or AC voltage supply | `.left`, `.right` |
| `CurrentSource()` | Constant current supply | `.left`, `.right` |
| `Diode()` | Semiconductor diode | `.anode`, `.cathode` |
| `Switch()` | Open or closed circuit switch | `.left`, `.right` |
| `Cell()` | DC battery cell | `.left`, `.right` |
| `Ground()` | Earth / ground reference | `.up` |
| `Node()` | 4-way electrical junction | `.left`, `.right`, `.up`, `.down` |

---

## 3. Labels, Voltages & Currents

Components have built-in methods for placing LaTeX annotations:

```python
resistor = Resistor().rotate(90 * DEGREES)

# 1. Component value or symbol label:
resistor.set_label("R_1 = 10\\,\\Omega")

# 2. Voltage drop indication:
resistor.set_voltage("v_R(t)")

# 3. Current flow indication:
resistor.set_current("i(t)")
```

---

## 4. Building Circuits with `Circuit`

The `Circuit` container handles wire routing and terminal attachments cleanly:

```python
circuit = (
    Circuit(source, resistor, capacitor, top_node, bottom_node)
    .connect(source.right, top_node.left)
    .connect(resistor.right, top_node.down)
    .connect(capacitor.right, top_node.right)
    .connect(source.left, bottom_node.left)
    .connect(resistor.left, bottom_node.up)
    .connect(capacitor.left, bottom_node.right)
)
```

---

## 5. Production Recipe: RLC Resonant Tank Circuit

```python
from manim import *
from manim_eng import *

class RLCCircuitScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Instantiate electrical components
        v_source = VoltageSource().rotate(90 * DEGREES).shift(LEFT * 3)
        resistor = Resistor().shift(UP * 1.5)
        inductor = Inductor().rotate(90 * DEGREES).shift(RIGHT * 1)
        capacitor = Capacitor().rotate(90 * DEGREES).shift(RIGHT * 3)

        top_junction = Node().shift(UP * 1.5 + RIGHT * 1)
        bot_junction = Node().shift(DOWN * 1.5 + RIGHT * 1)
        top_left = Node().shift(UP * 1.5 + LEFT * 3)
        bot_left = Node().shift(DOWN * 1.5 + LEFT * 3)
        bot_right = Node().shift(DOWN * 1.5 + RIGHT * 3)

        # 2. Annotations & values
        v_source.set_voltage("V_s(t)")
        resistor.set_label("R")
        inductor.set_label("L")
        capacitor.set_label("C")

        # 3. Assemble and wire circuit
        circuit = (
            Circuit(
                v_source, resistor, inductor, capacitor,
                top_junction, bot_junction, top_left, bot_left, bot_right
            )
            # Source branch
            .connect(v_source.right, top_left.down)
            .connect(top_left.right, resistor.left)
            .connect(v_source.left, bot_left.up)
            .connect(bot_left.right, bot_junction.left)
            # Resistor to junction
            .connect(resistor.right, top_junction.left)
            # Parallel Inductor branch
            .connect(top_junction.down, inductor.right)
            .connect(inductor.left, bot_junction.up)
            # Parallel Capacitor branch
            .connect(top_junction.right, capacitor.right)
            .connect(capacitor.left, bot_right.up)
            .connect(bot_right.left, bot_junction.right)
        )

        title = Tex(r"\textbf{Second-Order Parallel RLC Tank Circuit}", font_size=32).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), Create(circuit), run_time=2.0)
        self.wait(1)

        # 4. Highlight resonant branch
        self.play(
            Indicate(inductor, color=YELLOW_C),
            Indicate(capacitor, color=TEAL_C),
            run_time=1.5
        )
        self.wait(1)
```

---

## 6. Best Practices

1. **Terminal Alignment**: Align components on a shared grid (e.g. `UP * 1.5`, `DOWN * 1.5`) so connecting wires form crisp right-angles.
2. **Terminal Orientation**: Rotating components (`.rotate(90 * DEGREES)`) alters terminal directions. Verify that `.left` / `.right` match your wire route.
3. **Debug Mode**: If wire connections look misaligned, enable `config_eng.debug = True` to see visual terminal markers and bounding boxes during scene drafting.
