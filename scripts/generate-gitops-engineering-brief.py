#!/usr/bin/env python3
"""Generate the recruiter-facing GitOps engineering brief.

Usage:
  uv run --with reportlab==4.4.3 python scripts/generate-gitops-engineering-brief.py
"""
from pathlib import Path
from textwrap import wrap

from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import portrait

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "from-commit-to-observable-rollback.pdf"
W, H = 720, 900
PAGE = portrait((W, H))

BG = HexColor("#07111F")
PANEL = HexColor("#0E1C2E")
PANEL_2 = HexColor("#12243A")
TEXT = HexColor("#ECF4FF")
MUTED = HexColor("#9FB1C7")
CYAN = HexColor("#3DD6D0")
BLUE = HexColor("#5CA7FF")
GREEN = HexColor("#58D68D")
AMBER = HexColor("#F2B84B")
RED = HexColor("#FF7B7B")
VIOLET = HexColor("#A98BFF")
GRID = HexColor("#14243A")

URL_CASE = "https://syedtashfin.com/case-studies/cicd-gitops-multitenant-kubernetes-saas"
URL_REPO = "https://github.com/SyedTashfin/Outsight-MultiTenant-GitOps-Lab"
URL_PROFILE = "https://github.com/SyedTashfin"


def background(c, page_no, section):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GRID)
    c.setLineWidth(0.4)
    for x in range(0, W + 1, 36):
        c.line(x, 0, x, H)
    for y in range(0, H + 1, 36):
        c.line(0, y, W, y)
    c.setFillColor(CYAN)
    c.circle(48, 858, 4, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(62, 854, section.upper())
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawRightString(672, 854, f"SYEDTASHFIN.COM  /  {page_no:02d}")


def title(c, text, y=805, size=30, color=TEXT):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    lines = wrap(text, width=max(18, int(44 * 30 / size)))
    for line in lines:
        c.drawString(48, y, line)
        y -= size * 1.15
    return y


def paragraph(c, text, x, y, width=620, size=12, leading=18, color=MUTED, font="Helvetica"):
    c.setFillColor(color)
    c.setFont(font, size)
    chars = max(20, int(width / (size * 0.53)))
    for line in wrap(text, width=chars):
        c.drawString(x, y, line)
        y -= leading
    return y


def label(c, text, x, y, color=CYAN):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, text.upper())


def card(c, x, y, w, h, heading, body=None, accent=CYAN, bullets=None):
    c.setFillColor(PANEL)
    c.roundRect(x, y, w, h, 12, fill=1, stroke=0)
    c.setFillColor(accent)
    c.roundRect(x, y, 5, h, 2, fill=1, stroke=0)
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x + 20, y + h - 28, heading)
    ty = y + h - 50
    if body:
        ty = paragraph(c, body, x + 20, ty, w - 40, 10, 14)
    if bullets:
        c.setFont("Helvetica", 10)
        for bullet in bullets:
            c.setFillColor(accent)
            c.circle(x + 24, ty + 3, 2, fill=1, stroke=0)
            c.setFillColor(MUTED)
            for i, line in enumerate(wrap(bullet, width=max(20, int((w - 52) / 5.3)))):
                c.drawString(x + 34, ty, line)
                ty -= 14
            ty -= 5


def pill(c, x, y, text, color=BLUE):
    fs = 8
    width = stringWidth(text, "Helvetica-Bold", fs) + 20
    c.setFillColor(PANEL_2)
    c.roundRect(x, y, width, 24, 12, fill=1, stroke=0)
    c.setStrokeColor(color)
    c.setLineWidth(0.8)
    c.roundRect(x, y, width, 24, 12, fill=0, stroke=1)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", fs)
    c.drawCentredString(x + width / 2, y + 8, text)
    return width


def footer_link(c, label_text, url, x, y, width):
    c.setFillColor(PANEL_2)
    c.roundRect(x, y, width, 40, 9, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 14, y + 15, label_text)
    c.linkURL(url, (x, y, x + width, y + 40), relative=0)


def node(c, x, y, w, h, head, sub, color):
    c.setFillColor(PANEL)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=0)
    c.setStrokeColor(color)
    c.setLineWidth(1.4)
    c.roundRect(x, y, w, h, 10, fill=0, stroke=1)
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x + w / 2, y + h - 22, head)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    for i, line in enumerate(wrap(sub, width=max(12, int(w / 5.0)))):
        c.drawCentredString(x + w / 2, y + h - 38 - i * 10, line)


def arrow(c, x1, y1, x2, y2, color=MUTED, dashed=False):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(1.4)
    if dashed:
        c.setDash(4, 3)
    c.line(x1, y1, x2, y2)
    c.setDash()
    if abs(x2 - x1) >= abs(y2 - y1):
        s = 1 if x2 >= x1 else -1
        c.line(x2, y2, x2 - 7 * s, y2 + 4)
        c.line(x2, y2, x2 - 7 * s, y2 - 4)
    else:
        s = 1 if y2 >= y1 else -1
        c.line(x2, y2, x2 - 4, y2 - 7 * s)
        c.line(x2, y2, x2 + 4, y2 - 7 * s)


