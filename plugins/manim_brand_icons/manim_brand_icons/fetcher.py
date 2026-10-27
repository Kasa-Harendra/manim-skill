"""Fetcher utilities for simplepycons and Brandfetch/Clearbit APIs."""

import os
import sys
import ssl
import json
import urllib.request
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

# Ensure Homebrew libcairo can be found on macOS Apple Silicon
if sys.platform == "darwin" and os.path.exists("/opt/homebrew/lib"):
    current_dyld = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    if "/opt/homebrew/lib" not in current_dyld:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = f"/opt/homebrew/lib:{current_dyld}".rstrip(":")

# Package bundled assets directory
SKILL_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BUNDLED_ASSETS_DIR = SKILL_ROOT / "assets" / "icons"
USER_CACHE_DIR = Path.home() / ".cache" / "manim_brand_icons"

# Brand aliases map to simplepycons methods and domains
AI_BRAND_ALIASES = {
    "openai": {"simple": "openaigym", "domain": "openai.com", "color": "#0081A5"},
    "chatgpt": {"simple": "openaigym", "domain": "chatgpt.com", "color": "#10A37F"},
    "gemini": {"simple": "googlegemini", "domain": "gemini.google.com", "color": "#8E75B2"},
    "google_gemini": {"simple": "googlegemini", "domain": "gemini.google.com", "color": "#8E75B2"},
    "claude": {"simple": "anthropic", "domain": "anthropic.com", "color": "#D97757"},
    "anthropic": {"simple": "anthropic", "domain": "anthropic.com", "color": "#191919"},
    "meta": {"simple": "metaai", "domain": "meta.com", "color": "#0668E1"},
    "llama": {"simple": "metaai", "domain": "meta.com", "color": "#9844FF"},
    "mistral": {"simple": "mistralai", "domain": "mistral.ai", "color": "#FA520F"},
    "mistralai": {"simple": "mistralai", "domain": "mistral.ai", "color": "#FA520F"},
    "deepseek": {"simple": "deepseek", "domain": "deepseek.com", "color": "#5786FE"},
    "ollama": {"simple": "ollama", "domain": "ollama.ai", "color": "#FFFFFF"},
    "huggingface": {"simple": "huggingface", "domain": "huggingface.co", "color": "#FFD21E"},
    "nvidia": {"simple": "nvidia", "domain": "nvidia.com", "color": "#76B900"},
    "copilot": {"simple": "microsoft", "domain": "copilot.microsoft.com", "color": "#236BFE"},
    "perplexity": {"simple": "perplexity", "domain": "perplexity.ai", "color": "#1FB8CD"},
    "midjourney": {"simple": None, "domain": "midjourney.com", "color": "#FFFFFF"},
    "stabilityai": {"simple": None, "domain": "stability.ai", "color": "#702AFE"},
    "groq": {"simple": None, "domain": "groq.com", "color": "#F55036"},
    "pytorch": {"simple": "pytorch", "domain": "pytorch.org", "color": "#EE4C2C"},
    "tensorflow": {"simple": "tensorflow", "domain": "tensorflow.org", "color": "#FF6F00"},
    "google": {"simple": "google", "domain": "google.com", "color": "#4285F4"},
    "colab": {"simple": "googlecolab", "domain": "colab.research.google.com", "color": "#F9AB00"},
    "deepmind": {"simple": "deepmind", "domain": "deepmind.google", "color": "#4285F4"},
    "openrouter": {"simple": "openrouter", "domain": "openrouter.ai", "color": "#94A3B8"},
    "github": {"simple": "github", "domain": "github.com", "color": "#181717"},
}


