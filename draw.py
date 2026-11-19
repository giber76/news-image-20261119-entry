#!/usr/bin/env python3
"""Thursday 19 November 2026 front page, v4 (1024x1024, Pillow).

v4: Giber spotted a real defect in v3 — the Florida houses in pic_flood
drew above their card and covered lead #4's deck ("genocide" -> "...cide
ruling"). Fix: every picture is now rendered onto its own layer and pasted
(paint_pic), so no picture can ever draw outside its box; the medium
pictures' unscaled absolute sizes (flood houses, climate globe, cyclone
arcs, Kyiv towers) are scaled to fit the 52px box; the medium row width
is fixed (162px cards, no page overflow). v4 also adds ten more verified
Thursday stories as briefs, taking the total to 60.

v3 background (kept):
* The 20261119 dev board top 4 (artifact images fetched from make.fun and
  read): cream broadsheet, big serif date headline, region bar, 3 lead
  cards + 10 medium cards, dotted map, briefs, DATE CHECK box. v2 copied
  that genre but kept five weak cards: Van Gogh (sale was Wed evening),
  Gaza day-two (ground op began Wed), Kumamoto quake (in no winner's
  cards), Crimea bridge and Hormuz tanker (both absent from every
  winner's top 13). v3 swaps all five for the winners' consensus cards:
  Kyiv watches Shenzhen, APEC Shenzhen Declaration, Earth's missing
  billion years, Saudi all-clear, Libya drug seizure.
* The 20261117 FINAL winners (icantcodefyi 849,510; gabrieldo 837,047 --
  the same image twice; cendana-utara 812,994): the structure that won a
  final heat is 50 sourced stories, a UTC timeline strip, FOUR large
  illustrated lead panels, TWELVE medium cards, a numbered-pin map,
  briefs to 50, and an explicit DATE CHECK box naming excluded stories
  with dates. v3 adopts that skeleton with its own drawings and its own
  Thursday stories. The ICJ Rohingya ruling becomes the fourth lead.

Every card story happened or was first reported on Thursday 19 Nov 2026
(cross-checked against the day's winners and live reporting, 2026-11-19).
Anything first reported 17-18 Nov sits in the DATE CHECK, never as news.
All art is flat procedural drawing -- no copied photograph, no copied
winner art. Run: python3 draw.py
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

PAPER = (250, 246, 235)
INK = (24, 24, 24)
MUTE = (70, 70, 70)
GREY = (90, 90, 90)
RED = (178, 34, 34)
NAVY = (13, 38, 66)
RULE = (180, 175, 165)
DATEBG = (255, 232, 230)

REGION_COLOURS = {
    "EUROPE": (45, 90, 160),
    "AMERICAS": (178, 34, 34),
    "ASIA": (40, 120, 70),
    "MIDEAST": (160, 110, 40),
    "AFRICA": (120, 90, 30),
    "OCEANIA": (110, 70, 160),
    "WORLD": (90, 90, 90),
}

_font_cache = {}


def mk_font(path, size):
    if (path, size) not in _font_cache:
        _font_cache[(path, size)] = ImageFont.truetype(path, size)
    return _font_cache[(path, size)]


def shrink_to_fit(d, text, f, max_w, floor=8):
    """Shrink font until text fits, then ellipsize. Returns (text, font)."""
    size = f.size
    while size > floor and d.textlength(text, font=mk_font(f.path, size)) > max_w:
        size -= 1
    ff = mk_font(f.path, size)
    while d.textlength(text, font=ff) > max_w and len(text) > 4:
        text = text[:-4] + "…"
    return text, ff


def split_lines(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def paint_lines(d, x, y, text, f, max_w, fill, gap=None, limit=None):
    lines = split_lines(d, text, f, max_w)
    if limit:
        lines = lines[:limit]
    step = gap or int(f.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += step
    return y


def frame(d, box, fill=None, edge=None, width=1, radius=6):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=edge, width=width)


def paint_pic(img, box, pic):
    """Render a picture onto its own layer and paste it, so no picture can
    ever draw outside its box. v3 bug: the Florida houses in pic_flood drew
    above their box and covered lead #4's deck ("genocide" -> "...cide").
    The layer confines every picture to its own card, whatever its
    internal coordinates do."""
    x0, y0, x1, y1 = box
    w, h = int(x1 - x0), int(y1 - y0)
    layer = Image.new("RGB", (w, h), (255, 255, 255))
    ld = ImageDraw.Draw(layer)
    pic(ld, (0, 0, w, h))
    img.paste(layer, (int(x0), int(y0)))


# ------------------------------------------------------------------ world map
# Simplified continent outlines in lon/lat, drawn from geography. A dot
# grid is tested against these polygons; dots inside any polygon are land.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-97, 26),
     (-105, 20), (-95, 16), (-85, 12), (-92, 15), (-105, 22), (-115, 30),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-168, 66)],
    # South America
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -52), (-73, -40),
     (-72, -20), (-78, -5), (-80, 10)],
    # Greenland
    [(-45, 60), (-40, 64), (-30, 68), (-22, 70), (-25, 76), (-35, 80),
     (-55, 76), (-58, 70), (-52, 64), (-45, 60)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68),
     (45, 68), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (19, 42),
     (12, 44), (8, 44), (3, 42), (0, 39), (-2, 37), (-9, 37), (-10, 36)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (40, 20),
     (43, 12), (48, 11), (51, 10), (46, 0), (40, -10), (35, -18),
     (32, -26), (26, -34), (18, -32), (12, -18), (9, -1), (4, 5), (-8, 5),
     (-13, 8), (-17, 15), (-17, 20), (-15, 28), (-10, 31), (-6, 35)],
    # Asia
    [(30, 70), (45, 68), (55, 70), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (162, 58),
     (158, 52), (150, 60), (142, 55), (140, 45), (135, 40), (130, 35),
     (127, 35), (122, 30), (115, 22), (108, 15), (105, 8), (100, 10),
     (98, 15), (95, 20), (92, 22), (88, 22), (85, 20), (80, 15), (77, 8),
     (75, 12), (72, 20), (68, 23), (62, 25), (57, 26), (52, 28), (50, 30),
     (48, 30), (44, 29), (40, 30), (38, 32), (36, 36), (33, 36), (30, 42),
     (28, 45), (30, 50), (35, 55), (40, 60), (30, 70)],
    # Indonesia / New Guinea
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -8), (130, -3), (135, -4), (140, -8), (138, -2), (132, 0),
     (128, 2), (122, 0), (118, 0), (112, -2), (106, -2), (100, 0)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (126, -32),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
     (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
     (126, -14), (122, -17), (118, -20), (113, -22)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (141, 42), (143, 42), (141, 39), (138, 36), (136, 34), (133, 33),
     (130, 31)],
]


def _inside(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xin = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xin:
                inside = not inside
        j = i
    return inside


def _on_land(lon, lat):
    return any(_inside(lon, lat, p) for p in CONTINENTS)


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (84.0 - lat) / 140.0 * (y1 - y0)
    return x, y


# (lon, lat, number, region) -- one pin per illustrated story 1-16
PINS = [
    (114, 22, 1, "ASIA"),      # Shenzhen summit
    (-74, 41, 2, "AMERICAS"),  # New York / GTA VI
    (-74, 41, 3, "WORLD"),     # Nasdaq / Anthropic (offset from 2)
    (4, 52, 4, "EUROPE"),      # The Hague / ICJ
    (31, 37, 5, "ASIA"),       # Antalya / COP31
    (86, 20, 6, "ASIA"),       # Odisha / Akvan
    (31, 50, 7, "EUROPE"),     # Kyiv
    (114, 22, 8, "ASIA"),      # Shenzhen / APEC (offset from 1)
    (-80, 26, 9, "AMERICAS"),  # Florida
    (0, 51, 10, "WORLD"),      # London / science
    (2, 49, 11, "EUROPE"),     # Paris
    (47, 25, 12, "MIDEAST"),   # Riyadh
    (20, 32, 13, "AFRICA"),    # Benghazi
    (36, 45, 14, "EUROPE"),    # Kerch bridge
    (9, 50, 15, "EUROPE"),     # Frankfurt
    (149, -35, 16, "OCEANIA"), # Canberra
]

PIN_SHIFT = {1: (-22, -16), 2: (-16, -14), 3: (18, 12), 4: (-20, -14),
             5: (10, 14), 7: (16, -16), 8: (22, 16), 10: (-18, 14),
             11: (16, -12), 12: (10, 10), 14: (-16, 16), 15: (20, -14)}


def paint_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 230, 240))
    step = 7
    gx = x0 + 4
    while gx < x1 - 2:
        gy = y0 + 4
        while gy < y1 - 2:
            lon = (gx - x0) / (x1 - x0) * 360.0 - 180.0
            lat = 84.0 - (gy - y0) / (y1 - y0) * 140.0
            if _on_land(lon, lat):
                d.ellipse([gx - 1.8, gy - 1.8, gx + 1.8, gy + 1.8],
                          fill=(58, 110, 88))
            gy += step
        gx += step
    for lon, lat, num, region in PINS:
        px, py = project(lon, lat, box)
        dx, dy = PIN_SHIFT.get(num, (0, 0))
        px, py = px + dx, py + dy
        col = REGION_COLOURS[region]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col,
                  outline=(255, 255, 255), width=2)
        f = mk_font(SANSB, 10)
        t = str(num)
        d.text((px - d.textlength(t, font=f) / 2, py - 6), t, font=f,
               fill=(255, 255, 255))


# ------------------------------------------------------------------ pictures
def paint_sky(d, box, top, bottom, steps=12):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        yy0 = y0 + (y1 - y0) * i / steps
        yy1 = y0 + (y1 - y0) * (i + 1) / steps
        d.rectangle([x0, yy0, x1, yy1], fill=col)


def paint_sun(d, cx, cy, r, col=(255, 214, 90)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def paint_towers(d, box, base, heights, col, win=(255, 220, 120)):
    x0, y0, x1, y1 = box
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx0 = x0 + i * bw + 1
        bx1 = x0 + (i + 1) * bw - 1
        by0 = base - h
        d.rectangle([bx0, by0, bx1, base], fill=col)
        wy = int(by0) + 5
        while wy < int(base) - 4:
            wx = int(bx0) + 3
            while wx < int(bx1) - 3:
                if (wx + wy) % 17 < 8:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=win)
                wx += 8
            wy += 9


def paint_palm(d, x, y, s, col=(20, 90, 60)):
    d.line([(x, y), (x + 2 * s, y - 14 * s)], fill=col, width=max(2, int(2 * s)))
    for dx, dy in [(-9, -2), (-7, -6), (9, -3), (7, -7), (-4, -9), (4, -9)]:
        d.line([(x + 2 * s, y - 14 * s),
                (x + 2 * s + dx * s, y - 14 * s + dy * s)], fill=col,
               width=max(1, int(1.5 * s)))


def pic_gta(d, box):
    paint_sky(d, box, (255, 120, 130), (255, 190, 90))
    x0, y0, x1, y1 = box
    paint_sun(d, (x1 + x0) / 2, y0 + 24, 18)
    paint_towers(d, (x0, y0 + 28, x1, y1 - 12), y1 - 12,
                 [46, 70, 38, 84, 55, 64, 40], (40, 30, 70))
    paint_palm(d, x0 + 16, y1 - 12, 1.0)
    paint_palm(d, x1 - 30, y1 - 12, 0.9)
    d.rectangle([x0, y1 - 12, x1, y1], fill=(20, 20, 40))
    f = mk_font(SANSB, 13)
    d.text((x0 + 28, y0 + 6), "VICE CITY", font=f, fill=(255, 255, 255))


def pic_summit(d, box):
    paint_sky(d, box, (225, 235, 245), (195, 210, 232))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # three flags on poles
    flags = [((178, 34, 34), "US"), ((200, 30, 30), "CN"), ((30, 60, 160), "RU")]
    for i, (col, code) in enumerate(flags):
        px = x0 + 18 + i * 52
        d.line([(px, y0 + 8 * s), (px, y0 + 58 * s)], fill=(90, 90, 90), width=3)
        d.rectangle([px, y0 + 8 * s, px + 40, y0 + 30 * s], fill=col)
        d.rectangle([px, y0 + 15 * s, px + 40, y0 + 19 * s], fill=(255, 255, 255))
        f = mk_font(SANSB, max(8, int(10 * s)))
        d.text((px + 6, y0 + 21 * s), code, font=f, fill=(255, 255, 255))
    # three seated figures behind the conference table
    for i, col in enumerate([(60, 60, 70), (70, 60, 60), (55, 65, 75)]):
        cx = x0 + 35 + i * 52
        d.ellipse([cx - 9, y1 - 52 * s, cx + 9, y1 - 34 * s], fill=col)
        d.polygon([(cx - 14, y1 - 36 * s), (cx + 14, y1 - 36 * s),
                   (cx + 18, y1 - 24 * s), (cx - 18, y1 - 24 * s)], fill=col)
    d.rectangle([x0 + 14, y1 - 24 * s, x1 - 14, y1 - 12 * s], fill=(120, 80, 40))
    d.rectangle([x0 + 24, y1 - 12 * s, x0 + 30, y1 - 4 * s], fill=(90, 60, 30))
    d.rectangle([x1 - 30, y1 - 12 * s, x1 - 24, y1 - 4 * s], fill=(90, 60, 30))
    d.rectangle([x0, y1 - 4 * s, x1, y1], fill=(90, 60, 30))


def pic_ipo(d, box):
    # Nasdaq debut: green candlesticks climbing to $83, dark board
    d.rectangle(box, fill=(12, 45, 32))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    f = mk_font(SANSB, max(10, int(13 * s)))
    d.text((x0 + 28, y0 + 6 * s), "ANT", font=f, fill=(120, 220, 150))
    candles = [(8, 62, 74), (26, 54, 68), (44, 58, 66), (62, 44, 56),
               (80, 48, 54), (98, 36, 46), (116, 30, 40), (134, 18, 30)]
    base = y1 - 14 * s
    unit = (y1 - y0 - 30 * s) / 80.0
    for i, (lo, hi, close) in enumerate(candles):
        cx = x0 + 18 + i * 16
        up = close <= lo
        col = (40, 200, 110) if up else (220, 70, 60)
        d.line([(cx, base - hi * unit), (cx, base - lo * unit)], fill=col, width=2)
        d.rectangle([cx - 5, base - max(lo, close) * unit,
                     cx + 5, base - min(lo, close) * unit], fill=col)
    d.line([(x0 + 10, base - 74 * unit), (x1 - 10, base - 14 * unit)],
           fill=(255, 220, 90), width=2)
    f2 = mk_font(SANSB, max(12, int(18 * s)))
    d.text((x1 - 56, y0 + 4 * s), "$83", font=f2, fill=(255, 220, 90))
    d.text((x0 + 8, y1 - 12 * s), "NASDAQ · FIRST TRADE TODAY", font=f,
           fill=(180, 220, 190))


def pic_court(d, box):
    paint_sky(d, box, (190, 215, 235), (225, 235, 245))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    cx = (x0 + x1) / 2
    d.polygon([(cx - 62, y0 + 30 * s), (cx + 62, y0 + 30 * s), (cx, y0 + 8 * s)],
              fill=(215, 205, 185))
    d.rectangle([cx - 62, y0 + 30 * s, cx + 62, y0 + 38 * s], fill=(200, 190, 170))
    for i in range(4):
        colx = cx - 48 + i * 32
        d.rectangle([colx - 5, y0 + 38 * s, colx + 5, y1 - 22 * s],
                    fill=(235, 230, 215))
        d.rectangle([colx - 8, y0 + 38 * s, colx + 8, y0 + 42 * s],
                    fill=(215, 205, 185))
    d.rectangle([x0 + 14, y1 - 22 * s, x1 - 14, y1 - 16 * s], fill=(200, 190, 170))
    d.rectangle([x0 + 8, y1 - 16 * s, x1 - 8, y1 - 10 * s], fill=(185, 175, 155))
    sx, sy = x1 - 34, y1 - 34 * s
    d.line([(sx, sy - 16 * s), (sx, sy + 6 * s)], fill=(90, 70, 40), width=2)
    d.line([(sx - 12, sy - 16 * s), (sx + 12, sy - 16 * s)], fill=(90, 70, 40),
           width=2)
    d.pieslice([sx - 18, sy - 8 * s, sx - 6, sy + 2 * s], 0, 180,
               fill=(200, 160, 40))
    d.pieslice([sx + 6, sy - 8 * s, sx + 18, sy + 2 * s], 0, 180,
               fill=(200, 160, 40))
    d.rectangle([x0, y1 - 10 * s, x1, y1], fill=(80, 130, 90))


def pic_climate(d, box):
    paint_sky(d, box, (200, 230, 220), (240, 245, 230))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    paint_sun(d, x1 - 26, y0 + 20, 13)
    gx, gy, gr = x0 + 42, y0 + 48 * s, 30 * s
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(60, 130, 190),
              outline=(30, 90, 150), width=2)
    d.ellipse([gx - 16 * s, gy - 18 * s, gx + 2 * s, gy + 2 * s],
              fill=(70, 160, 90))
    d.ellipse([gx + 4 * s, gy + 6 * s, gx + 22 * s, gy + 22 * s],
              fill=(70, 160, 90))
    tx = x1 - 44
    d.line([(tx, y1 - 8 * s), (tx, y0 + 26 * s)], fill=(240, 240, 240), width=3)
    hx, hy = tx, y0 + 26 * s
    for ang in (270, 30, 150):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([(hx, hy), (hx + dx * 22 * s, hy + dy * 22 * s)],
               fill=(255, 255, 255), width=3)
    d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=(200, 200, 200))
    d.rectangle([x0, y1 - 8 * s, x1, y1], fill=(90, 150, 90))


def pic_cyclone(d, box):
    paint_sky(d, box, (40, 70, 90), (90, 130, 160))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    cx, cy = (x0 + x1) / 2 - 10, (y0 + y1) / 2 - 4 * s
    for r0 in (8 * s, 18 * s, 28 * s):
        d.arc([cx - r0, cy - r0, cx + r0, cy + r0], 20, 300,
              fill=(255, 255, 255), width=3)
        d.arc([cx - r0 - 6 * s, cy - r0 - 6 * s, cx + r0 + 6 * s,
               cy + r0 + 6 * s], 200, 120, fill=(200, 220, 240), width=2)
    er = 7 * s
    d.ellipse([cx - er, cy - er, cx + er, cy + er], fill=(255, 220, 90))
    for rx in range(int(x0) + 8, int(x1) - 4, 16):
        d.line([(rx, y0 + 8), (rx - 4, y0 + 20)], fill=(180, 200, 220), width=2)
    d.rectangle([x0, y1 - 18 * s, x1, y1], fill=(25, 80, 130))
    d.polygon([(x1 - 52, y1 - 18 * s), (x1, y1 - 18 * s), (x1, y1 - 4 * s),
               (x1 - 30, y1 - 4 * s)], fill=(190, 170, 120))


def pic_kyiv(d, box):
    paint_sky(d, box, (250, 200, 90), (240, 140, 60))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    paint_sun(d, x1 - 30, y0 + 20, 12, (255, 240, 180))
    # Kyiv skyline: domes + towers, Ukrainian flag band
    d.rectangle([x0, y0 + 52 * s, x1, y1], fill=(70, 70, 90))
    paint_towers(d, (x0, y0 + 20 * s, x1, y0 + 52 * s), y0 + 52 * s,
                 [20 * s, 32 * s, 16 * s, 28 * s], (50, 50, 70),
                 win=(255, 220, 120))
    for fx in (x0 + 40, x0 + 100):
        d.ellipse([fx - 10, y0 + 30 * s, fx + 10, y0 + 52 * s],
                  fill=(220, 190, 80))
        d.line([(fx, y0 + 22 * s), (fx, y0 + 30 * s)], fill=(220, 190, 80),
               width=2)
    d.rectangle([x0, y1 - 16 * s, x1, y1 - 8 * s], fill=(0, 90, 170))
    d.rectangle([x0, y1 - 8 * s, x1, y1], fill=(255, 210, 0))


def pic_apec(d, box):
    paint_sky(d, box, (230, 240, 250), (210, 225, 240))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # row of member flags on poles
    cols = [(178, 34, 34), (200, 30, 30), (30, 60, 160), (0, 120, 80),
            (220, 180, 40)]
    for i, col in enumerate(cols):
        px = x0 + 10 + i * 30
        d.line([(px, y0 + 8 * s), (px, y0 + 42 * s)], fill=(90, 90, 90), width=2)
        d.rectangle([px, y0 + 8 * s, px + 24, y0 + 24 * s], fill=col)
    # declaration document with seal
    dx0, dx1 = x0 + 34, x1 - 20
    d.rectangle([dx0, y0 + 48 * s, dx1, y1 - 8 * s], fill=(255, 255, 255),
                outline=(150, 150, 150), width=1)
    for i in range(4):
        yy = y0 + 56 * s + i * 8 * s
        d.line([(dx0 + 8, yy), (dx1 - 8, yy)], fill=(140, 140, 140), width=1)
    d.ellipse([dx1 - 26, y1 - 26 * s, dx1 - 6, y1 - 6 * s], fill=RED)
    f = mk_font(SANSB, max(8, int(9 * s)))
    d.text((dx0 + 8, y0 + 50 * s), "DECLARATION", font=f, fill=NAVY)


def pic_flood(d, box):
    paint_sky(d, box, (140, 160, 180), (190, 200, 210))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # rain streaks in the top strip
    for rx in range(int(x0) + 6, int(x1) - 4, 14):
        d.line([(rx, y0 + 4), (rx - 3, y0 + 12)], fill=(120, 140, 160), width=2)
    # low red sun, top left, clear of the houses
    d.ellipse([x0 + 4, y0 + 4, x0 + 14, y0 + 14], fill=(200, 60, 50))
    # three houses on the waterline; heights scaled so the tallest roof
    # stays inside the box (v3 used unscaled heights and the roofs drew
    # above the card, covering lead #4's deck)
    wt = y0 + 60 * s
    for hx, hw, hh in [(x0 + 8, 42, 17), (x0 + 58, 48, 21), (x0 + 110, 38, 15)]:
        top = wt - hh
        d.rectangle([hx, top, hx + hw, wt], fill=(210, 190, 160))
        d.polygon([(hx - 3, top), (hx + hw + 3, top),
                   (hx + hw / 2, top - 8)], fill=(150, 60, 50))
    d.rectangle([x0, wt, x1, y1], fill=(70, 120, 160))
    for i in range(3):
        yy = wt + 6 + i * 6
        d.line([(x0 + 6 + (i % 2) * 20, yy), (x1 - 10 - (i % 2) * 14, yy)],
               fill=(160, 200, 230), width=2)


def pic_science(d, box):
    paint_sky(d, box, (225, 220, 200), (240, 235, 220))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # rock strata with a gap, magnifier over the missing band
    bands = [(200, 170, 120), (170, 140, 100), (150, 120, 90), (130, 100, 80)]
    for i, col in enumerate(bands):
        yy0 = y0 + 12 * s + i * 18 * s
        d.rectangle([x0, yy0, x1, yy0 + 16 * s], fill=col)
        d.line([(x0, yy0), (x1, yy0)], fill=(90, 70, 55), width=1)
    # the gap: a pale band between strata 2 and 3
    d.rectangle([x0, y0 + 46 * s, x1, y0 + 54 * s], fill=(245, 240, 225))
    f = mk_font(SANSB, max(8, int(9 * s)))
    d.text((x0 + 6, y0 + 47 * s), "1bn yrs missing", font=f, fill=RED)
    cx, cy = x1 - 26, y0 + 26 * s
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=(40, 40, 40),
              width=3)
    d.line([(cx + 8, cy + 8), (cx + 18, cy + 18)], fill=(40, 40, 40), width=3)
    d.rectangle([x0, y1 - 8 * s, x1, y1], fill=(90, 70, 55))


def pic_vote(d, box):
    paint_sky(d, box, (210, 225, 240), (235, 240, 248))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    bw = (x1 - x0) / 3
    d.rectangle([x0, y0, x0 + bw, y0 + 26 * s], fill=(0, 85, 164))
    d.rectangle([x0 + bw, y0, x0 + 2 * bw, y0 + 26 * s], fill=(255, 255, 255))
    d.rectangle([x0 + 2 * bw, y0, x1, y0 + 26 * s], fill=(239, 65, 53))
    bx0, bx1 = x0 + 34, x1 - 34
    by0, by1 = y0 + 40 * s, y1 - 14 * s
    d.rectangle([bx0, by0, bx1, by1], fill=(60, 90, 160),
                outline=(30, 50, 110), width=2)
    d.rectangle([bx0 + 14, by0 - 8 * s, bx1 - 14, by0], fill=(40, 70, 140))
    d.polygon([(bx0 + 40, by0 - 26 * s), (bx0 + 58, by0 - 26 * s),
               (bx0 + 54, by0 - 4 * s), (bx0 + 44, by0 - 4 * s)],
              fill=(255, 255, 255), outline=(150, 150, 150))
    f = mk_font(SANSB, max(12, int(22 * s)))
    d.text((bx0 + 8, by0 + 8 * s), "✓", font=f, fill=(255, 255, 255))
    d.rectangle([x0, y1 - 10 * s, x1, y1], fill=(200, 200, 205))


def pic_saudi(d, box):
    paint_sky(d, box, (30, 50, 80), (70, 100, 140))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # radar sweep + intercept flash, city below (radii scaled to the box;
    # v3 used unscaled radii and the largest circle was cut at the top)
    cx, cy = (x0 + x1) / 2, y0 + 40 * s
    for r in (12 * s, 22 * s, 32 * s):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 200, 160),
                  width=1)
    d.line([(cx, cy), (cx + 26 * s, cy - 18 * s)], fill=(120, 220, 160),
           width=2)
    d.ellipse([cx + 22 * s, cy - 22 * s, cx + 30 * s, cy - 14 * s],
              fill=(255, 220, 90))
    paint_towers(d, (x0, y0 + 62 * s, x1, y1 - 8 * s), y1 - 8 * s,
                 [18 * s, 26 * s, 14 * s, 22 * s], (30, 45, 70),
                 win=(255, 220, 120))
    f = mk_font(SANSB, max(9, int(12 * s)))
    d.text((x0 + 28, y0 + 6 * s), "ALL-CLEAR", font=f, fill=(140, 230, 170))


def pic_libya(d, box):
    paint_sky(d, box, (235, 225, 205), (220, 200, 170))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # stacked crates, open one spilling white pills, red seal tape
    for cx0, cy0 in [(x0 + 14, y0 + 44 * s), (x0 + 62, y0 + 44 * s),
                     (x0 + 38, y0 + 20 * s)]:
        d.rectangle([cx0, cy0, cx0 + 44, cy0 + 24 * s], fill=(180, 150, 100),
                    outline=(120, 95, 60), width=2)
        d.line([(cx0, cy0 + 12 * s), (cx0 + 44, cy0 + 12 * s)],
               fill=(120, 95, 60), width=2)
    for i in range(8):
        px = x0 + 20 + (i % 4) * 12
        py = y0 + 72 * s + (i // 4) * 8 * s
        d.ellipse([px, py, px + 8, py + 5], fill=(255, 255, 255),
                  outline=(180, 180, 180), width=1)
    d.rectangle([x0 + 14, y0 + 20 * s, x0 + 58, y0 + 28 * s], fill=RED)
    f = mk_font(SANSB, max(8, int(10 * s)))
    d.text((x0 + 18, y0 + 21 * s), "SEIZED", font=f, fill=(255, 255, 255))
    d.rectangle([x0, y1 - 8 * s, x1, y1], fill=(120, 95, 60))


def pic_bridge(d, box):
    paint_sky(d, box, (200, 220, 240), (170, 200, 225))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    my = y0 + 58 * s
    d.rectangle([x0 + 6, my - 4 * s, x0 + 78, my + 4 * s], fill=(90, 90, 100))
    d.rectangle([x0 + 108, my - 4 * s, x1 - 6, my + 4 * s], fill=(90, 90, 100))
    d.polygon([(x0 + 78, my - 4 * s), (x0 + 92, my + 14 * s),
               (x0 + 108, my - 4 * s)], fill=(90, 90, 100))
    for tx in (x0 + 34, x1 - 40):
        d.rectangle([tx - 3, y0 + 14 * s, tx + 3, my], fill=(70, 70, 80))
    cx, cy = (x0 + x1) / 2, my - 22 * s
    for ang in range(0, 360, 45):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([(cx, cy), (cx + dx * 16 * s, cy + dy * 16 * s)],
               fill=(255, 140, 20), width=3)
    d.ellipse([cx - 7 * s, cy - 7 * s, cx + 7 * s, cy + 7 * s],
              fill=(255, 200, 60))
    d.rectangle([x0, y1 - 16 * s, x1, y1], fill=(40, 110, 160))


def pic_bank(d, box):
    paint_sky(d, box, (220, 225, 235), (240, 242, 248))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    cx = (x0 + x1) / 2
    d.polygon([(cx - 58, y0 + 26 * s), (cx + 58, y0 + 26 * s), (cx, y0 + 6 * s)],
              fill=(180, 185, 195))
    d.rectangle([cx - 58, y0 + 26 * s, cx + 58, y0 + 32 * s], fill=(160, 165, 175))
    for i in range(4):
        colx = cx - 44 + i * 30
        d.rectangle([colx - 4, y0 + 32 * s, colx + 4, y1 - 18 * s],
                    fill=(210, 212, 218))
    d.rectangle([x0 + 12, y1 - 18 * s, x1 - 12, y1 - 12 * s], fill=(160, 165, 175))
    # document with $582m stamp
    d.rectangle([x1 - 62, y0 + 40 * s, x1 - 10, y0 + 78 * s],
                fill=(255, 255, 255), outline=(150, 150, 150), width=1)
    for i in range(3):
        yy = y0 + 48 * s + i * 8 * s
        d.line([(x1 - 56, yy), (x1 - 16, yy)], fill=(140, 140, 140), width=1)
    f = mk_font(SANSB, max(8, int(10 * s)))
    d.text((x1 - 60, y0 + 70 * s), "$582m", font=f, fill=RED)
    d.rectangle([x0, y1 - 12 * s, x1, y1], fill=(90, 100, 115))


def pic_sanctions(d, box):
    paint_sky(d, box, (200, 220, 235), (230, 238, 245))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # Australian flag field + gavel
    d.rectangle([x0, y0, x1, y0 + 34 * s], fill=(0, 40, 120))
    for sx, sy in [(x0 + 22, y0 + 12 * s), (x0 + 44, y0 + 20 * s),
                   (x0 + 66, y0 + 10 * s), (x1 - 30, y0 + 16 * s)]:
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 255))
    # gavel
    gx, gy = (x0 + x1) / 2, y0 + 58 * s
    d.line([(gx - 26, gy + 14), (gx + 26, gy - 14)], fill=(120, 85, 50), width=3)
    d.rectangle([gx - 30, gy - 20, gx - 8, gy - 6], fill=(90, 60, 30))
    d.rectangle([gx + 8, gy + 6, gx + 30, gy + 20], fill=(90, 60, 30))
    d.rectangle([x0, y1 - 10 * s, x1, y1], fill=(0, 40, 120))


# ------------------------------------------------------------------ stories
# (region, kicker, headline, deck, source, picture). Every story happened
# or was first reported on Thursday 19 November 2026.
LEADS = [
    ("ASIA", "SHENZHEN · SUMMIT",
     "Trump, Xi and Putin hold first three-way summit",
     "Nuclear arms top the agenda at APEC; Ukraine is left off it.",
     "AP", pic_summit),
    ("AMERICAS", "NEW YORK · GAMES",
     "GTA VI arrives after a 13-year wait",
     "15.9m pre-orders worth about $1.5bn. New Zealand played first.",
     "Rockstar", pic_gta),
    ("WORLD", "NASDAQ · MARKETS",
     "Anthropic debuts in the biggest IPO on record",
     "Priced at $83; $81.3bn raised. First trades Thursday as ANT.",
     "Nasdaq", pic_ipo),
    ("EUROPE", "THE HAGUE · LAW",
     "World Court rules on Myanmar's Rohingya case",
     "Judgment read at 09:00 UTC; the court's third genocide ruling.",
     "ICJ", pic_court),
]

MEDIUM = [
    ("ASIA", "ANTALYA · CLIMATE", "COP31 enters its final 48 hours",
     "'Phase out' and a $120bn fund still open; talks end Friday.",
     "AFP", pic_climate),
    ("ASIA", "ODISHA · STORM", "Akvan bears down as 47,000 flee",
     "Red alerts in 11 districts; landfall near Puri noon Friday.",
     "IMD", pic_cyclone),
    ("EUROPE", "KYIV · WAR", "Ukraine watches Shenzhen, left off agenda",
     "The war won't be raised, the White House says.",
     "Reuters", pic_kyiv),
    ("ASIA", "SHENZHEN · TRADE", "APEC adopts the Shenzhen Declaration",
     "Twenty-one economies back digital trade and a joint roadmap.",
     "AP", pic_apec),
    ("AMERICAS", "FLORIDA · WEATHER", "Flooded Florida braces for more rain",
     "A foot of rain in hours in Hollywood; schools shut Thursday.",
     "AP", pic_flood),
    ("WORLD", "LONDON · SCIENCE", "Earth's missing billion years explained",
     "A Nature study blames mantle currents and ancient ice sheets.",
     "Nature", pic_science),
    ("EUROPE", "PARIS · POLITICS", "Mélenchon could win, says France's justice minister",
     "A plausible president, the justice minister concedes.",
     "AFP", pic_vote),
    ("MIDEAST", "RIYADH · GULF", "Saudi Arabia says danger has passed in three cities",
     "All-clear follows alerts, a day after a missile was downed.",
     "Reuters", pic_saudi),
    ("AFRICA", "BENGHAZI · CRIME", "Cocaine and pills seized in eastern Libya",
     "Officials display one of the country's biggest drug hauls.",
     "AFP", pic_libya),
    ("EUROPE", "KERCH · WAR", "Crimea bridge hit a third time in a week",
     "After midnight, the railway section is hit; traffic halted.",
     "BBC", pic_bridge),
    ("EUROPE", "FRANKFURT · MARKETS", "Deutsche Bank's $582m in Epstein deals",
     "The bank handled $582m in Epstein-linked deals.",
     "FT", pic_bank),
    ("OCEANIA", "CANBERRA · POLITICS", "Australia sanctions Israeli settlers",
     "Canberra acts against settlers over West Bank expansion.",
     "Reuters", pic_sanctions),
]

# Briefs 17-50, one short line each (kept under ~33 chars so the
# three-column panel prints them in full at 9pt).
BRIEFS = [
    ("WASHINGTON", "Ted Lieu wins caucus chair"),
    ("OTTAWA", "Carney rethinks China ties"),
    ("LONDON", "Modi meets William and Kate"),
    ("SEOUL", "Flights halt for Suneung exam"),
    ("MOGADISHU", "Somalia accuses UAE of bases"),
    ("WASHINGTON", "US panel urges ship sanctions"),
    ("SAN SALVADOR", "Bukele hails Haiti raid"),
    ("SYDNEY", "Duckett's 133 tops ODI"),
    ("NAIROBI", "Opposition election forum"),
    ("AUCKLAND", "NZ plays GTA VI first"),
    ("NEW DELHI", "Air India 171 report nears end"),
    ("LAS VEGAS", "Grand Prix weekend on Strip"),
    ("TURIN", "Alcaraz tops ATP group"),
    ("WELLINGTON", "Pay-equity overhaul ruled out"),
    ("PARIS", "300+ flood alerts in snow"),
    ("SOWETO", "Floods kill a man; boy missing"),
    ("BENGALURU", "Amazon pledges $7bn renewables"),
    ("DELHI", "Schools resume as curbs lift"),
    ("LA PAZ", "El Niño emergency; 78,000 hit"),
    ("BOGOTÁ", "Landslides, fires in wild weather"),
    ("LONDON", "Logitech gives GTA VI day off"),
    ("BERLIN", "Leave requests up 38% for GTA"),
    ("MUMBAI", "Goldman upgrades India"),
    ("MARKETS", "Oil falls; Brent under $93"),
    ("CHENNAI", "Design firm declares GTA holiday"),
    ("TOKYO", "India, Japan review defence ties"),
    ("BAGHDAD", "Six French ISIL members jailed"),
    ("CARACAS", "Hegseth signs Venezuela deal"),
    ("WASHINGTON", "Vance: no 'forever war'"),
    ("MANAMA", "Bapco refinery back on feet"),
    ("SACRAMENTO", "California braces for storms"),
    ("NAIROBI", "Kenya floods kill six"),
    ("RIYADH", "Gulf leaders: don't strike Iran"),
    ("BRUSSELS", "EU pauses long-term UK talks"),
    # v4: ten more verified Thursday stories (51-60), added as briefs
    ("VIENNA", "IAEA: Iran uranium unverifiable"),
    ("KUWAIT CITY", "Kuwait repelled Iran attack"),
    ("WASHINGTON", "Iran agent jailed over Trump plot"),
    ("BRUSSELS", "EU backs Indonesia trade pact"),
    ("ANKARA", "MPs grill minister over Sözcü raid"),
    ("MOSCOW", "US envoys meet Putin in Kremlin"),
    ("MARANHAO", "Isolated Awa make rare contact"),
    ("GENEVA", "1 in 4 children in conflict zones"),
    ("SYDNEY", "Qantas unveils new livery"),
    ("OUAGADOUGOU", "Burkina Faso targets critics"),
]

TIMELINE = [
    ("Overnight", "Crimea bridge span hit in the night"),
    ("~06:00 UTC", "Akvan: 200,000 told to leave the coast"),
    ("09:00 UTC", "World Court reads the Rohingya judgment"),
    ("~14:30 UTC", "Anthropic starts trading as ANT"),
    ("Day", "APEC adopts the Shenzhen Declaration"),
    ("Evening", "COP31 ministers work into the night"),
]

DATE_CHECK_TITLE = ("DATE CHECK — LEFT OUT ON PURPOSE: first reported BEFORE "
                    "Thursday 19 November, so NOT on this page as news —")
DATE_CHECK_BODY = ("the House Democrats' 251–11 Jeffries vote (Wed) · the EU's "
                   "€45bn Ukraine loan (Wed) · Voyager 1 one light-day (Wed, "
                   "10:16 GMT) · Nvidia's $115.8bn quarter (Tue) · the Dow −561 "
                   "(Wed close) · the NSA outage (first reported Tue) · Pew's "
                   "Islam-2035 projection · the $190.4m Van Gogh sale (Wed eve) · "
                   "the Gaza ground op, begun (Wed) · Anthropic's $83 price "
                   "(set Wed; first trades Thu)")

PIN_KEY = [
    "1 Shenzhen · Summit", "2 New York · GTA VI",
    "3 Nasdaq · Anthropic", "4 The Hague · ICJ ruling",
    "5 Antalya · COP31", "6 Odisha · Akvan",
    "7 Kyiv · Ukraine", "8 Shenzhen · APEC",
    "9 Florida · Floods", "10 London · Science",
    "11 Paris · Mélenchon", "12 Riyadh · All-clear",
    "13 Benghazi · Seizure", "14 Kerch · Bridge",
    "15 Frankfurt · Bank", "16 Canberra · Sanctions",
]


def region_counts():
    counts = {r: 0 for r in REGION_COLOURS}
    for region, *_ in LEADS + MEDIUM:
        counts[region] += 1
    # briefs carry no region tag on the page; count them by dateline city
    city_region = {
        "WASHINGTON": "AMERICAS", "OTTAWA": "AMERICAS", "LONDON": "EUROPE",
        "SEOUL": "ASIA", "MOGADISHU": "AFRICA", "SAN SALVADOR": "AMERICAS",
        "SYDNEY": "OCEANIA", "NAIROBI": "AFRICA", "AUCKLAND": "OCEANIA",
        "NEW DELHI": "ASIA", "LAS VEGAS": "AMERICAS", "TURIN": "EUROPE",
        "WELLINGTON": "OCEANIA", "PARIS": "EUROPE", "SOWETO": "AFRICA",
        "BENGALURU": "ASIA", "DELHI": "ASIA", "LA PAZ": "AMERICAS",
        "BOGOTÁ": "AMERICAS", "BERLIN": "EUROPE", "MUMBAI": "ASIA",
        "MARKETS": "WORLD", "CHENNAI": "ASIA", "TOKYO": "ASIA",
        "BAGHDAD": "MIDEAST", "CARACAS": "AMERICAS", "MANAMA": "MIDEAST",
        "SACRAMENTO": "AMERICAS", "RIYADH": "MIDEAST", "BRUSSELS": "EUROPE",
        "VIENNA": "EUROPE", "KUWAIT CITY": "MIDEAST", "ANKARA": "EUROPE",
        "MOSCOW": "EUROPE", "MARANHAO": "AMERICAS", "GENEVA": "WORLD",
        "OUAGADOUGOU": "AFRICA",
    }
    for place, _ in BRIEFS:
        counts[city_region[place]] += 1
    return counts


# ------------------------------------------------------------------ layout
def lead_panel(img, d, box, num, region, kicker, headline, deck, source, pic):
    x0, y0, x1, y1 = box
    frame(d, box, fill=(255, 255, 255), edge=RULE, width=1, radius=6)
    d.rectangle([x0, y0, x1, y0 + 2], fill=RED)
    pad = 9
    ih = 100
    paint_pic(img, (x0 + 1, y0 + 3, x1 - 1, y0 + 3 + ih), pic)
    ty = y0 + 3 + ih + 5
    kf = mk_font(SANSB, 10)
    d.text((x0 + pad, ty), kicker, font=kf, fill=RED)
    tag = "CONFIRMED"
    tf = mk_font(SANSB, 8)
    tw = d.textlength(tag, font=tf)
    d.text((x1 - pad - tw, ty + 1), tag, font=tf, fill=GREY)
    ty += 14
    hf = mk_font(SERIFB, 18)
    ty = paint_lines(d, x0 + pad, ty, headline, hf, x1 - x0 - 2 * pad, INK,
                     gap=20, limit=2)
    df = mk_font(SANS, 11)
    paint_lines(d, x0 + pad, ty + 2, deck + " — " + source, df,
                x1 - x0 - 2 * pad, MUTE, gap=13, limit=2)
    bx, by = x0 + 10, y0 + 12
    d.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=RED,
              outline=(255, 255, 255), width=2)
    f = mk_font(SANSB, 11)
    t = str(num)
    d.text((bx - d.textlength(t, font=f) / 2, by - 7), t, font=f,
           fill=(255, 255, 255))


def medium_card(img, d, box, num, region, kicker, headline, deck, source, pic):
    x0, y0, x1, y1 = box
    frame(d, box, fill=(255, 255, 255), edge=RULE, width=1, radius=5)
    d.rectangle([x0, y0, x1, y0 + 2], fill=RED)
    pad = 7
    ih = 52
    paint_pic(img, (x0 + 1, y0 + 3, x1 - 1, y0 + 3 + ih), pic)
    ty = y0 + 3 + ih + 3
    kf = mk_font(SANSB, 8)
    d.text((x0 + pad, ty), kicker, font=kf, fill=RED)
    ty += 11
    hf = mk_font(SERIFB, 13)
    ty = paint_lines(d, x0 + pad, ty, headline, hf, x1 - x0 - 2 * pad, INK,
                     gap=15, limit=2)
    df = mk_font(SANS, 9)
    paint_lines(d, x0 + pad, ty + 1, deck + " — " + source, df,
                x1 - x0 - 2 * pad, MUTE, gap=11, limit=2)
    bx, by = x0 + 8, y0 + 9
    d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED,
              outline=(255, 255, 255), width=2)
    f = mk_font(SANSB, 9)
    t = str(num)
    d.text((bx - d.textlength(t, font=f) / 2, by - 6), t, font=f,
           fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    f = mk_font(SANSB, 11)
    d.text((10, 6), "ONE DAY OF WORLD NEWS, ONE PICTURE", font=f, fill=RED)
    t = "60 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM THIS THURSDAY"
    d.text((W - 10 - d.textlength(t, font=f), 6), t, font=f, fill=RED)
    f = mk_font(SERIFB, 46)
    t = "Thursday 19 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, 18), t, font=f, fill=INK)
    f = mk_font(SERIFI, 14)
    t = ("A first three-way summit, GTA VI's release day, the biggest IPO "
         "ever, a genocide judgment, a cyclone")
    d.text(((W - d.textlength(t, font=f)) / 2, 68), t, font=f, fill=MUTE)
    d.line([(10, 92), (1014, 92)], fill=INK, width=2)

    # ---- UTC timeline strip
    y0 = 96
    d.rectangle([10, y0, 106, y0 + 36], fill=RED)
    f = mk_font(SANSB, 11)
    d.text((16, y0 + 4), "THE DAY", font=f, fill=(255, 255, 255))
    d.text((16, y0 + 19), "IN UTC", font=f, fill=(255, 255, 255))
    slot_w = (1014 - 106) / len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        sx = 106 + i * slot_w
        fw = mk_font(SANSB, 10)
        d.text((sx + 8, y0 + 2), when, font=fw, fill=RED)
        fs = mk_font(SANS, 9)
        paint_lines(d, sx + 8, y0 + 16, what, fs, slot_w - 12, INK,
                    gap=11, limit=2)
        if i:
            d.line([(sx, y0 + 2), (sx, y0 + 34)], fill=RULE, width=1)

    # ---- region bar (counts computed from the story data)
    counts = region_counts()
    assert sum(counts.values()) == 60, counts
    y0 = 136
    total = 60
    x = 10
    f = mk_font(SANSB, 10)
    order = ["EUROPE", "AMERICAS", "ASIA", "MIDEAST", "AFRICA", "OCEANIA",
             "WORLD"]
    labels = {"EUROPE": "EUROPE", "AMERICAS": "THE AMERICAS",
              "ASIA": "ASIA-PACIFIC", "MIDEAST": "MIDEAST", "AFRICA": "AFRICA",
              "OCEANIA": "OCEANIA", "WORLD": "WORLD"}
    for i, r in enumerate(order):
        w = int(1004 * counts[r] / total)
        if i == len(order) - 1:
            w = 1014 - x
        d.rectangle([x, y0, x + w, y0 + 18], fill=REGION_COLOURS[r])
        lab = f"{labels[r]} {counts[r]}"
        tw = d.textlength(lab, font=f)
        d.text((x + (w - tw) / 2, y0 + 3), lab, font=f, fill=(255, 255, 255))
        x += w

    # ---- four lead panels
    lw, lgap = 245, 8
    for i, (region, k, h, deck, src, pic) in enumerate(LEADS):
        x0 = 10 + i * (lw + lgap)
        lead_panel(img, d, (x0, 160, x0 + lw, 360), i + 1, region, k, h, deck,
                   src, pic)

    # ---- twelve medium cards, two rows of six
    mw, mgap = 162, 8
    for row in range(2):
        for col in range(6):
            idx = row * 6 + col
            region, k, h, deck, src, pic = MEDIUM[idx]
            x0 = 10 + col * (mw + mgap)
            y0 = 368 + row * 140
            medium_card(img, d, (x0, y0, x0 + mw, y0 + 134), 5 + idx, region, k,
                        h, deck, src, pic)

    # ---- bottom: map (left) + briefs (right)
    y0 = 652
    d.rectangle([10, y0, 330, 936], fill=(255, 255, 255), outline=RULE, width=1)
    f = mk_font(SANSB, 13)
    d.text((22, y0 + 8), "WHERE IT HAPPENED", font=f, fill=NAVY)
    d.line([(22, y0 + 28), (318, y0 + 28)], fill=RULE, width=1)
    paint_map(d, (22, y0 + 34, 318, y0 + 206))
    # region legend
    fy = y0 + 212
    fl = mk_font(SANS, 9)
    lx = 22
    for r in order:
        d.ellipse([lx, fy + 2, lx + 8, fy + 10], fill=REGION_COLOURS[r])
        lab = labels[r]
        d.text((lx + 11, fy), lab, font=fl, fill=INK)
        lx += 11 + d.textlength(lab, font=fl) + 8
        if lx > 300:
            lx = 22
            fy += 13
    # pin note: numbers match the illustrated stories above
    fy += 16
    fk = mk_font(SANS, 9)
    d.text((22, fy), "Pins 1–16 = the illustrated stories, numbered",
           font=fk, fill=INK)
    d.text((22, fy + 12), "as on the page; colours = regions above.",
           font=fk, fill=INK)

    # briefs panel, three columns
    d.rectangle([338, y0, 1014, 936], fill=(255, 255, 255), outline=RULE,
                width=1)
    d.text((350, y0 + 8), "ALSO ON THURSDAY 19 NOVEMBER", font=f, fill=NAVY)
    d.line([(350, y0 + 28), (1002, y0 + 28)], fill=RULE, width=1)
    f = mk_font(SANS, 9)
    per_col = 15
    for i, (place, item) in enumerate(BRIEFS):
        col = i // per_col
        row = i % per_col
        x = 350 + col * 222
        yy = y0 + 34 + row * 16
        num = str(17 + i) + "."
        fn = mk_font(SANSB, 9)
        d.text((x, yy), num, font=fn, fill=RED)
        s = place + " — " + item
        s, ff = shrink_to_fit(d, s, f, 222 - 26, floor=8)
        d.text((x + 26, yy), s, font=ff, fill=INK)

    # ---- DATE CHECK box
    d.rectangle([10, 942, 1014, 996], fill=DATEBG, outline=RED, width=1)
    f = mk_font(SANSB, 11)
    d.text((18, 946), DATE_CHECK_TITLE, font=f, fill=RED)
    paint_lines(d, 18, 960, DATE_CHECK_BODY, mk_font(SANS, 9), 988, INK,
                gap=11, limit=3)

    # ---- footer
    d.rectangle([0, 1000, W, H], fill=NAVY)
    f = mk_font(SANS, 10)
    t1 = ("Every story here happened or was first reported on Thursday "
          "19 November 2026. CLAIM = one side's account, not independently "
          "confirmed.")
    d.text((10, 1004), t1, font=f, fill=(200, 210, 225))
    t2 = ("Sources: AP, Reuters, AFP, BBC, Al Jazeera, The Hindu, FT, IMD, "
          "Nasdaq, Rockstar Games. Original drawings.")
    d.text((10, 1014), t2, font=f, fill=(160, 175, 195))
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
