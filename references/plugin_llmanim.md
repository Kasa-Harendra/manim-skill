# LLManim Plugin Reference Guide

`LLManim` is a specialized library of pre-built visual components, animations, and mathematical utilities designed specifically for creating high-retention educational videos about Large Language Models, Transformer architectures, and Deep Learning mechanics using Manim Community.

- **Repository**: [https://github.com/rishabhbhartiya/LLManim](https://github.com/rishabhbhartiya/LLManim)
- **Author**: Rishabh Bhartiya
- **Package**: `llmanim`
- **Import Namespace**: `llmanim`

---

## 1. Installation & Setup

```bash
pip install llmanim
```

Import in your script:
```python
from manim import *
from llmanim.base.shapes import MatrixBox, VectorBar, TokenBox, LabeledBlock, SoftmaxCurve
from llmanim.base.animations import highlight_sequence, data_flow_arrow, attention_flow, forward_pass_pulse
from llmanim.tokenization.token_box import TokenRow, BPESequence, VocabTable
from llmanim.styles.colors import TOKEN_COLOR, EMBEDDING_COLOR, ATTENTION_COLOR, QUERY_COLOR, KEY_COLOR, VALUE_COLOR
```

---

## 2. Core Visual Components

### 1. `TokenRow` & `TokenBox`
Visualizes input strings parsed into discreet token representations:
```python
row = TokenRow(["Attention", "is", "all", "you", "need"], token_ids=[324, 82, 12, 45, 98])
self.play(row.appear())
```

### 2. `MatrixBox`
Grid representation of weight matrices ($W_Q, W_K, W_V$) or embedding tables:
```python
mat = MatrixBox(rows=4, cols=6, color=EMBEDDING_COLOR)
self.play(mat.fill_anim())
self.play(mat.highlight_row(1))
self.play(mat.highlight_col(3))
```

### 3. `VectorBar`
1D dense representation of token embeddings or latent states:
```python
vec = VectorBar(dim=8, values=[0.12, -0.45, 0.88, 0.31, -0.05, 0.62, -0.71, 0.44])
self.play(vec.pulse())
```

### 4. `SoftmaxCurve`
Dynamic probability distribution bar chart showing logits converted to probabilities:
```python
softmax_bars = SoftmaxCurve(logits=[2.4, 0.8, -1.2, 4.1])
self.play(softmax_bars.show_values())
```

---

## 3. High-Density Animations

| Function | Purpose |
| :--- | :--- |
| `data_flow_arrow(src, tgt, label="...")` | Creates and animates a labeled connection arrow between architectural blocks. |
| `highlight_sequence(boxes)` | Cascading sequential glow highlighting each box in order. |
| `attention_flow(tokens, weights)` | Draws weighted, curved attention connection arcs between token positions. |
| `forward_pass_pulse(blocks)` | Sends an energy pulse travelling through a sequence of layers. |

---

## 4. Production Recipe: Scaled Dot-Product Attention (Q, K, V)

```python
from manim import *
from llmanim.base.shapes import MatrixBox, VectorBar
from llmanim.base.animations import data_flow_arrow, highlight_sequence
from llmanim.tokenization.token_box import TokenRow
from llmanim.styles.colors import (
    TOKEN_COLOR, QUERY_COLOR, KEY_COLOR, VALUE_COLOR, ATTENTION_COLOR
)

class TransformerAttentionScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"\textbf{Self-Attention: } $\mathrm{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$", font_size=32).to_edge(UP, buff=0.6)
        self.add(title)

        # 1. Token Input Sequence
        tokens = TokenRow(["Thinking", "Machines"], token_ids=[1042, 5912]).shift(UP * 1.8)
        self.play(tokens.appear())
        self.wait(0.5)

        # 2. Q, K, V Projections
        q_box = VectorBar(dim=4, values=[0.8, 0.2, -0.5, 0.1], color=QUERY_COLOR).shift(LEFT * 4 + DOWN * 0.2)
        k_box = VectorBar(dim=4, values=[0.7, 0.3, -0.4, 0.2], color=KEY_COLOR).shift(LEFT * 0 + DOWN * 0.2)
        v_box = VectorBar(dim=4, values=[0.1, 0.9, 0.4, -0.3], color=VALUE_COLOR).shift(RIGHT * 4 + DOWN * 0.2)

        q_label = MathTex("Q", color=QUERY_COLOR).next_to(q_box, UP)
        k_label = MathTex("K", color=KEY_COLOR).next_to(k_box, UP)
        v_label = MathTex("V", color=VALUE_COLOR).next_to(v_box, UP)

        self.play(
            FadeIn(q_box), FadeIn(q_label),
            FadeIn(k_box), FadeIn(k_label),
            FadeIn(v_box), FadeIn(v_label),
            run_time=1.5
        )
        self.wait(0.5)

        # 3. Attention Score Matrix (2x2)
        attn_matrix = MatrixBox(rows=2, cols=2, color=ATTENTION_COLOR).shift(DOWN * 2.2)
        attn_label = Text("Attention Weights", font_size=18, color=ATTENTION_COLOR).next_to(attn_matrix, DOWN, buff=0.2)

        self.play(attn_matrix.fill_anim(), FadeIn(attn_label), run_time=1.2)
        self.wait(0.5)

        # 4. Highlight attention activation
        self.play(attn_matrix.highlight_row(0))
        self.play(v_box.pulse())
        self.wait(1.5)
```

---

## 5. Best Practices & 3b1b Aesthetic

1. **Semantic Color Palette**: Stick to standard LLManim semantic colors (`QUERY_COLOR`, `KEY_COLOR`, `VALUE_COLOR`, `TOKEN_COLOR`) to maintain instant visual clarity across scenes.
2. **Dimension Scaling**: Keep matrix and vector visual dimensions small (e.g. 4 to 8 units) rather than actual 4096-wide tensors to ensure elements remain crisp and legible.
3. **Continuous Motion**: Chain operations with `data_flow_arrow` and `pulse_glow` rather than sudden cuts.
