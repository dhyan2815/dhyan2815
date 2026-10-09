"""Render design/profile-card.html to assets/profile-card.png.

Usage (from the repo root):
    pip install playwright && python -m playwright install chromium
    python design/render.py
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "design" / "profile-card.html"
OUT = ROOT / "assets" / "profile-card.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    # 2x scale keeps text crisp when GitHub scales the image down
    page = browser.new_page(viewport={"width": 1200, "height": 760}, device_scale_factor=2)
    page.goto(SRC.as_uri())
    page.evaluate("document.fonts.ready")
    OUT.parent.mkdir(exist_ok=True)
    page.locator("#card").screenshot(path=str(OUT), omit_background=True)
    browser.close()

print(f"Wrote {OUT.relative_to(ROOT)}")
