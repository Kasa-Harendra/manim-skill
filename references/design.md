# Manim Visual Design & 3Blue1Brown Aesthetic Guide

This document defines the strict visual and animation design standards for Manim code. It enforces the signature visual craft of Grant Sanderson (3Blue1Brown) and explicitly bans common "AI slop" patterns.

---

## 1. Absolute Bans: Eliminating AI Slop

When generating Manim code, **NEVER** produce these low-effort, synthetic patterns:

### Component Containers vs. Text Encapsulation (Balanced Rounded Box Rule)
- ❌ **NEVER wrap simple text, labels, or equations in rounded boxes**: Do not encase individual mathematical formulas, definitions, titles, or single words in rounded rectangular "cards", pill badges, or bento boxes. Equations and text should breathe freely on the canvas using natural spatial layout (`VGroup.arrange`), curly braces (`Brace`), underlines, or dynamic spotlights (`Circumscribe`, `Indicate`).
- ✅ **ALLOWED: Architectural Components & Functional Subsystems**: You MAY use `RoundedRectangle` purposefully to represent higher-level architectural components and functional subsystems (e.g., an API Gateway node, Service Cluster boundary, Database subsystem, Microservice container) that encapsulate multiple internal entities or represent physical/logical compute modules.
- **Design rules when using component containers**:
  - Keep corner radii subtle (`corner_radius=0.1` to `0.2`).
  - Use sleek, low-distraction styling (`stroke_width=1.5` to `2.0`, subtle borders `#334155` or matching semantic color, low fill opacity `0.1` to `0.25`).
  - Never clutter every element with boxes—use them intentionally to delineate genuine structural components.

```python
# ❌ AI SLOP: Wrapping simple formulas or single text labels in cards
box = RoundedRectangle(corner_radius=0.3, width=6, height=3, fill_color="#1E1E2E", fill_opacity=0.8)
equation = MathTex(r"e^{i\pi} + 1 = 0")
self.play(Create(box), Write(equation))  # AVOID: Math should float freely

# ✅ PROPER USE: Delineating a genuine architectural component/subsystem
gateway_box = RoundedRectangle(corner_radius=0.15, width=4.2, height=2.4, stroke_color=BLUE_C, stroke_width=1.5, fill_opacity=0.15)
gw_title = Text("API Gateway Subsystem", font="Helvetica Neue", font_size=14, weight=BOLD, color=WHITE).next_to(gateway_box.get_top(), DOWN, buff=0.2)
gw_route1 = Text("GET  /users ➜ User Cluster", font="JetBrains Mono", font_size=11, color=GREY_A).next_to(gw_title, DOWN, buff=0.18)
gw_route2 = Text("POST /orders ➜ Order Cluster", font="JetBrains Mono", font_size=11, color=BLUE_C).next_to(gw_route1, DOWN, buff=0.12)
gateway_component = VGroup(gateway_box, gw_title, gw_route1, gw_route2)
```

---

### ❌ BANNED: Top "//" Headings & Slide-Deck Headers
- **No `//` headings**: Never prefix titles or headers with `//` (e.g. `// 01. INTRODUCTION`, `// NEURAL NETWORKS`, `// STEP 1`). Code-comment headers are a lazy AI trope.
- **No static presentation title bars**: Never anchor persistent corporate headers, breadcrumbs, or presentation banners at the top of the frame for the entire scene.
- **Contextual, evolving titles**: Titles should be elegant mathematical or conceptual statements. They enter with subtle motion, anchor context, and fade out or transform as the scene transitions into visual mechanics.

```python
# ❌ AI SLOP: Slide presentation header
title = Text("// 01. LINEAR TRANSFORMATIONS", font="JetBrains Mono", font_size=20)
title.to_corner(UL)  # NEVER DO THIS

# ✅ 3BLUE1BROWN STYLE: Elegant, purposeful concept entrance
title = Tex(r"\textbf{Visualizing Linear Transformations}", font_size=42)
title.to_edge(UP, buff=0.8)
self.play(FadeIn(title, shift=DOWN * 0.3))
self.wait(1)
# Title smoothly transitions or clears when the transformation begins
self.play(FadeOut(title, shift=UP * 0.2))
```

---

### ❌ BANNED: AI Slop Color Palettes & Gimmicks
- **No random neon or rainbow palettes**: Never use arbitrary rainbow borders, cyber-glow gradients, or saturated candy colors.
- **No washed-out dark gray backgrounds**: Never use `#1e1e1e`, `#121212`, or charcoal unless explicitly requested. Always use pure `BLACK` (`#000000`).
- **No decorative clutter**: Never add decorative particles, random floating circles, or meaningless emojis. Every pixel on screen must serve mathematical intuition.

