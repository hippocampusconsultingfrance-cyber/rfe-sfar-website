# -*- coding: utf-8 -*-
"""
Shared style module for the "Medical Guidelines" SFAR/SRLF/HAS fiche PDFs.

RECONSTRUCTED 2026-09-04: the original style.py was lost from the /tmp scratchpad
(the one file in the project untouched since day 1, apparently swept by a tmp-cleanup
pass during a long idle gap while every other file's mtime was recent). Rebuilt by
reverse-engineering the exact call signatures used across all ~50 fiche_*.py scripts
(grep of header_band/footer_band/section_bar/info_panel/grade_chip/pstyle/icon_*
call sites) and by pixel-sampling colors/margins directly from previously-rendered
ground-truth PDFs still present in output/ (e.g. Fiche_SFAR_SRLF_Insuffisance_Renale_
Aigue_2015.pdf, rendered before the loss). Colors below are exact (sampled RGB);
font sizes/leadings are best-effort reconstructions tuned by visual comparison
against the same ground-truth renders.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.graphics.shapes import Drawing, String, Rect, Path, Circle, Group
from reportlab.pdfgen import canvas as _canvas_mod

# ---------------------------------------------------------------------------
# Palette (sampled directly from ground-truth rendered PDF pixels)
# ---------------------------------------------------------------------------
def _c(r, g, b):
    return colors.Color(r / 255.0, g / 255.0, b / 255.0)

NAVY = _c(10, 59, 84)
TEAL_DARK = _c(10, 91, 102)
TEAL = _c(14, 124, 133)
GREEN = _c(45, 138, 86)
RED = _c(182, 40, 45)
AMBER = _c(200, 121, 12)
GREY = _c(107, 121, 128)
GREY_LIGHT = _c(216, 227, 227)
BG_PANEL = _c(239, 246, 246)
WHITE = colors.white
BLACK = colors.black
INK = _c(18, 35, 43)

GREEN_LIGHT = _c(225, 239, 230)
RED_LIGHT = _c(245, 222, 223)
AMBER_LIGHT = _c(245, 233, 211)

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"

PAGE_W, PAGE_H = A4
MARGIN = 14 * mm

# ---------------------------------------------------------------------------
# Grade-chip color map: label -> (background, text)
# ---------------------------------------------------------------------------
GRADE_COLORS = {
    "1+": (GREEN, WHITE),
    "1-": (RED, WHITE),
    "2+": (TEAL, WHITE),
    "2-": (AMBER, WHITE),
    "AE": (GREY, WHITE),
    "?": (GREY, WHITE),
}

# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------
def pstyle(name, base=None, **kw):
    """Factory used both here and locally in individual fiche scripts to derive
    one-off paragraph styles from a base style."""
    parent = base if base is not None else _BASE
    st = ParagraphStyle(name, parent=parent)
    for k, v in kw.items():
        setattr(st, k, v)
    return st

_BASE = ParagraphStyle(
    "base", fontName=FONT_REGULAR, fontSize=8.6, leading=11, textColor=INK,
    alignment=TA_LEFT, spaceBefore=0, spaceAfter=0,
)

S_BODY = pstyle("body", fontSize=9.2, leading=12.4, textColor=INK)
S_BODY_SM = pstyle("body_sm", fontSize=8.3, leading=11.2, textColor=INK)
S_CELL = pstyle("cell", fontSize=8.6, leading=10.8, textColor=INK)
S_CELL_B = pstyle("cell_b", fontSize=8.6, leading=10.8, textColor=INK, fontName=FONT_BOLD)
S_CELL_C = pstyle("cell_c", fontSize=8.6, leading=10.8, textColor=INK, alignment=TA_CENTER)
S_H2 = pstyle("h2", fontSize=10.4, leading=12.6, textColor=NAVY, fontName=FONT_BOLD)
S_HEAD_W = pstyle("head_w", fontSize=8.2, leading=10, textColor=WHITE, fontName=FONT_BOLD)
S_HEAD_W_C = pstyle("head_w_c", fontSize=8.2, leading=10, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
S_NOTE = pstyle("note", fontSize=7.8, leading=10, textColor=GREY, fontName=FONT_ITALIC)
S_SOURCE = pstyle("source", fontSize=6.6, leading=8.6, textColor=GREY)
S_BADGE_HEAD = pstyle("badge_head", fontSize=7.8, leading=9.6, textColor=INK)

# ---------------------------------------------------------------------------
# Small drawing helpers
# ---------------------------------------------------------------------------
def _rounded_rect(x, y, w, h, radius, fillColor, strokeColor, strokeWidth=0):
    p = Path(fillColor=fillColor, strokeColor=strokeColor, strokeWidth=strokeWidth)
    r = min(radius, w / 2.0, h / 2.0)
    k = 0.5523 * r
    p.moveTo(x + r, y)
    p.lineTo(x + w - r, y)
    p.curveTo(x + w - r + k, y, x + w, y + r - k, x + w, y + r)
    p.lineTo(x + w, y + h - r)
    p.curveTo(x + w, y + h - r + k, x + w - r + k, y + h, x + w - r, y + h)
    p.lineTo(x + r, y + h)
    p.curveTo(x + r - k, y + h, x, y + h - r + k, x, y + h - r)
    p.lineTo(x, y + r)
    p.curveTo(x, y + r - k, x + r - k, y, x + r, y)
    p.closePath()
    return p

# ---------------------------------------------------------------------------
# Grade chip (small colored badge flowable, used inside table cells)
# ---------------------------------------------------------------------------
def grade_chip(label, width=15 * mm, fontsize=8.4, height=6.2 * mm):
    bg, fg = GRADE_COLORS.get(label, (GREY, WHITE))
    st = pstyle("chip_%s_%s" % (label, fontsize), fontSize=fontsize, leading=fontsize + 1,
                textColor=fg, fontName=FONT_BOLD, alignment=TA_CENTER)
    t = Table([[Paragraph(label, st)]], colWidths=[width], rowHeights=[height])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 1),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1),
    ]))
    return t

# ---------------------------------------------------------------------------
# Info panel (bordered/tinted callout box)
# ---------------------------------------------------------------------------
def info_panel(flowable, bg=BG_PANEL, border=TEAL, pad=3.2 * mm):
    content = flowable if isinstance(flowable, list) else [flowable]
    t = Table([[content]], colWidths=[PAGE_W - 2 * MARGIN - 2 * pad])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 1.1, border),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, border),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t

# ---------------------------------------------------------------------------
# Section bar (colored full-width title band, used mid-page)
# ---------------------------------------------------------------------------
def section_bar(title, color=TEAL_DARK, height=7.6 * mm, fontsize=11.2):
    st = pstyle("secbar_%s" % fontsize, fontSize=fontsize, leading=fontsize + 1.5,
                textColor=WHITE, fontName=FONT_BOLD)
    t = Table([[Paragraph(title, st)]], colWidths=[PAGE_W - 2 * MARGIN], rowHeights=[height])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t

# ---------------------------------------------------------------------------
# Icons (simple white glyphs drawn on the header band)
# ---------------------------------------------------------------------------
def icon_kidney(c, x, y, size):
    c.saveState()
    c.setFillColor(WHITE)
    c.setStrokeColor(WHITE)
    r = size * 0.26
    c.circle(x, y + r * 0.5, r, fill=1, stroke=0)
    c.circle(x + r * 0.75, y - r * 0.3, r * 0.7, fill=1, stroke=0)
    c.setFillColor(TEAL_DARK)
    c.circle(x + r * 0.1, y + r * 0.3, r * 0.38, fill=1, stroke=0)
    c.restoreState()

def icon_shield(c, x, y, size):
    c.saveState()
    c.setFillColor(WHITE)
    p = c.beginPath()
    r = size * 0.42
    p.moveTo(x, y + r)
    p.curveTo(x + r * 0.8, y + r * 0.75, x + r * 0.8, y + r * 0.2, x + r * 0.8, y - r * 0.1)
    p.curveTo(x + r * 0.8, y - r * 0.75, x + r * 0.3, y - r * 1.0, x, y - r * 1.15)
    p.curveTo(x - r * 0.3, y - r * 1.0, x - r * 0.8, y - r * 0.75, x - r * 0.8, y - r * 0.1)
    p.curveTo(x - r * 0.8, y + r * 0.2, x - r * 0.8, y + r * 0.75, x, y + r)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

def icon_pill(c, x, y, size):
    c.saveState()
    c.setFillColor(WHITE)
    w, h = size * 0.85, size * 0.36
    c.roundRect(x - w / 2, y - h / 2, w, h, h / 2, fill=1, stroke=0)
    c.setFillColor(TEAL_DARK)
    c.rect(x - 0.6, y - h / 2, 1.2, h, fill=1, stroke=0)
    c.restoreState()

def icon_liver(c, x, y, size):
    c.saveState()
    c.setFillColor(WHITE)
    r = size * 0.3
    c.ellipse(x - r * 1.05, y - r * 0.55, x + r * 0.65, y + r * 0.85, fill=1, stroke=0)
    c.ellipse(x - r * 0.15, y - r * 0.85, x + r * 1.05, y + r * 0.15, fill=1, stroke=0)
    c.setFillColor(TEAL_DARK)
    c.circle(x - r * 0.1, y - r * 0.05, r * 0.16, fill=1, stroke=0)
    c.restoreState()

def icon_drop(c, x, y, size):
    c.saveState()
    c.setFillColor(WHITE)
    r = size * 0.34
    p = c.beginPath()
    p.moveTo(x, y + r * 1.3)
    p.curveTo(x + r * 1.05, y + r * 0.15, x + r * 0.95, y - r * 1.05, x, y - r * 1.05)
    p.curveTo(x - r * 0.95, y - r * 1.05, x - r * 1.05, y + r * 0.15, x, y + r * 1.3)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

# ---------------------------------------------------------------------------
# Header / footer bands (drawn directly on the canvas via onPage callbacks)
# ---------------------------------------------------------------------------
def header_band(canvas, doc, top_label, title, subtitle, icon_fn=None, color=TEAL_DARK):
    canvas.saveState()
    band_h = 26 * mm
    canvas.setFillColor(color)
    canvas.rect(0, PAGE_H - band_h, PAGE_W, band_h, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - band_h - 1.6 * mm, PAGE_W, 1.6 * mm, fill=1, stroke=0)

    canvas.setFillColor(WHITE)
    canvas.setFont(FONT_BOLD, 8.6)
    canvas.drawString(MARGIN, PAGE_H - 9 * mm, top_label.upper())

    icon_reserve = 16 * mm
    max_title_w = PAGE_W - 2 * MARGIN - icon_reserve
    title_size = 16.5
    while title_size > 11 and canvas.stringWidth(title, FONT_BOLD, title_size) > max_title_w:
        title_size -= 0.5
    canvas.setFont(FONT_BOLD, title_size)
    canvas.drawString(MARGIN, PAGE_H - 16.4 * mm, title)

    canvas.setFont(FONT_REGULAR, 10.6)
    canvas.drawString(MARGIN, PAGE_H - 22.4 * mm, subtitle)

    if icon_fn is not None:
        icon_fn(canvas, PAGE_W - MARGIN - 7 * mm, PAGE_H - band_h / 2)
    canvas.restoreState()

def footer_band(canvas, doc, source_text, page_indicator):
    canvas.saveState()
    y0 = 15 * mm
    canvas.setStrokeColor(GREY_LIGHT)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, y0, PAGE_W - MARGIN, y0)

    canvas.setFont(FONT_BOLD, 7.6)
    canvas.setFillColor(GREY)
    canvas.drawString(MARGIN, y0 - 4.2 * mm, "Fiche de synthèse indépendante — non officielle")
    canvas.drawRightString(PAGE_W - MARGIN, y0 - 4.2 * mm, page_indicator)

    st = pstyle("footer_src", fontSize=6.4, leading=8.2, textColor=GREY)
    p = Paragraph(source_text, st)
    w = PAGE_W - 2 * MARGIN
    _, h = p.wrap(w, 20 * mm)
    p.drawOn(canvas, MARGIN, y0 - 6 * mm - h)
    canvas.restoreState()