def page_cover(c):
    background(c, 1, "Engineering brief")
    label(c, "Production-style platform lab", 48, 790)
    y = title(c, "From commit to observable rollback", 750, 38)
    y -= 10
    paragraph(c, "A reviewable GitOps delivery path for a multi-tenant Kubernetes service.", 48, y, 580, 16, 23, TEXT, "Helvetica")
    c.setFillColor(PANEL)
    c.roundRect(48, 390, 624, 210, 18, fill=1, stroke=0)
    steps = [
        ("CODE", CYAN), ("TEST", BLUE), ("IMAGE", VIOLET),
        ("DESIRED STATE", AMBER), ("ROLLOUT", GREEN), ("TELEMETRY", RED),
    ]
    x, y0 = 70, 495
    for i, (txt, col) in enumerate(steps):
        w = 78 if txt not in {"DESIRED STATE", "TELEMETRY"} else 96
        c.setFillColor(PANEL_2)
        c.roundRect(x, y0, w, 50, 9, fill=1, stroke=0)
        c.setStrokeColor(col)
        c.roundRect(x, y0, w, 50, 9, fill=0, stroke=1)
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + w / 2, y0 + 21, txt)
        if i < len(steps) - 1:
            arrow(c, x + w + 4, y0 + 25, x + w + 20, y0 + 25, MUTED)
        x += w + 28
    paragraph(c, "The artifact is immutable. Desired state is reviewed. The cluster reconciles. Prometheus decides whether the release progresses or rolls back.", 70, 455, 570, 11, 16)
    label(c, "Built and documented by", 48, 300, BLUE)
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(48, 267, "Syed Mohammad Shah Mostafa (Tash)")
    paragraph(c, "Platform & Backend Engineer building observable AI systems | Paris", 48, 240, 600, 11, 16)
    footer_link(c, "OPEN CASE STUDY", URL_CASE, 48, 74, 196)
    footer_link(c, "INSPECT REPOSITORY", URL_REPO, 260, 74, 196)
    footer_link(c, "VIEW GITHUB PROFILE", URL_PROFILE, 472, 74, 200)


def page_path(c):
    background(c, 2, "Delivery architecture")
    title(c, "The delivery path", 800, 30)
    paragraph(c, "CI produces evidence and an artifact. Git carries the reviewed intent. Argo CD owns reconciliation inside the cluster.", 48, 744, 620, 12, 18)
    nodes = [
        (52, 605, 120, 80, "GitHub", "source + tests", CYAN),
        (212, 605, 120, 80, "Actions", "build + scan + publish", BLUE),
        (372, 605, 120, 80, "GHCR", "immutable multi-arch image", VIOLET),
        (532, 605, 136, 80, "Git desired state", "Helm values update", AMBER),
        (132, 420, 150, 90, "Argo CD", "pull + reconcile", AMBER),
        (362, 420, 150, 90, "Argo Rollout", "progressive delivery", GREEN),
        (262, 235, 150, 90, "Prometheus", "analysis query", RED),
    ]
    for n in nodes:
        node(c, *n)
    arrow(c, 172, 645, 212, 645, CYAN)
    arrow(c, 332, 645, 372, 645, BLUE)
    arrow(c, 492, 645, 532, 645, VIOLET)
    arrow(c, 600, 605, 250, 510, AMBER)
    arrow(c, 282, 465, 362, 465, GREEN)
    arrow(c, 437, 420, 352, 325, RED, dashed=True)
    arrow(c, 337, 325, 412, 420, RED, dashed=True)
    card(c, 48, 80, 624, 105, "Boundary that matters", "The workflow does not use CI credentials to push arbitrary runtime changes into the cluster. CI updates versioned intent; the reconciler applies it.", CYAN)


def page_tenancy(c):
    background(c, 3, "Tenancy and controls")
    title(c, "Tenant differences stay reviewable", 800, 30)
    paragraph(c, "One chart carries shared behavior. Per-tenant values express controlled differences without copying entire manifest trees.", 48, 744, 620, 12, 18)
    node(c, 250, 620, 220, 82, "Shared Helm chart", "templates + defaults", CYAN)
    node(c, 72, 450, 240, 110, "Tenant A values", "namespace, quotas, limits, routing", BLUE)
    node(c, 408, 450, 240, 110, "Tenant B values", "namespace, quotas, limits, routing", VIOLET)
    arrow(c, 310, 620, 210, 560, BLUE)
    arrow(c, 410, 620, 528, 560, VIOLET)
    controls = [
        ("RBAC", "service identity and permissions", CYAN),
        ("NetworkPolicy", "profile-dependent traffic boundaries", RED),
        ("Quota", "namespace resource ceilings", AMBER),
        ("Limits", "container requests and caps", GREEN),
    ]
    x = 48
    for head, body, col in controls:
        card(c, x, 260, 144, 125, head, body, col)
        x += 160
    card(c, 48, 80, 624, 125, "What this proves", bullets=[
        "tenant configuration can be reviewed as data",
        "shared templates reduce drift between tenant deployments",
        "security and resource controls are visible in the rendered manifests",
    ], accent=GREEN)