---

### ❌ BANNED: Static Slide Syndrome
- **Never produce static bullet-point slides**: Manim is an animation engine, not PowerPoint.
- **No long static walls of text**: Never display paragraphs of explanatory text. If an idea can be shown geometrically, animated as a graph, or demonstrated through motion, **never write it as a paragraph**.

---

## 2. The 3Blue1Brown Aesthetic & Visual Standards

### Pure Black Canvas
Always configure a pure black canvas (`BLACK` / `"#000000"`). Pure black maximizes contrast, makes mathematical curves vivid, and reproduces the signature 3b1b cinematic look:

```python
self.camera.background_color = BLACK  # In construct()
# Or globally:
config.background_color = BLACK
```

---

### The 3b1b Mathematical Color Palette
Colors must carry **consistent mathematical meaning**, binding equations to geometric objects:

| Color Constant | Hex | Usage & Semantic Meaning |
|---|---|---|
| `BLUE` / `BLUE_C` | `#58C4DD` | Primary geometric focus, vectors, curves, $f(x)$ |
| `YELLOW` / `YELLOW_C` | `#FFFF00` | Active parameters, variables, time $t$, inputs $x$ |
| `GREEN` / `GREEN_C` | `#83C167` | Outputs, transformed vectors, areas, results |
| `RED` / `RED_C` | `#FC6255` | Errors, negative directions, invariants, differences |
| `PURPLE` / `PURPLE_C` | `#9A72AC` | Higher dimensions, complex plane, orthogonal spaces |
| `MAROON` | `#C55F73` | Secondary contrasts, limits, boundary cases |
| `TEAL` / `TEAL_C` | `#5CD0B3` | Coordinate grids, auxiliary constructions, projections |
| `GOLD` | `#F0AC5F` | Fundamental constants ($\pi, e, i$), special values |
| `WHITE` / Warm Cream | `#FFFFFF` / `#ECEED1` | LaTeX equations, primary mathematical text |
| `LIGHT_GREY` | `#BBBBBB` | Grid axes, subtle helper markings |

#### Semantic Color Binding Pattern
Always color-code terms in formulas to match their visual representations:

```python
# Color-code matching terms in equations and geometry
formula = MathTex(
    r"\vec{v}", r"=", r"a", r"\hat{i}", r"+", r"b", r"\hat{j}",
    substrings_to_isolate=[r"\vec{v}", r"a", r"\hat{i}", r"b", r"\hat{j}"]
)
formula.set_color_by_tex(r"\vec{v}", GREEN)
formula.set_color_by_tex(r"a", YELLOW)
formula.set_color_by_tex(r"\hat{i}", BLUE)
formula.set_color_by_tex(r"b", RED)
formula.set_color_by_tex(r"\hat{j}", PURPLE)
```

---

## 3. High-Density Animation Mechanics (The 3b1b Method)

3Blue1Brown videos feel alive because **visuals are in continuous, coordinated motion**. Use these techniques to achieve that depth:

### 1. Continuous Motion with Updaters & ValueTrackers
Instead of jumping from state A to state B, animate continuous changes using `ValueTracker` and `always_redraw()` / `.add_updater()`:

```python
# Tangent line sliding along a dynamic curve
t_tracker = ValueTracker(1.0)
axes = Axes(x_range=[-3, 3], y_range=[-1, 9], x_length=7, y_length=5)
graph = axes.plot(lambda x: x**2, color=BLUE)

# Dot tracks curve position continuously
dot = always_redraw(lambda: Dot(
    axes.c2p(t_tracker.get_value(), graph.underlying_function(t_tracker.get_value())),
    color=YELLOW
))

# Tangent line updates in real time
tangent = always_redraw(lambda: axes.get_secant_slope_group(
    t_tracker.get_value(),
    graph,
    dx=0.001,
    secant_line_length=4,
    secant_line_color=RED
))

self.play(Create(axes), Create(graph))
self.play(FadeIn(dot), Create(tangent))
self.play(t_tracker.animate.set_value(2.5), run_time=3, rate_func=smooth)
self.play(t_tracker.animate.set_value(-1.5), run_time=4, rate_func=smooth)
```

---

### 2. Seamless Mathematical Morphing
Transform equations term-by-term using `TransformMatchingTex` so the viewer can follow the algebra effortlessly:

