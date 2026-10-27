# manim-brand-icons Plugin Reference Guide

`manim-brand-icons` is a dedicated Manim Community plugin and asset library for rendering high-resolution brand icons, logos, and transparent PNGs. It integrates:
1. **`simplepycons`**: Offline access to 3,000+ vector brand icons and primary brand colors without external network calls or API keys.
2. **Brandfetch / Clearbit / Unavatar**: Dynamic on-the-fly logo fetching and caching for arbitrary startup domains and company websites.
3. **Bundled Pre-rendered Transparent PNGs & SVGs**: Ready-to-use 1024x1024 transparent assets for all major AI providers and products.

- **Location**: [`plugins/manim_brand_icons`](file:///Users/kasaharendra/.gemini/config/skills/manim/plugins/manim_brand_icons)
- **Asset Directory**: [`assets/icons/`](file:///Users/kasaharendra/.gemini/config/skills/manim/assets/icons) (`png/` and `svg/`)
- **Package**: `manim-brand-icons`
- **Import Namespace**: `manim_brand_icons`

---

## 1. Installation & Setup

```bash
# Installed locally inside the skill environment:
pip install -e /Users/kasaharendra/.gemini/config/skills/manim/plugins/manim_brand_icons simplepycons requests cairosvg
```

Import in your script:
```python
from manim import *
from manim_brand_icons import AIIcon, BrandIcon, get_brand_color
```

---

## 2. Core APIs & Usage Modes

### `AIIcon(name, mode="auto", height=1.0, color=None)`
Convenience function specifically designed for AI, LLM, and Machine Learning workflows.

```python
# 1. Transparent PNG (Full fidelity ImageMobject)
chatgpt_png = AIIcon("chatgpt", mode="png", height=1.2)

# 2. Vector SVG (SVGMobject ready for DrawBorderThenFill & Transforms)
gemini_svg = AIIcon("gemini", mode="svg", height=1.2)

# 3. Vector with official Brand Primary Color applied automatically
claude_colored = AIIcon("claude", mode="svg", color="brand")

# 4. Auto mode (prefers vector SVG if available, fallback to PNG)
deepseek = AIIcon("deepseek", mode="auto", height=1.0)
```

---

### `BrandIcon(name_or_domain, mode="auto", height=1.0, color=None)`
General-purpose brand loader supporting any tech company, consumer brand, or website domain:

```python
# From simplepycons offline library (e.g. github, python, docker, aws, spotify)
github_icon = BrandIcon("github", mode="svg", color=WHITE)

# Arbitrary website domain via Clearbit / Brandfetch API (auto-cached)
linear_icon = BrandIcon("linear.app", mode="png", height=1.0)
cursor_icon = BrandIcon("cursor.com", mode="png", height=1.0)
```

---

### Supported Out-of-the-Box AI Models & Brands

The plugin includes pre-configured aliases, official primary colors, and pre-rendered 1024x1024 transparent PNGs for:

| Brand / Product | Aliases | Primary Hex Color | Modes Available |
| :--- | :--- | :--- | :--- |
| **OpenAI** | `"openai"` | `#0081A5` | `svg`, `png` |
| **ChatGPT** | `"chatgpt"` | `#10A37F` | `svg`, `png` |
| **Google Gemini** | `"gemini"`, `"google_gemini"` | `#8E75B2` | `svg`, `png` |
| **Anthropic Claude** | `"claude"`, `"anthropic"` | `#D97757` | `svg`, `png` |
| **Meta AI / LLaMA** | `"meta"`, `"llama"` | `#0668E1` / `#9844FF` | `svg`, `png` |
| **Mistral AI** | `"mistral"`, `"mistralai"` | `#FA520F` | `svg`, `png` |
| **DeepSeek** | `"deepseek"` | `#5786FE` | `svg`, `png` |
| **Ollama** | `"ollama"` | `#FFFFFF` | `svg`, `png` |
| **Hugging Face** | `"huggingface"` | `#FFD21E` | `svg`, `png` |
| **NVIDIA** | `"nvidia"` | `#76B900` | `svg`, `png` |
| **Perplexity AI** | `"perplexity"` | `#1FB8CD` | `svg`, `png` |
| **PyTorch** | `"pytorch"` | `#EE4C2C` | `svg`, `png` |
| **TensorFlow** | `"tensorflow"` | `#FF6F00` | `svg`, `png` |
| **Google Colab** | `"colab"`, `"googlecolab"` | `#F9AB00` | `svg`, `png` |
| **Google DeepMind**| `"deepmind"` | `#4285F4` | `svg`, `png` |
| **OpenRouter** | `"openrouter"` | `#94A3B8` | `svg`, `png` |
| **Microsoft Copilot**| `"copilot"` | `#236BFE` | `png` |
| **Midjourney** | `"midjourney"` | `#FFFFFF` | `png` |
| **Stability AI** | `"stabilityai"` | `#702AFE` | `png` |

---

## 3. Production Recipes

### Recipe 1: Frontier LLM Comparison (Transparent PNG Showcase)

Uses native transparent PNGs (`mode="png"`) with smooth scale entrances and metric cards:

```python
from manim import *
from manim_brand_icons import AIIcon, get_brand_color

class FrontierLLMGrid(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"\textbf{Frontier AI Ecosystem: The 2026 Landscape}", font_size=32).to_edge(UP, buff=0.6)
        self.add(title)

        # 4 Core Frontier Models
        models = [
            ("chatgpt", "ChatGPT (o3-mini)", "Reasoning Leader"),
            ("gemini", "Gemini 2.0 Flash", "Multimodal SOTA"),
            ("claude", "Claude 3.5 Sonnet", "Coding Benchmark"),
            ("deepseek", "DeepSeek-R1", "Open-Weights SOTA"),
        ]

        cards = VGroup()

        for slug, name, tag in models:
            # 1. Load transparent PNG directly as an ImageMobject
            icon = AIIcon(slug, mode="png", height=1.1)
            
            # 2. Get official brand color for accent
            accent_color = get_brand_color(slug)
            
            label = Text(name, font_size=16, color=WHITE).next_to(icon, DOWN, buff=0.25)
            badge = Text(tag, font_size=13, color=accent_color).next_to(label, DOWN, buff=0.15)
            
            card = VGroup(icon, label, badge)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.8).shift(DOWN * 0.3)

        # Animate entrance with stagger
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.5) for card in cards], lag_ratio=0.25),
            run_time=2.0
        )
        self.wait(1.0)

        # Dynamic focus spotlight on DeepSeek & Gemini
        self.play(
            cards[1][0].animate.scale(1.2),
            cards[3][0].animate.scale(1.2),
            run_time=0.8
        )
        self.wait(1.5)
```

---

### Recipe 2: Vector Morphing & Synthesis (Vector SVG Mode)

Uses `mode="svg"` for mathematical morphing via `TransformMatchingShapes`:

```python
from manim import *
from manim_brand_icons import AIIcon

class AIModelTransformation(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Start with OpenAI SVG
        icon_openai = AIIcon("openai", mode="svg", height=2.0, color="#0081A5")
        icon_gemini = AIIcon("gemini", mode="svg", height=2.0, color="#8E75B2")

        label_openai = Text("Proprietary Frontier", font_size=20, color=WHITE).next_to(icon_openai, DOWN, buff=0.5)
        label_gemini = Text("Multimodal Engine", font_size=20, color=WHITE).next_to(icon_gemini, DOWN, buff=0.5)

        self.play(DrawBorderThenFill(icon_openai), FadeIn(label_openai), run_time=1.8)
        self.wait(1.0)

        # Morph directly from OpenAI rosette to Gemini star
        self.play(
            Transform(icon_openai, icon_gemini),
            Transform(label_openai, label_gemini),
            run_time=1.5
        )
        self.wait(1.5)
```

---

## 4. Best Practices & 3b1b Aesthetic

1. **When to use PNG vs. SVG**:
   - Use `mode="png"` (Transparent PNG) when you want photorealistic, multi-colored brand logos (e.g. Hugging Face yellow emoji, DeepSeek blue gradient, Google multi-color G).
   - Use `mode="svg"` (Vector SVG) when animating lines, drawing outlines (`DrawBorderThenFill`), or morphing between logos (`Transform`).
2. **Pure Black Contrast**: All transparent PNGs in `assets/icons/png/` have transparent alpha backgrounds and render cleanly against `#000000`.
3. **No Container Cards**: Never encase the brand icon and label inside a generic rounded rectangular box; allow the logo and its typography to breathe directly on the canvas.
