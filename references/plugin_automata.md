# manim-automata Plugin Reference Guide

`manim-automata` is a Manim Community extension for generating automated, step-by-step animations of Finite State Machines (FSMs), Deterministic/Nondeterministic Finite Automata (DFA / NFA), and Pushdown Automata (PDA) using JFLAP XML specifications.

- **Repository**: [https://github.com/SeanNelsonIO/manim-automata](https://github.com/SeanNelsonIO/manim-automata)
- **Package**: `manim-automata`
- **Import Namespace**: `manim_automata`

---

## 1. Installation & Setup

```bash
pip install manim-automata
```

Automata definitions can be created using [JFLAP](https://www.jflap.org) (saved as `.jff` files) or written as standard JFLAP XML files.

---

## 2. Core Classes & Architecture

| Class | Purpose |
| :--- | :--- |
| `ManimAutomaton(xml_file=...)` | Base automaton mobject loaded from a JFLAP `.jff` XML file. |
| `ManimDeterminsticFiniteAutomaton(...)` | DFA model with deterministic transition simulation. |
| `ManimNonDeterminsticFiniteAutomaton(...)` | NFA model handling branching non-deterministic transitions. |
| `ManimPushDownAutomaton(...)` | Pushdown Automaton with visual stack memory operations. |
| `ManimAnimations` | Base class for customizing state highlights, tape motion, and transitions. |

---

## 3. Workflow & Key Methods

1. **Initialize from XML**: Load your `.jff` file via `manim_automaton = ManimDeterminsticFiniteAutomaton(xml_file="machine.jff", cli=False)`.
2. **Camera Framing (`MovingCameraScene`)**: Since state machines vary in geometry, adjust the camera frame:
   ```python
   self.camera.frame_width = manim_automaton.width + 10
   self.camera.frame_height = manim_automaton.height + 10
   self.camera.frame.move_to(manim_automaton)
   ```
3. **Construct Input Tape**: Generate the animated tape input mobject:
   ```python
   automaton_input = manim_automaton.construct_automaton_input("110011")
   automaton_input.shift(UP * 3)
   ```
4. **Step Through the Input Sequence**: Animate the machine evaluating the string:
   ```python
   for sequence in manim_automaton.play_string(automaton_input):
       self.play(*sequence, run_time=0.6)
   ```

---

## 4. Production Recipe

```python
from manim import *
from manim_automata import ManimDeterminsticFiniteAutomaton

class DFASimulationScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Load DFA from JFLAP XML
        automaton = ManimDeterminsticFiniteAutomaton(
            xml_file="assets/dfa_binary_even_zeros.jff",
            cli=False
        )

        # 2. Camera framing
        self.camera.frame_width = automaton.width + 6
        self.camera.frame_height = automaton.height + 6
        self.camera.frame.move_to(automaton)

        # 3. Create input string tape
        input_tape = automaton.construct_automaton_input("10100")
        input_tape.next_to(automaton, UP, buff=1.0)

        # 4. Initial entrance
        self.play(
            DrawBorderThenFill(automaton),
            FadeIn(input_tape, shift=DOWN * 0.3),
            run_time=1.5
        )
        self.wait(0.5)

        # 5. Play automated string consumption
        for sequence in automaton.play_string(input_tape):
            self.play(*sequence, run_time=0.5)

        self.wait(1.5)
```

---

## 5. Best Practices & 3b1b Aesthetic Tips

- **Camera Centering**: Always position the automaton relative to the center or use `MovingCameraScene` to keep state transitions and the tape header comfortably within bounds.
- **Tape Positioning**: Place the input tape directly above (`next_to(automaton, UP, buff=0.8)`) so viewers can track the tape pointer and active states simultaneously.
- **Pacing**: Use `run_time=0.4 - 0.6` per token step for snappy evaluation, pausing with `self.wait()` at final accepting or rejecting states.
