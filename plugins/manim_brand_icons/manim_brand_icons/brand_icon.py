"""Manim Mobject wrapper for Brand and AI icons."""

from typing import Optional, Union
from .fetcher import fetcher, AI_BRAND_ALIASES


def BrandIcon(
    name_or_domain: str,
    mode: str = "auto",
    height: float = 1.0,
    width: Optional[float] = None,
    color: Optional[str] = None,
    **kwargs
):
    """
    Returns a Manim Mobject (SVGMobject or ImageMobject) for a brand or AI provider.

    Parameters:
    - name_or_domain: Brand slug, company name, or domain (e.g. 'openai', 'gemini', 'claude', 'github.com')
    - mode: 'auto' (prefers vector SVG, falls back to PNG), 'svg' (enforce vector), 'png' (enforce transparent PNG)
    - height: Scale height of the mobject in Manim scene units (default 1.0)
    - width: Optional explicit width scaling
    - color: Hex color or 'brand' to apply the official brand primary color (SVG only)
    """
    # Lazy import manim so non-manim utilities can still import this module
    from manim import SVGMobject, ImageMobject, WHITE

    paths = fetcher.get_icon_paths(name_or_domain)
    svg_path = paths.get("svg")
    png_path = paths.get("png")
    brand_color = paths.get("color") or "#FFFFFF"

    target_type = mode.lower()
    if target_type == "auto":
        target_type = "svg" if svg_path else "png"

    if target_type == "svg":
        if not svg_path:
            if png_path:
                target_type = "png"
            else:
                raise FileNotFoundError(f"Could not locate or generate SVG for brand: '{name_or_domain}'")
        else:
            mob = SVGMobject(svg_path, **kwargs)
            if color == "brand":
                mob.set_color(brand_color)
            elif color:
                mob.set_color(color)

    if target_type == "png":
        if not png_path:
            raise FileNotFoundError(f"Could not locate or generate transparent PNG for brand: '{name_or_domain}'")
        mob = ImageMobject(png_path, **kwargs)

    if height is not None:
        mob.set_height(height)
    if width is not None:
        mob.set_width(width)

    # Attach metadata attributes for animation workflows
    mob.brand_name = paths.get("name")
    mob.brand_color = brand_color
    mob.svg_path = svg_path
    mob.png_path = png_path

    return mob


def AIIcon(
    name: str,
    mode: str = "auto",
    height: float = 1.0,
    color: Optional[str] = None,
    **kwargs
):
    """Convenience alias specifically tailored for AI, LLM, and Machine Learning brand icons."""
    return BrandIcon(name_or_domain=name, mode=mode, height=height, color=color, **kwargs)


def get_brand_color(name_or_domain: str) -> str:
    """Returns the official brand primary hex color."""
    return fetcher.get_brand_color(name_or_domain)