```python
eq1 = MathTex(r"a^2", r"+", r"b^2", r"=", r"c^2")
eq2 = MathTex(r"c", r"=", r"\sqrt{a^2 + b^2}")

self.play(Write(eq1))
self.wait(0.8)
# Transforms identical LaTeX substrings smoothly into their new positions
self.play(TransformMatchingTex(eq1, eq2, path_arc=PI/4))
self.wait(1)
```

---

### 3. Directing Attention Without UI Boxes
Draw the viewer's eye using dynamic mathematical focus tools:

- **`Indicate(mobject, color=YELLOW)`**: Subtle pulse highlight.
- **`Circumscribe(mobject, color=YELLOW, fade_out=True)`**: Clean drawn loop around an expression.
- **`Flash(point, color=GOLD, line_length=0.2)`**: Point burst for sudden breakthroughs.
- **`Wiggle(mobject)`**: Playful vibration for contradictions or key terms.
- **`Arrow` / `Vector`**: Pointing directly to geometric features.

```python
# Highlight a critical term cleanly
self.play(Circumscribe(equation[2], color=YELLOW, run_time=1.5))
self.play(Indicate(graph, color=GREEN))
```

---

### 4. Dynamic Space Transformations
Bring linear algebra and calculus to life by warping spaces and tracking trajectories:

```python
# Grid transformation (Linear Algebra signature)
plane = NumberPlane(background_line_style={"stroke_opacity": 0.4})
self.play(Create(plane))

matrix = [[1, 2], [2, 1]]
self.play(plane.animate.apply_matrix(matrix), run_time=3)
```

---

### 5. Camera Choreography (`MovingCameraScene`)
For detailed visualizations, move the camera into the math rather than cramming everything on one static screen:

```python
class DeepDiveScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK

        axes = Axes(x_range=[0, 10], y_range=[0, 10])
        self.play(Create(axes))

        # Smoothly zoom into an infinitesimal region
        self.play(
            self.camera.frame.animate.set(width=3).move_to(axes.c2p(2, 4)),
            run_time=2.5,
            rate_func=smooth
        )
```

---

### 7. Screen Alignment, Centering & Composition Geometry
A visually stunning Manim presentation requires rigorous spatial discipline and mathematical composition:

- **16:9 Safe Camera Bounds**:
  - Standard Manim frame width is `14.22` and height is `8.0` (x: `[-7.11, +7.11]`, y: `[-4.0, +4.0]`).
  - Keep all visual content strictly within the safe viewport: `x ∈ [-6.4, +6.4]` horizontally and `y ∈ [-3.5, +3.5]` vertically. Never allow text, formulas, or bounding boxes to bleed against the display boundaries.
- **Strict Center-Anchoring for Primary Focus**:
  - All titles, subtitles, single-focus equations, central diagrams, and closing takeaways must be explicitly centered:
    ```python
    title = Text("Concept Architecture", font="Helvetica Neue", weight=BOLD, font_size=36).to_edge(UP, buff=0.6).set_x(0)
    ```
  - When stacking vertical tiers or feature pillars, center the entire group at `x = 0` (`group.set_x(0)` or `.move_to([0, y, 0])`) rather than pushing content off to one side.
- **Symmetrical Multi-Column Layouts (Left-Anchor Guide Discipline)**:
  - When presenting side-by-side content (e.g., raw wire/code stream on the left and architectural annotations on the right):
    - **Never stagger elements by individual widths**: Staggered centering creates messy, unaligned left edges.
    - **Anchor left-column items to a shared left guideline**: e.g., anchor left edges at `x = -5.8`:
      ```python
      code_item.move_to([-5.8 + code_item.width / 2, y, 0])
      ```
    - **Anchor right-column items to a shared left guideline**: e.g., anchor left edges at `x = +0.8`:
      ```python
      annot_item.move_to([0.8 + annot_item.width / 2, y, 0])
      ```
    - This creates a razor-sharp, terminal/editorial margin down the center with balanced outer padding on both sides.
- **Avoid Asymmetric Right-Brace Clutter**:
  - Attaching `Brace(..., direction=RIGHT)` to wide code blocks pushes label text off the right edge of the screen. Instead, use clean two-column side-by-side layouts or place annotations directly above/below the active token.
- **Mathematical Table Grid Alignment**:
  - When comparing methods or displaying tabular references, calculate explicit column center X-coordinates (e.g., `col1_x = -4.0`, `col2_x = -0.5`, `col3_x = +3.3`) rather than using variable `buff` values that distort column alignment.

---

### 8. Code Blocks, Syntax Highlighting & Guaranteed Visual Indentation
When displaying code snippets, wire data representations (JSON, XML, YAML), or terminal scripts:

