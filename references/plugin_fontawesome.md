# manim-fontawesome Plugin Reference Guide

`manim-fontawesome` gives Manim direct access to thousands of Font Awesome (v6.5.1) vector icons as native `SVGMobject` instances. It allows you to build clean, professional software architecture, cloud infrastructure, and systems diagrams without low-res PNGs or manual SVG asset management.

- **Repository**: [https://github.com/naveen521kk/manim-fontawesome](https://github.com/naveen521kk/manim-fontawesome)
- **Author**: Naveen M K
- **Package**: `manim-fontawesome`
- **Import Namespace**: `manim_fontawesome`

---

## 1. Installation & Setup

```bash
pip install manim-fontawesome
```

Import in your script:
```python
from manim import *
from manim_fontawesome import brand, regular, solid
```

---

## 2. Icon Categories

Icons are organized into three namespaces as dynamic Python attributes returning `SVGMobject`:

### 1. `brand`
Tech stacks, languages, frameworks, cloud providers, and platforms:
- `brand.python`, `brand.rust`, `brand.golang`, `brand.java`, `brand.js`
- `brand.docker`, `brand.aws`, `brand.linux`, `brand.ubuntu`, `brand.debian`
- `brand.github`, `brand.gitlab`, `brand.git`, `brand.bitbucket`
- `brand.react`, `brand.vuejs`, `brand.angular`, `brand.node_js`
- `brand.apple`, `brand.google`, `brand.windows`, `brand.cloudflare`

### 2. `solid`
Infrastructure, hardware, security, data structures, and utilities:
- `solid.server`, `solid.database`, `solid.network_wired`, `solid.cloud`
- `solid.microchip`, `solid.memory`, `solid.hard_drive`, `solid.terminal`
- `solid.shield_halved`, `solid.lock`, `solid.key`, `solid.fingerprint`
- `solid.code_branch`, `solid.code_commit`, `solid.code_pull_request`
- `solid.gear`, `solid.arrows_spin`, `solid.bolt`, `solid.magnifying_glass`

### 3. `regular`
Outlined glyphs for notifications, status, documents, and UI states:
- `regular.bell`, `regular.clock`, `regular.circle_check`, `regular.circle_xmark`
- `regular.file_code`, `regular.folder_open`, `regular.comment`, `regular.eye`

---

## 3. Styling & Animation Capabilities

Because every icon is a native `SVGMobject`:
- **Resizing**: `icon.scale(0.6)` or `icon.set_height(0.8)`.
- **Coloring**: `icon.set_color(BLUE_C)` or `icon.set_fill(YELLOW_C, opacity=1.0)`.
- **Animations**:
  - `DrawBorderThenFill(icon)`: Sleek animated outline and fill.
  - `Write(icon)` or `Create(icon)`.
  - `Transform(icon_a, icon_b)`.
  - `Indicate(icon, color=RED_C)` or `Flash(icon)`.

---

## 4. AI & LLM Model Icons: ChatGPT, Gemini, Claude, OpenAI

When creating AI/LLM comparisons or architecture explainer videos, you can render brand-accurate vector icons directly in Manim:

### Method 1: Using `manim-fontawesome`
- **ChatGPT / OpenAI**: `brand.openai` (The official OpenAI rosette / ChatGPT icon)
- **Google**: `brand.google` (The official Google 'G' logo)
- **Sparkles / AI Magic**: `solid.wand_magic_sparkles` or `solid.sparkles`

```python
from manim import *
from manim_fontawesome import brand, solid

# ChatGPT (OpenAI) Icon:
chatgpt_icon = brand.openai.scale(0.8).set_color("#10A37F")  # OpenAI Teal

# Google Icon:
google_icon = brand.google.scale(0.8).set_color("#4285F4")   # Google Blue
```

### Method 2: Native Vector Mobjects for Gemini & ChatGPT (No External File Needed)
You can instantiate pixel-perfect, scalable vector icons directly via inline SVG strings:

```python
from manim import *
import tempfile, os

def get_gemini_icon(size=1.0, color="#8E75FF"):
    """
    Returns the official Google Gemini 4-point curved sparkle diamond star as an SVGMobject.
    """
    svg_data = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white">
      <path d="M12 0C12 6.627 6.627 12 0 12C6.627 12 12 17.373 12 24C12 17.373 17.373 12 24 12C17.373 12 12 6.627 12 0Z"/>
    </svg>"""
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
        f.write(svg_data)
        path = f.name
    mob = SVGMobject(path).scale(size).set_color(color)
    os.unlink(path)
    return mob

def get_chatgpt_icon(size=1.0, color="#10A37F"):
    """
    Returns the official ChatGPT / OpenAI spiral rosette logo as an SVGMobject.
    """
    from manim_fontawesome import brand
    return brand.openai.copy().scale(size).set_color(color)
```

### AI Model Comparison Recipe (ChatGPT vs. Gemini)

```python
from manim import *
from manim_fontawesome import brand

class ModelShowdownScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"\textbf{Frontier LLM Benchmarks: GPT-4o vs. Gemini 1.5 Pro}", font_size=32).to_edge(UP, buff=0.6)
        self.add(title)

        # ChatGPT Node
        chatgpt_logo = brand.openai.scale(0.8).set_color("#10A37F").shift(LEFT * 3.5)
        chatgpt_name = Text("ChatGPT (GPT-4o)", font_size=20, color=WHITE).next_to(chatgpt_logo, DOWN, buff=0.3)
        chatgpt_metric = MathTex(r"\mathbf{MMLU:\ 88.7\%}", font_size=22, color="#10A37F").next_to(chatgpt_name, DOWN, buff=0.2)
        chatgpt_group = VGroup(chatgpt_logo, chatgpt_name, chatgpt_metric)

        # Gemini Node
        gemini_logo = get_gemini_icon(size=0.8, color="#4E75F8").shift(RIGHT * 3.5)
        gemini_name = Text("Google Gemini 1.5 Pro", font_size=20, color=WHITE).next_to(gemini_logo, DOWN, buff=0.3)
        gemini_metric = MathTex(r"\mathbf{MMLU:\ 85.9\%}", font_size=22, color="#4E75F8").next_to(gemini_name, DOWN, buff=0.2)
        gemini_group = VGroup(gemini_logo, gemini_name, gemini_metric)

        # VS divider
        vs = Text("VS", font_size=26, color=GRAY_B)

        self.play(
            DrawBorderThenFill(chatgpt_logo),
            Write(chatgpt_name),
            DrawBorderThenFill(gemini_logo),
            Write(gemini_name),
            FadeIn(vs),
            run_time=2.0
        )
        self.play(FadeIn(chatgpt_metric), FadeIn(gemini_metric), run_time=1.0)
        self.wait(1)

        # Dynamic focus highlight
        self.play(
            Indicate(chatgpt_logo, color=YELLOW_C),
            Indicate(gemini_logo, color=YELLOW_C),
            run_time=1.2
        )
        self.wait(1.5)
```

---

## 5. Production Recipe: Distributed Microservices Architecture

Visualizing an API Gateway routing traffic to Microservices and Database nodes:

```python
from manim import *
from manim_fontawesome import brand, solid

class MicroservicesScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"\textbf{Event-Driven Microservices Architecture}", font_size=32).to_edge(UP, buff=0.6)
        self.add(title)

        # 1. Icons for Infrastructure Nodes
        client_icon = brand.apple.scale(0.5).set_color(LIGHT_GREY).shift(LEFT * 5.5)
        client_label = Text("Client App", font_size=16, color=LIGHT_GREY).next_to(client_icon, DOWN, buff=0.2)

        gateway_icon = solid.network_wired.scale(0.6).set_color(BLUE_C).shift(LEFT * 2.5)
        gateway_label = Text("API Gateway", font_size=16, color=BLUE_C).next_to(gateway_icon, DOWN, buff=0.2)

        auth_service = brand.rust.scale(0.5).set_color(ORANGE).shift(RIGHT * 1 + UP * 1.5)
        auth_label = Text("Auth (Rust)", font_size=14, color=ORANGE).next_to(auth_service, DOWN, buff=0.15)

        data_service = brand.python.scale(0.5).set_color(YELLOW_C).shift(RIGHT * 1 + DOWN * 1.5)
        data_label = Text("Service (Python)", font_size=14, color=YELLOW_C).next_to(data_service, DOWN, buff=0.15)

        db_icon = solid.database.scale(0.6).set_color(GREEN_C).shift(RIGHT * 4.5)
        db_label = Text("Primary DB", font_size=16, color=GREEN_C).next_to(db_icon, DOWN, buff=0.2)

        nodes = VGroup(
            client_icon, client_label,
            gateway_icon, gateway_label,
            auth_service, auth_label,
            data_service, data_label,
            db_icon, db_label
        )

        # 2. Network links
        wire1 = Arrow(client_icon.get_right(), gateway_icon.get_left(), buff=0.2, stroke_width=2.5, color=GRAY_B)
        wire_auth = Arrow(gateway_icon.get_right(), auth_service.get_left(), buff=0.2, stroke_width=2.5, color=GRAY_B)
        wire_data = Arrow(gateway_icon.get_right(), data_service.get_left(), buff=0.2, stroke_width=2.5, color=GRAY_B)
        wire_db = Arrow(data_service.get_right(), db_icon.get_left(), buff=0.2, stroke_width=2.5, color=GRAY_B)

        wires = VGroup(wire1, wire_auth, wire_data, wire_db)

        # 3. Entrance
        self.play(DrawBorderThenFill(nodes), Create(wires), run_time=2.0)
        self.wait(0.5)

        # 4. Animated Data Packet Flow (Anti-slop dynamic motion)
        packet = Dot(color=YELLOW_A, radius=0.08).move_to(client_icon.get_center())
        self.play(FadeIn(packet, scale=0.5))

        # Client -> Gateway
        self.play(packet.animate.move_to(gateway_icon.get_center()), run_time=0.8, rate_func=linear)
        self.play(Indicate(gateway_icon, color=YELLOW_C, scale_factor=1.2), run_time=0.3)

        # Gateway -> Data Service -> Database
        self.play(packet.animate.move_to(data_service.get_center()), run_time=0.8, rate_func=linear)
        self.play(Indicate(data_service, color=YELLOW_C, scale_factor=1.2), run_time=0.3)

        self.play(packet.animate.move_to(db_icon.get_center()), run_time=0.8, rate_func=linear)
        self.play(Flash(db_icon, color=GREEN_A, line_length=0.2), run_time=0.5)
        self.play(FadeOut(packet))
        self.wait(1.0)
```

---

## 5. Best Practices & 3b1b Aesthetic Tips

1. **Semantic Color Binding**: Give functional components intentional colors (e.g. `BLUE_C` for gateways, `ORANGE` for security/auth, `GREEN_C` for persistent databases).
2. **Never Enclose in AI-Slop Boxes**: Do not wrap icons and their small labels inside rounded grey rectangles or pill containers. Let the icon and its text breathe cleanly on the pure black canvas.
3. **Use Animated Packet Pulses**: Direct attention across network lines using moving `Dot` packets and `Indicate()` rather than static arrows alone.