def page_rollout(c):
    background(c, 4, "Progressive delivery")
    title(c, "A release should be able to fail safely", 800, 30)
    paragraph(c, "The rollout controller changes traffic in steps. Prometheus supplies a measurable health signal before promotion.", 48, 744, 620, 12, 18)
    stages = [
        ("1", "Deploy candidate", "new ReplicaSet", BLUE),
        ("2", "Shift traffic", "canary step", VIOLET),
        ("3", "Query health", "Prometheus analysis", RED),
        ("4A", "Promote", "health passes", GREEN),
        ("4B", "Abort / roll back", "health fails", AMBER),
    ]
    y = 630
    for i, (num, head, sub, col) in enumerate(stages[:3]):
        c.setFillColor(col)
        c.circle(86, y + 25, 22, fill=1, stroke=0)
        c.setFillColor(BG)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(86, y + 21, num)
        card(c, 122, y - 10, 500, 70, head, sub, col)
        if i < 2:
            arrow(c, 86, y - 15, 86, y - 42, MUTED)
        y -= 120
    arrow(c, 360, 390, 250, 265, GREEN)
    arrow(c, 385, 390, 500, 265, AMBER)
    card(c, 72, 150, 260, 105, stages[3][1], stages[3][2], GREEN)
    card(c, 388, 150, 260, 105, stages[4][1], stages[4][2], AMBER)
    label(c, "Operational principle", 48, 100, CYAN)
    paragraph(c, "Telemetry is part of the release decision, not a dashboard added after deployment.", 48, 78, 620, 11, 16, TEXT)


def page_decisions(c):
    background(c, 5, "Engineering decisions")
    title(c, "The tool list is not the argument", 800, 30)
    paragraph(c, "The useful signal is where responsibilities stop, how failures are handled, and which claims can be reproduced.", 48, 744, 620, 12, 18)
    card(c, 48, 555, 300, 150, "CI builds; Git declares", bullets=[
        "publish immutable artifacts",
        "update reviewed desired state",
        "leave cluster reconciliation to Argo CD",
    ], accent=CYAN)
    card(c, 372, 555, 300, 150, "Configuration is data", bullets=[
        "share templates",
        "keep tenant differences explicit",
        "render and lint before deployment",
    ], accent=BLUE)
    card(c, 48, 365, 300, 150, "Health has a failure path", bullets=[
        "query Prometheus during rollout",
        "promote only when analysis passes",
        "make abort behavior inspectable",
    ], accent=RED)
    card(c, 372, 365, 300, 150, "Evidence accompanies claims", bullets=[
        "source paths and workflows",
        "tests and verification commands",
        "limitations published beside outcomes",
    ], accent=GREEN)
    card(c, 48, 105, 624, 195, "Trade-offs", bullets=[
        "A local or single-cluster lab makes the control flow reproducible, but it does not prove multi-cluster operations.",
        "Prometheus analysis demonstrates measurable release gates, but synthetic or lab traffic cannot stand in for production SLO history.",
        "Git review improves traceability, but it also adds a repository update step and requires careful secret boundaries.",
    ], accent=AMBER)


def page_limits(c):
    background(c, 6, "Verification and limits")
    title(c, "What you can inspect", 800, 30)
    paragraph(c, "This brief is an entry point. The repository contains the implementation and the case study explains the reasoning.", 48, 744, 620, 12, 18)
    card(c, 48, 545, 300, 155, "Verification paths", bullets=[
        "Python tests and Ruff",
        "Helm lint for both tenants",
        "workflow and manifest review",
        "reproducible quick-start commands",
    ], accent=GREEN)
    card(c, 372, 545, 300, 155, "Public evidence", bullets=[
        "Argo Rollout templates",
        "Prometheus analysis configuration",
        "RBAC, NetworkPolicy, quotas, limits",
        "GitHub Actions and GHCR path",
    ], accent=BLUE)
    card(c, 48, 310, 624, 180, "What this does not claim", bullets=[
        "No claim of production traffic, enterprise scale, or EKS deployment.",
        "No claim of reduced MTTR or real on-call incident ownership.",
        "No claim that a production-style lab replaces operating a live platform.",
        "The project demonstrates design choices, implementation, and verification within its stated scope.",
    ], accent=RED)
    label(c, "Continue the review", 48, 235, CYAN)
    footer_link(c, "READ THE FULL CASE STUDY", URL_CASE, 48, 165, 296)
    footer_link(c, "INSPECT SOURCE AND TESTS", URL_REPO, 376, 165, 296)
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(48, 105, "Platform & Backend Engineer building observable AI systems")
    paragraph(c, "Syed Mohammad Shah Mostafa (Tash) | Paris, France", 48, 80, 620, 10, 14)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("From commit to observable rollback")
    c.setAuthor("Syed Mohammad Shah Mostafa (Tash)")
    c.setSubject("GitOps, Kubernetes, progressive delivery, and observability engineering brief")
    for fn in (page_cover, page_path, page_tenancy, page_rollout, page_decisions, page_limits):
        fn(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
