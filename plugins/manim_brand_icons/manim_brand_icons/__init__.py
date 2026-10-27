"""manim-brand-icons: Unified Brand & AI Icon Assets for Manim Community."""

from .brand_icon import BrandIcon, AIIcon, get_brand_color
from .fetcher import fetcher, AI_BRAND_ALIASES

__all__ = [
    "BrandIcon",
    "AIIcon",
    "get_brand_color",
    "fetcher",
    "AI_BRAND_ALIASES",
]
