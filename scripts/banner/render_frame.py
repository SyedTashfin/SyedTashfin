#!/usr/bin/env python3
"""Render single frames of the banner at explicit times — for previewing a
change without generating the whole 100-frame sequence and GIF.

Usage (from the profile repo root):
    python3 scripts/banner/render_frame.py --out /tmp/frames --times 2.3,4.0
"""
from __future__ import annotations

import argparse
from pathlib import Path

from render import HEIGHT, WIDTH, find_chromium

HTML = Path(__file__).resolve().parent / "index.html"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--times", required=True, help="comma-separated times in seconds")
    ap.add_argument("--scale", type=int, default=1)
    ap.add_argument("--chromium", default=None)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    binary = find_chromium(args.chromium)
    with sync_playwright() as p:
        if binary:
            browser = p.chromium.launch(executable_path=binary, headless=True)
        else:
            browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=args.scale,
        )
        page.goto(f"file://{HTML}")
        for raw in args.times.split(","):
            t = float(raw)
            page.evaluate(f"window.renderBanner({t})")
            page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
            page.screenshot(path=str(out / f"t_{t:0.2f}.png"))
            print(out / f"t_{t:0.2f}.png")
        browser.close()


if __name__ == "__main__":
    main()