class BrandIconFetcher:
    """Orchestrates asset discovery across bundled assets, simplepycons, and web APIs."""

    def __init__(self):
        USER_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._simplepycons_icons = None

    def _get_simplepycons(self):
        if self._simplepycons_icons is None:
            try:
                from simplepycons import all_icons
                self._simplepycons_icons = all_icons
            except ImportError:
                self._simplepycons_icons = False
        return self._simplepycons_icons

    def get_brand_color(self, name: str) -> str:
        """Returns the official hex color for a brand or #FFFFFF default."""
        slug = name.lower().replace("-", "_").replace(" ", "_")
        if slug in AI_BRAND_ALIASES:
            return AI_BRAND_ALIASES[slug].get("color", "#FFFFFF")
        
        # Check simplepycons
        all_icons = self._get_simplepycons()
        if all_icons:
            method_name = f"get_{slug.replace('_', '')}_icon"
            if hasattr(all_icons, method_name):
                icon = getattr(all_icons, method_name)()
                return f"#{icon.primary_color}"
        return "#FFFFFF"

    def get_icon_paths(self, name_or_domain: str) -> Dict[str, Optional[str]]:
        """
        Locates or generates both SVG and transparent PNG paths for the given brand.
        Returns: {'svg': <path or None>, 'png': <path or None>, 'color': <hex>}
        """
        clean_name = name_or_domain.lower().replace("-", "_").replace(" ", "_").strip()
        alias_info = AI_BRAND_ALIASES.get(clean_name, {})
        
        svg_path = None
        png_path = None
        brand_color = alias_info.get("color") or self.get_brand_color(clean_name)

        # 1. Check Bundled Skill Assets First
        bundled_svg = BUNDLED_ASSETS_DIR / "svg" / f"{clean_name}.svg"
        bundled_png = BUNDLED_ASSETS_DIR / "png" / f"{clean_name}.png"

        if bundled_svg.exists():
            svg_path = str(bundled_svg)
        if bundled_png.exists():
            png_path = str(bundled_png)

        # 2. Check User Cache
        cached_svg = USER_CACHE_DIR / f"{clean_name}.svg"
        cached_png = USER_CACHE_DIR / f"{clean_name}.png"

        if not svg_path and cached_svg.exists():
            svg_path = str(cached_svg)
        if not png_path and cached_png.exists():
            png_path = str(cached_png)

        # 3. If icon_id has a collection prefix (e.g. lucide:cpu, mdi:robot) or requested via better-icons
        if ":" in name_or_domain:
            bi_svg = self.fetch_from_better_icons(name_or_domain, brand_color)
            if bi_svg:
                svg_path = bi_svg

        # 4. Query simplepycons if SVG is still missing
        if not svg_path:
            all_icons = self._get_simplepycons()
            if all_icons:
                simple_slug = alias_info.get("simple", clean_name).replace("_", "")
                method_name = f"get_{simple_slug}_icon"
                if hasattr(all_icons, method_name):
                    icon = getattr(all_icons, method_name)()
                    raw_svg = icon.raw_svg
                    # Inject primary brand color into the SVG
                    if not brand_color:
                        brand_color = f"#{icon.primary_color}"
                    if "<path " in raw_svg and 'fill=' not in raw_svg:
                        raw_svg = raw_svg.replace("<path ", f'<path fill="{brand_color}" ', 1)
                    cached_svg.write_text(raw_svg, encoding="utf-8")
                    svg_path = str(cached_svg)

        # 5. Fallback to better-icons search if still missing
        if not svg_path and ":" not in name_or_domain:
            # Try searching in better-icons (e.g. simple-icons:slug or lucide:slug)
            for prefix in ["simple-icons", "lucide", "mdi", "tabler"]:
                bi_candidate = self.fetch_from_better_icons(f"{prefix}:{clean_name.replace('_', '-')}", brand_color)
                if bi_candidate:
                    svg_path = bi_candidate
                    break

        # 6. Generate transparent PNG from SVG if PNG is missing
        if svg_path and not png_path:
            try:
                import cairosvg
                cairosvg.svg2png(
                    url=svg_path,
                    write_to=str(cached_png),
                    output_width=1024,
                    output_height=1024
                )
                png_path = str(cached_png)
            except Exception:
                pass

        # 7. Fallback to Clearbit / Unavatar API for domains/companies if still missing
        if not png_path or not svg_path:
            domain = alias_info.get("domain") or (name_or_domain if "." in name_or_domain else f"{name_or_domain}.com")
            web_path = self.fetch_from_web(domain, clean_name)
            if web_path:
                if web_path.endswith(".png") and not png_path:
                    png_path = web_path
                elif web_path.endswith(".svg") and not svg_path:
                    svg_path = web_path

        return {
            "svg": svg_path,
            "png": png_path,
            "color": brand_color or "#FFFFFF",
            "name": clean_name
        }

    def fetch_from_better_icons(self, icon_id: str, color: Optional[str] = None) -> Optional[str]:
        """Fetches SVG using npx better-icons get <icon_id> [--color <color>]."""
        import subprocess
        clean_file = icon_id.replace(":", "_").replace("/", "_")
        cached_svg = USER_CACHE_DIR / f"{clean_file}.svg"
        if cached_svg.exists():
            return str(cached_svg)
        
        cmd = ["npx", "--yes", "better-icons", "get", icon_id]
        if color and color != "#FFFFFF":
            cmd.extend(["--color", color])
        
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
            stdout = res.stdout.strip()
            if res.returncode == 0 and "<svg" in stdout:
                # Extract clean SVG in case of npx warnings
                svg_start = stdout.find("<svg")
                svg_end = stdout.rfind("</svg>") + 6
                svg_content = stdout[svg_start:svg_end]
                cached_svg.write_text(svg_content, encoding="utf-8")
                return str(cached_svg)
        except Exception:
            pass
        return None

    def fetch_from_web(self, domain: str, save_name: str) -> Optional[str]:
        """Fetches brand icon from unavatar / clearbit and caches it."""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        urls = [
            f"https://unavatar.io/{domain}",
            f"https://logo.clearbit.com/{domain}"
        ]

        for url in urls:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, context=ctx, timeout=4) as r:
                    data = r.read()
                    if not data:
                        continue
                    ext = "svg" if data.startswith(b"<svg") else "png"
                    out_path = USER_CACHE_DIR / f"{save_name}.{ext}"
                    out_path.write_bytes(data)
                    return str(out_path)
            except Exception:
                continue
        return None

    def search_brandfetch(self, brand_name: str, client_id: str) -> Optional[Dict[str, Any]]:
        """Queries Brandfetch Search API by brand name."""
        try:
            import requests
            url = f"https://api.brandfetch.io/v2/search/{brand_name}?c={client_id}"
            res = requests.get(url, timeout=5).json()
            if res and isinstance(res, list):
                match = res[0]
                return {
                    "name": match.get("name"),
                    "domain": match.get("domain"),
                    "icon_url": match.get("icon")
                }
        except Exception:
            pass
        return None


fetcher = BrandIconFetcher()
