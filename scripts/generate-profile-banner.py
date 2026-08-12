#!/usr/bin/env python3
"""Generate the animated, dependency-light GitHub profile banner.

Requires Pillow. Run from the profile repository root:
    python3 scripts/generate-profile-banner.py
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 400
FPS = 12
FRAMES = 72
OUT_DIR = Path(__file__).resolve().parents[1] / "assets"
FONT_CANDIDATES = [
    os.environ.get("PROFILE_BANNER_FONT", ""),
    "/System/Library/Fonts/SFNSMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "C:/Windows/Fonts/consola.ttf",
]
FONT = next((candidate for candidate in FONT_CANDIDATES if candidate and Path(candidate).exists()), "")

BG = "#07111f"
PANEL = "#0b1728"
GRID = "#142238"
TEXT = "#e6edf7"
MUTED = "#8da2bd"
CYAN = "#2dd4bf"
BLUE = "#60a5fa"
VIOLET = "#a78bfa"
AMBER = "#fbbf24"
ROSE = "#fb7185"
Color = Any


def font(size: int) -> ImageFont.FreeTypeFont:
    if not FONT:
        raise RuntimeError(
            "No monospaced font found. Set PROFILE_BANNER_FONT to a .ttf font path."
        )
    return ImageFont.truetype(FONT, size=size)


def ease(value: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, value)))


def round_rect(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size, fill: Color = TEXT, anchor=None):
    draw.text(xy, value, font=font(size), fill=fill, anchor=anchor)


def base_frame() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    # Subtle engineering grid and ambient glows.
    for x in range(0, WIDTH, 40):
        draw.line((x, 0, x, HEIGHT), fill=GRID, width=1)
    for y in range(0, HEIGHT, 40):
        draw.line((0, y, WIDTH, y), fill=GRID, width=1)
    for r, color in [(210, "#0b2636"), (150, "#12213d")]:
        draw.ellipse((WIDTH - 130 - r, -80 - r, WIDTH - 130 + r, -80 + r), fill=color)

    # Header.
    round_rect(draw, (42, 34, 188, 66), 16, "#10273a", CYAN)
    draw.ellipse((57, 47, 65, 55), fill=CYAN)
    text(draw, (77, 50), "SYEDTASHFIN", 15, CYAN, "lm")
    text(draw, (42, 98), "PLATFORM + BACKEND", 42, TEXT)
    text(draw, (42, 148), "ENGINEER", 42, TEXT)
    text(draw, (43, 207), "BUILDING OBSERVABLE AI SYSTEMS", 20, MUTED)

    # Right-side focus panel.
    round_rect(draw, (820, 34, 1158, 224), 18, PANEL, "#263a55", 2)
    text(draw, (850, 64), "CURRENT FOCUS", 14, MUTED)
    draw.line((850, 91, 1128, 91), fill="#263a55", width=1)

    # Delivery path panel.
    round_rect(draw, (42, 270, 1158, 362), 18, PANEL, "#263a55", 2)
    text(draw, (67, 290), "DELIVERY PATH", 12, MUTED)
    return image


NODES = [
    ("CODE", BLUE),
    ("CI/CD", VIOLET),
    ("K8S", CYAN),
    ("API", AMBER),
    ("TELEMETRY", CYAN),
    ("ROLLBACK", ROSE),
]
FOCUS = [
    ("PLATFORM SYSTEMS", "Kubernetes  /  Helm  /  GitOps", CYAN),
    ("BACKEND SERVICES", "TypeScript  /  Python  /  APIs", BLUE),
    ("OBSERVABLE AI", "OpenTelemetry  /  Prometheus  /  RAG", VIOLET),
]


def make_frame(index: int) -> Image.Image:
    image = base_frame()
    draw = ImageDraw.Draw(image)
    phase = index / FRAMES

    # Focus content cross-fades by using a short vertical slide at segment boundaries.
    segment = (index * len(FOCUS)) // FRAMES
    local = ((index * len(FOCUS)) % FRAMES) / (FRAMES / len(FOCUS))
    title, stack, accent = FOCUS[segment]
    enter = ease(min(local / 0.13, 1.0))
    leave = ease(max((local - 0.86) / 0.14, 0.0))
    offset = int((1 - enter) * 12 - leave * 12)
    alpha = max(0.72, min(enter, 1 - leave))

    def blend(hex_color: str, amount: float) -> tuple[int, int, int]:
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        bg = tuple(int(PANEL[i:i+2], 16) for i in (1, 3, 5))
        return (
            int(bg[0] + (rgb[0] - bg[0]) * amount),
            int(bg[1] + (rgb[1] - bg[1]) * amount),
            int(bg[2] + (rgb[2] - bg[2]) * amount),
        )

    draw.ellipse((850, 116, 862, 128), fill=blend(accent, alpha))
    text(draw, (879, 108 + offset), title, 24, blend(TEXT, alpha))
    text(draw, (850, 155 + offset), stack, 14, blend(MUTED, alpha))
    round_rect(draw, (850, 186, 1128, 199), 6, "#13223a")
    progress = int(278 * local)
    if progress:
        round_rect(draw, (850, 186, 850 + progress, 199), 6, accent)

    # Pipeline line and nodes.
    y = 327
    xs = [100, 280, 460, 640, 820, 1034]
    draw.line((xs[0], y, xs[-1], y), fill="#2a3f5c", width=3)
    for (label, color), x in zip(NODES, xs):
        width = 88 if label not in {"TELEMETRY", "ROLLBACK"} else 126
        round_rect(draw, (x - width // 2, y - 19, x + width // 2, y + 19), 10, "#0e1d31", color, 2)
        text(draw, (x, y), label, 13, TEXT, "mm")

    # Two moving packets reinforce build -> runtime -> feedback.
    for packet_phase, color in [(phase, CYAN), ((phase + 0.5) % 1.0, BLUE)]:
        p = ease(packet_phase)
        px = xs[0] + (xs[-1] - xs[0]) * p
        draw.ellipse((px - 8, y - 8, px + 8, y + 8), fill=color)
        draw.ellipse((px - 15, y - 15, px + 15, y + 15), outline=color, width=2)

    # Animated telemetry loop from rollback back toward code.
    arc_phase = (phase + 0.16) % 1.0
    pulse = int(90 + 120 * (0.5 + 0.5 * math.sin(arc_phase * math.tau)))
    draw.arc((86, 242, 1048, 386), start=188, end=352, fill=(45, 212, 191), width=2)
    text(draw, (1090, 289), "feedback", 11, (pulse, pulse, pulse), "mm")

    # Tiny operational status—not fake metrics.
    text(draw, (1158, 381), "DESIGN  •  BUILD  •  OBSERVE  •  IMPROVE", 11, MUTED, "ra")
    return image


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frames = [make_frame(i) for i in range(FRAMES)]
    # Use a fully legible point in the first focus segment for the static fallback.
    frames[5].save(OUT_DIR / "platform-engineering-banner.png", optimize=True)
    quantized = [frame.quantize(colors=96, method=Image.Quantize.MEDIANCUT) for frame in frames]
    quantized[0].save(
        OUT_DIR / "platform-engineering-banner.gif",
        save_all=True,
        append_images=quantized[1:],
        duration=round(1000 / FPS),
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(OUT_DIR / "platform-engineering-banner.gif")


if __name__ == "__main__":
    main()
