# manim-data-structures Plugin Reference Guide

`manim-data-structures` provides native, highly configurable mobjects and animations for common computer science data structures (arrays, pointers, sliding windows, memory addresses, and variable tracking cards).

- **Repository**: [https://github.com/drageelr/manim-data-structures](https://github.com/drageelr/manim-data-structures)
- **Author**: Raghav Goel (@drageelr)
- **Package**: `manim-data-structures`
- **Import Namespace**: `manim_data_structures`

---

## 1. Installation & Setup

```bash
pip install manim-data-structures
```

Import in your script:
```python
from manim import *
from manim_data_structures import *
```

---

## 2. Core Components & APIs

### `MArray`
Memory array displaying elements, indices, and values with fine-grained animation handles.

```python
MArray(
    arr=[10, 20, 30, 40],               # list: Initial values
    direction=MArrayDirection.HORIZONTAL,# Orientation: HORIZONTAL or VERTICAL
    index_hex_display=False,            # bool: Format indices as 0x00, 0x01, etc.
    index_offset=0,                     # int: Base offset for indices
    hide_index=False,                   # bool: Suppress index labels
    mob_square_args={'side_length': 1.0, 'color': BLUE_C, 'stroke_width': 2},
    mob_value_args={'font_size': 26, 'color': WHITE},
    mob_index_args={'font_size': 18, 'color': GRAY_B}
)
```

#### Key Methods & Sub-Mobject Animation Handles
- `arr.animate_elem(i)`: Animates the whole element compound at index `i` (square, value, and index).
- `arr.animate_elem_square(i)`: Animates just the background square at index `i` (e.g. `.set_fill(GREEN, opacity=0.4)`).
- `arr.animate_elem_value(i)`: Animates just the value text at index `i` (e.g. `.set_color(YELLOW)`).
- `arr.animate_elem_index(i)`: Animates the index label at index `i`.
- `arr.update_elem_value(i, new_value, mob_value_args=...)`: Replaces the value at index `i`.
- `arr.append_elem(value, mob_square_args=...)`: Appends a new cell to the array.
- `arr.fetch_elem(i)`: Returns the `MArrayElement` at index `i`.

---

### `MArrayPointer`
Pointer arrows with semantic labels attached to array elements (ideal for `left`, `right`, `mid`, `head`, `tail`).

```python
pointer = MArrayPointer(
    m_array=arr,
    target_index=2,
    direction=UP,                        # Orientation of arrow towards the cell
    text="mid",
    text_args={'font_size': 20, 'color': YELLOW_C}
)
# Move pointer dynamically:
self.play(pointer.track_elem(4))
```

---

### `MArraySlidingWindow`
Highlights a contiguous sub-range of array elements for sliding window algorithms:

```python
window = MArraySlidingWindow(
    m_array=arr,
    start_index=1,
    end_index=3,
    color=TEAL_C
)
# Expand or shift window:
self.play(window.shift_window(start_index=2, end_index=4))
```

---

### `MVariable`
Displays a variable inspection card showing name and current value:

```python
var = MVariable("target", 42, label_color=BLUE_C, value_color=YELLOW_C)
self.play(Create(var))
self.play(var.update_value(84))
```

---

## 3. Production Recipes

### Recipe 1: Binary Search Visualization

```python
from manim import *
from manim_data_structures import *

class BinarySearchScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Sorted array
        data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        arr = MArray(
            data,
            mob_square_args={'color': BLUE_D, 'stroke_width': 1.8},
            mob_value_args={'font_size': 24, 'color': WHITE},
            mob_index_args={'font_size': 16, 'color': GRAY_C}
        ).shift(UP * 0.5)

        title = Tex(r"\textbf{Binary Search: Target } $x = 23$", font_size=32).to_edge(UP, buff=0.6)
        self.play(FadeIn(title), Create(arr))
        self.wait(0.5)

        # 2. Pointers: L, R, Mid
        p_left = MArrayPointer(arr, target_index=0, direction=DOWN, text="L", text_args={'color': BLUE_C})
        p_right = MArrayPointer(arr, target_index=len(data)-1, direction=DOWN, text="R", text_args={'color': RED_C})
        p_mid = MArrayPointer(arr, target_index=4, direction=UP, text="mid", text_args={'color': YELLOW_C})

        self.play(Create(p_left), Create(p_right), Create(p_mid))
        self.wait(0.5)

        # Step 1: mid = 4 (value 16 < 23) -> shift left pointer
        self.play(
            arr.animate_elem_square(4).set_fill(DARK_GREY, opacity=0.5),
            run_time=0.6
        )
        self.play(
            p_left.track_elem(5),
            p_mid.track_elem(7),
            run_time=1.0
        )
        self.wait(0.5)

        # Step 2: mid = 7 (value 56 > 23) -> shift right pointer
        self.play(
            arr.animate_elem_square(7).set_fill(DARK_GREY, opacity=0.5),
            p_right.track_elem(6),
            p_mid.track_elem(5),
            run_time=1.0
        )
        self.wait(0.5)

        # Step 3: mid = 5 (value 23 == target) -> Success!
        self.play(
            arr.animate_elem_square(5).set_fill(GREEN_D, opacity=0.8),
            arr.animate_elem_value(5).set_color(GREEN_A).scale(1.2),
            Circumscribe(arr.fetch_elem(5), color=GREEN_B),
            run_time=1.2
        )
        self.wait(1.5)
```

---

## 4. Best Practices & 3b1b Aesthetic

1. **Pure Black Canvas**: Always combine `MArray` with `self.camera.background_color = BLACK` for high-contrast element outlines.
2. **Color Highlights**: Use semantic color fills rather than full redraws—e.g., `arr.animate_elem_square(i).set_fill(TEAL_E, opacity=0.6)`.
3. **Typography**: Ensure value font size (`font_size=24`) is clearly distinguished from index font size (`font_size=16`) to maintain visual hierarchy.
4. **Pointer Spacing**: When pointers share adjacent cells, alternate directions (`UP` and `DOWN`) to prevent collision.