#### ⚠️ The Cairo/Pango Whitespace Pitfall
Manim's `Text` mobjects use Pango and Cairo. Leading and trailing whitespace characters (spaces and tabs) **do not produce ink**, meaning the glyph bounding box only encompasses printable characters. 
**Calling `.arrange(DOWN, aligned_edge=LEFT)` on a list of `Text` lines snaps the first printable character of every line to the exact same X coordinate, completely erasing indentation!**

#### The Standard Pattern: Programmatic Line-Indent Shifts + `t2c`
Always construct code blocks using explicit `indent_level` offsets and Manim's native `t2c` (text-to-color) dictionary for syntax highlighting:

```python
def make_code_block(line_specs, base_x=-5.8, base_y=-0.1, font_size=13, buff=0.08, indent_step=0.45):
    """
    Builds code blocks with guaranteed visual indentation, exact monospace spacing, 
    and token syntax highlighting.
    
    line_specs: List of tuples (indent_level: int, text: str, t2c_dict: dict)
    """
    lines = []
    for indent, text, t2c_dict in line_specs:
        line_mob = Text(text, font="Menlo", font_size=font_size, color=WHITE, t2c=t2c_dict)
        lines.append((indent, line_mob))
    
    all_lines = VGroup(*[lm for _, lm in lines]).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    
    # Explicit horizontal shift guarantees visible hierarchy regardless of Pango bounding boxes
    for indent, line_mob in lines:
        line_mob.shift(RIGHT * indent * indent_step)
        
    min_left = min(lm.get_left()[0] for indent, lm in lines if indent == 0)
    all_lines.shift(RIGHT * (base_x - min_left))
    all_lines.set_y(base_y)
    return all_lines
```

#### Example Usage for JSON, XML, and YAML:
```python
# JSON example with nested array
json_specs = [
    (0, '{', {}),
    (1, '"id": 101,', {'"id":': CLR_KEY, '101': CLR_VAL}),
    (1, '"skills": [', {'"skills":': CLR_KEY}),
    (2, '"python", "docker"', {'"python",': CLR_VAL, '"docker"': CLR_VAL}),
    (1, '],', {}),
    (0, '}', {}),
]
json_code = make_code_block(json_specs, base_x=-5.8, base_y=0.0, indent_step=0.45)
```

---

## 4. Checklist: Is Your Code 3b1b Quality?

Before generating any Manim animation, verify against this checklist:

1. [ ] **Background**: Is `self.camera.background_color = BLACK` set?
2. [ ] **Screen Centering & Alignment**: Are all titles, single-focus cards, and summaries centered at `x = 0`? Are multi-column layouts anchored to consistent horizontal guides within the `[-6.4, +6.4]` safe margins without lopsided staggering or right-edge overflow?
3. [ ] **Component Containers Only**: Are rounded boxes used strictly for architectural components/subsystems, and NEVER wrapping simple text, titles, or equations?
4. [ ] **No `//` Headings**: No code-comment prefixes in titles or slide-deck banners?
5. [ ] **Semantic Color**: Does color code match between equations, labels, and geometry?
6. [ ] **Continuous Motion**: Are there `ValueTracker`, `always_redraw`, or updaters driving live changes?
7. [ ] **Visual Over Text**: Is the concept explained through geometric motion rather than paragraphs?
8. [ ] **Smooth Transforms**: Are equations and shapes morphing (`TransformMatchingTex`, `Transform`) rather than flashing?
9. [ ] **Proper Attention**: Are highlights done with `Indicate`, `Circumscribe`, or arrows instead of boxed outlines?
10. [ ] **Transient Cleanup**: Are all temporary particles, dots, and helper callouts explicitly faded out when stages transition?
11. [ ] **Code Blocks & Indentation**: If displaying code or wire formats (JSON, XML, YAML, Python), are lines indented via explicit programmatic horizontal shifts (`indent_step=0.40 - 0.45`) with `t2c` syntax highlighting, rather than relying on whitespace in strings that `arrange()` collapses?
12. [ ] **Mandatory Pre-Render Audio-Sync Audit (Mode 2)**:
    - [ ] Have all visual triggers been cross-checked against the actual Whisper word/segment timestamps in `timing.json` rather than arbitrary guesses?
    - [ ] Does `current_time + run_time <= next_cue_time` hold for all transitions to prevent timeline drift?
    - [ ] Have representative frames been extracted with `ffmpeg` and visually inspected to ensure zero misalignment or clipping before delivery?

