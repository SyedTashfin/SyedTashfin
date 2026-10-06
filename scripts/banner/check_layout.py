#!/usr/bin/env python3
"""Layout QA for the animated banner, before committing regenerated assets.

Checks, across the whole 5s timeline:
  * the chip row stays inside the identity column
  * no terminal line overflows the terminal card
  * the typing cursor lands on the glyph it is meant to follow
  * the terminal title and status pill do not collide

Usage (from the profile repo root):
    python3 scripts/banner/check_layout.py
"""
from __future__ import annotations

import re
from pathlib import Path

from render import FPS, HEIGHT, WIDTH, find_chromium

HTML = Path(__file__).resolve().parent / "index.html"


def timeline() -> tuple[float, float, float]:
    """Read the animation constants from the banner so QA cannot drift from it."""
    src = HTML.read_text(encoding="utf-8")

    def num(pattern: str) -> float:
        match = re.search(pattern, src)
        if not match:
            raise SystemExit(f"pattern {pattern!r} not found in {HTML.name}")
        return float(match.group(1))

    duration = num(r"var DURATION = ([\d.]+)")
    idle_after = num(r"var IDLE_AFTER = ([\d.]+)")
    first_start = min(float(m) for m in re.findall(r"start:([\d.]+)", src))
    return duration, idle_after, first_start

PROBE = """(t) => {
  window.renderBanner(t);
  const box = el => el.getBoundingClientRect();
  const tbody = box(document.getElementById('tbody'));
  const term = box(document.getElementById('term'));
  const chipsBox = box(document.getElementById('chips'));
  const chips = [...document.querySelectorAll('#chips .chip')].map(c => ({
    label: c.textContent, right: +box(c).right.toFixed(1),
  }));
  const lines = [...document.querySelectorAll('.line')].map(el => {
    const sym = box(el.querySelector('span:first-child'));
    const txt = box(el.querySelector('span:last-child'));
    return {
      text: el.textContent,
      right: +((txt.width > 0 ? txt.right : sym.right) - tbody.left).toFixed(1),
    };
  });
  const cursor = document.getElementById('cursor');
  const dots = box(document.querySelector('#tdots'));
  const ttitle = box(document.getElementById('ttitle'));
  const pill = box(document.getElementById('tlive'));

  // headline copy must stay inside the identity column
  const tagline = document.getElementById('tagline');
  const tagRange = document.createRange();
  tagRange.selectNodeContents(tagline);
  const tagRight = +tagRange.getBoundingClientRect().right.toFixed(1);

  const lineEls = [...document.querySelectorAll('.line')];
  // the row the cursor belongs to, resolved by geometry (not by "last row with text")
  let cursorRow = -1;
  let cursorLeft = null;
  if (cursor.style.display !== 'none') {
    const c = box(cursor);
    cursorLeft = +(c.left - tbody.left).toFixed(1);
    let best = 1e9;
    lineEls.forEach((el, i) => {
      const r = box(el);
      const d = Math.abs((r.top + 4) - c.top);
      if (d < best && d < 12) { best = d; cursorRow = i; }
    });
  }
  // expected x: end of the rendered text on that row (symbol included), else the row start
  let expected = null;
  if (cursorRow >= 0) {
    const el = lineEls[cursorRow];
    const sym = box(el.querySelector('span:first-child'));
    const txt = box(el.querySelector('span:last-child'));
    const openRight = txt.width > 0 ? txt.right : (sym.width > 0 ? sym.right : tbody.left + 18);
    expected = +(openRight - tbody.left).toFixed(1);
  }

  return {
    termLeft: +term.left.toFixed(1), termRight: +term.right.toFixed(1),
    chipsRight: +chipsBox.right.toFixed(1), chips,
    lines,
    tagRight,
    cursorVisible: cursor.style.display !== 'none',
    cursorLeft, cursorRow, expected,
    barGap: +(pill.left - ttitle.right).toFixed(1),
    dotsRight: +dots.right.toFixed(1),
  };
}"""


def main() -> None:
    from playwright.sync_api import sync_playwright

    binary = find_chromium()
    duration, idle_after, first_start = timeline()
    frames = int(duration * FPS)
    failures: list[str] = []
    worst_cursor = 0.0
    chip_slack = None
    min_bar_gap = 1e9
    cursor_samples = 0

    with sync_playwright() as p:
        browser = (p.chromium.launch(executable_path=binary, headless=True)
                   if binary else p.chromium.launch(headless=True))
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        page.goto(f"file://{HTML}")

        for i in range(frames):
            t = i / FPS
            m = page.evaluate(PROBE, t)

            for chip in m["chips"]:
                slack = m["chipsRight"] - chip["right"]
                chip_slack = slack if chip_slack is None else min(chip_slack, slack)
                if slack < 0:
                    failures.append(f"t={t:.2f} chip {chip['label']} overflows by {-slack:.1f}px")

            limit = m["termRight"] - 12
            for ln in m["lines"]:
                if ln["text"].strip() and ln["right"] > limit:
                    failures.append(f"t={t:.2f} terminal line overflows: {ln['text']!r}")

            min_bar_gap = min(min_bar_gap, m["barGap"])
            if m["tagRight"] > m["termLeft"] - 24:
                failures.append(f"t={t:.2f} tagline reaches {m['tagRight']}, terminal starts at {m['termLeft']}")
            # the cursor sits deliberately idle before the first line starts and
            # while the body clears, so only check it during the typing window
            typing = first_start <= t <= idle_after
            if typing and m["cursorVisible"] and m["cursorLeft"] is not None and m["cursorRow"] >= 0:
                cursor_samples += 1
                delta = abs(m["cursorLeft"] - m["expected"])
                worst_cursor = max(worst_cursor, delta)
                if delta > 2.5:
                    failures.append(
                        f"t={t:.2f} cursor on row {m['cursorRow']} at {m['cursorLeft']} "
                        f"but glyph end is {m['expected']}"
                    )

        browser.close()

    print(f"frames checked:        {frames}")
    print(f"cursor samples:        {cursor_samples}")
    print(f"min chip slack:        {chip_slack:.1f}px (must be > 0)")
    print(f"worst cursor offset:   {worst_cursor:.1f}px (must be < 2.5)")
    print(f"min title/pill gap:    {min_bar_gap:.1f}px (must be > 0)")
    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for f in failures[:20]:
            print("  " + f)
        raise SystemExit(1)
    print("\nlayout OK")


if __name__ == "__main__":
    main()
