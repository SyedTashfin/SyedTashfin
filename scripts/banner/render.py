#!/usr/bin/env python3
"""Render the animated profile banner (scripts/banner/index.html) to a PNG
frame sequence using headless Chromium via Playwright, for later GIF assembly.

Usage (from the profile repo root):
    python3 scripts/banner/render.py --out /tmp/banner-frames
    ffmpeg -framerate 20 -i /tmp/banner-frames/frame_%03d.png \
        -vf "scale=1200:400:flags=lanczos,split[a][b];[a]palettegen=max_colors=224:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle" \
        -loop 0 assets/platform-engineering-banner.gif

Chromium is auto-detected (a bundled Playwright build, then common system
paths). Override with --chromium or the PROFILE_BANNER_CHROMIUM env var.
"""
from __future__ import annotations

import argparse
import glob
import os
import shutil
import sys
from pathlib import Path

WIDTH, HEIGHT = 1200, 400
DURATION = 5.0
FPS = 20
SCALE = 2  # render at 2x for crisp text, downscale in ffmpeg

ROOT = Path(__file__).resolve().parents[2]
HTML = Path(__file__).resolve().parent / "index.html"

BROWSER_GLOBS = [
    # macOS Playwright builds (any cached version)
    "~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac*/chrome-headless-shell",
    "~/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
    # Linux Playwright builds
    "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/chrome-headless-shell",
    "~/.cache/ms-playwright/chromium-*/chrome-linux/chrome",
]


def find_chromium(explicit: str | None = None) -> str | None:
    """Return a runnable Chromium binary, or None to let Playwright decide."""
    for candidate in (explicit, os.environ.get("PROFILE_BANNER_CHROMIUM")):
        if candidate:
            if Path(candidate).exists():
                return candidate
            print(f"warning: {candidate} does not exist; auto-detecting", file=sys.stderr)
    for pattern in BROWSER_GLOBS:
        for match in sorted(glob.glob(os.path.expanduser(pattern)), reverse=True):
            if os.access(match, os.X_OK):
                return match
    for name in ("chromium", "google-chrome", "chrome", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--chromium", default=None)
    ap.add_argument("--duration", type=float, default=DURATION)
    ap.add_argument("--fps", type=int, default=FPS)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    binary = find_chromium(args.chromium)
    with sync_playwright() as p:
        if binary:
            print(f"chromium: {binary}", file=sys.stderr)
            browser = p.chromium.launch(executable_path=binary, headless=True)
        else:
            print("no chromium binary found; using the Playwright default", file=sys.stderr)
            browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=SCALE,
        )
        page.goto(f"file://{HTML}")

        n = round(args.duration * args.fps)
        for i in range(n):
            t = i / args.fps
            page.evaluate(f"window.renderBanner({t})")
            # force two rAFs so the frame is painted before capture
            page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
            page.screenshot(path=str(out / f"frame_{i:03d}.png"))

        browser.close()

    print(f"wrote {n} frames to {out}")


if __name__ == "__main__":
    main()
