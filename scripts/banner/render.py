#!/usr/bin/env python3
"""Render the animated profile banner (scripts/banner/index.html) to a PNG
frame sequence using headless Chromium via Playwright, for later GIF assembly.

Usage (from the profile repo root):
    python3 scripts/banner/render.py --out /tmp/banner-frames
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

WIDTH, HEIGHT = 1200, 400
DURATION = 5.0
FPS = 20
SCALE = 2  # render at 2x for crisp text, downscale in ffmpeg

ROOT = Path(__file__).resolve().parents[2]
HTML = Path(__file__).resolve().parent / "index.html"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--chromium", default="/opt/homebrew/bin/chromium")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(executable_path=args.chromium, headless=True)
        except Exception as e:  # fall back to playwright-bundled browser
            print(f"system chromium failed ({e}); trying bundled", file=sys.stderr)
            browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=SCALE,
        )
        page.goto(f"file://{HTML}")

        n = round(DURATION * FPS)
        for i in range(n):
            t = i / FPS
            page.evaluate(f"window.renderBanner({t})")
            # force two rAFs so the frame is painted before capture
            page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
            page.screenshot(path=str(out / f"frame_{i:03d}.png"))

        browser.close()

    print(f"wrote {n} frames to {out}")


if __name__ == "__main__":
    main()
