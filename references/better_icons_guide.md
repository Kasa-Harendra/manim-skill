# Better Icons for Manim

This guide explains how to use **Better Icons** (200,000+ icons across 150+ collections) in Manim animation projects.

---

## Why Better Icons for Manim?

In technical, mathematical, and AI explainer animations, you constantly need specialized symbols:
- **Architecture diagrams**: database servers, cloud nodes, CPU/GPU chips, API gateways, load balancers.
- **AI/ML pipelines**: brain nodes, neural network layers, prompt bubbles, robotic agents, transformers.
- **UI & Controls**: checkmarks, warning badges, play/pause buttons, lock shields, user avatars.

Instead of hunting for SVG files online or pasting bloated raw SVGs into scenes, **Better Icons** allows you to retrieve any icon with custom hex colors and immediately instantiate it as a Manim `SVGMobject` or high-resolution transparent `ImageMobject`.

---

## 1. Direct Python Integration via `manim-brand-icons`

Our local plugin `manim-brand-icons` has built-in native integration with `better-icons`:

```python
from manim import *
from manim_brand_icons import BrandIcon, AIIcon

class TechStackScene(Scene):
    def construct(self):
        # 1. Any icon from Lucide, MDI, Tabler, Heroicons, etc.
        cpu = BrandIcon("lucide:cpu", color="#10A37F", height=1.5)
        db = BrandIcon("material-symbols:database", color="#4285F4", height=1.5)
        cloud = BrandIcon("tabler:cloud", color="#38BDF8", height=1.5)
        
        # 2. Bundled official AI & Brand icons (pre-colored)
        chatgpt = AIIcon("chatgpt", height=1.5) # Emerald Green (#10A37F)
        gemini = AIIcon("gemini", height=1.5)   # Sparkling linear gradient
        claude = AIIcon("claude", height=1.5)   # Terracotta (#D97757)
        
        icons = VGroup(cpu, db, cloud, chatgpt, gemini, claude).arrange(RIGHT, buff=0.8)
        self.play(FadeIn(icons, shift=UP))
        self.wait(2)
```

---

## 2. CLI Usage for Project Asset Retrieval

You can search and retrieve SVG files directly from the command line:

### Search for Icons
```bash
# Search across all 150+ collections
npx better-icons search "database" --limit 10

# Search within a specific collection (e.g. lucide, mdi, tabler)
npx better-icons search "brain" --prefix lucide
```

### Download SVG with Custom Color & Size
```bash
# Download pre-colored SVG directly into assets
npx better-icons get lucide:cpu --color '#10A37F' > assets/cpu.svg
npx better-icons get mdi:robot --color '#4D6BFE' > assets/robot.svg
npx better-icons get heroicons:check-circle --color '#34A853' > assets/check.svg
```

### Render to High-Resolution Transparent PNG
If you prefer crisp raster graphics in Manim without vector tessellation overhead:
```bash
python3 -c "
import os; os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = '/opt/homebrew/lib'
import cairosvg
cairosvg.svg2png(url='assets/cpu.svg', write_to='assets/cpu.png', output_width=1024, output_height=1024)
"
```

---

## 3. Configuring Better Icons as an MCP Server in Antigravity

When configured as an MCP server, Antigravity AI coding agents can search, inspect, and retrieve icons directly using native tool calls.

Add to `~/.gemini/antigravity/mcp_config.json` (or your project's `.mcp.json`):

```json
{
  "mcpServers": {
    "better-icons": {
      "command": "npx",
      "args": ["-y", "better-icons"]
    }
  }
}
```

### Agent MCP Capabilities:
- `search_icons(query, prefix, limit)`: Locate icons across Lucide, Heroicons, Material Design, etc.
- `get_icon(icon_id, color, size, format)`: Output raw SVG code with pre-applied color.
- `find_similar_icons(icon_id)`: Find visual variants across collections (outline vs solid).
- `get_icons(icon_ids, color)`: Batch retrieval for complex scenes.

---

## 4. Popular Icon Collections Reference

| Collection Prefix | Library Name | Typical Visual Style | Available Icons |
|-------------------|--------------|----------------------|-----------------|
| `lucide` | Lucide Icons | Clean modern outline (2px stroke) | 1,500+ |
| `mdi` | Material Design Icons | Solid & filled symbols | 7,000+ |
| `material-symbols`| Google Material Symbols | Modern Google system icons | 3,000+ |
| `heroicons` | Tailwind Heroicons | Minimalist UI icons (outline/solid) | 300+ |
| `tabler` | Tabler Icons | Rounded technical outline | 5,000+ |
| `ph` | Phosphor Icons | Flexible line/fill/duotone | 9,000+ |
| `simple-icons` | Simple Icons | Tech & brand logos | 3,000+ |
| `fa6-solid` | Font Awesome 6 | Classic solid vector glyphs | 2,000+ |
