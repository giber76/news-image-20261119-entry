#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news broadsheet (1024x1024, Pillow).

A dense one-page front page: navy masthead, 3 illustrated hero cards,
8 illustrated medium cards, a by-the-numbers strip, a dotted world map
with numbered pins, a numbered list of the rest of the day (50 stories
in all, every one happened or first reported on Thursday 19 November
2026), a timeline strip, and a sources footer. All art is flat
procedural drawing -- no copied photograph. Run: python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

NAVY = (13, 38, 66)
NAVY2 = (19, 55, 92)
GOLD = (201, 162, 39)
PAPER = (250, 247, 238)
INK = (24, 24, 24)
GREY = (90, 90, 90)
RED = (178, 34, 34)
RULE = (180, 175, 165)

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def fit(draw, s, f, max_w, min_size=9):
    """Shrink the font until the string fits max_w, then truncate."""
    size = f.size
    while size > min_size and draw.textlength(s, font=font(f.path, size)) > max_w:
        size -= 1
    ff = font(f.path, size)
    while draw.textlength(s, font=ff) > max_w and len(s) > 4:
        s = s[:-4] + "\u2026"
    return s, ff


def wrap(draw, s, f, max_w):
    """Greedy word wrap, returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, f, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, s, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(f.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def rrect(draw, box, fill=None, outline=None, width=1, radius=6):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- world map
# Hand-built land grid, 72 columns (5 deg lon each, -180..180) x 34 rows
# (~4.1 deg lat each, 84N..-56S). '#' = land. Drawn from geography, not
# copied from any dataset.
LAND = [
    "...................####...........................................",
    "..............############..............###......####..............",
    "..######################.####..........###.....#####..............",
    "..##############################......#####..#####################",
    "..##############################..##..####..#######################",
    "..#########################.....######.####.#######################",
    "...#######################.....######.#############################",
    "....######################....##############################.#####",
    "....#####################....##########################.##########",
    "....####################....########################.############",
    "....###################.....######################..###########..",
    ".....##################.....#####################..##########....",
    ".....#################......##################...########.......",
    ".....#################......################....#######.........",
    ".....################......###############......######..........",
    "......###############.......##############......#####...........",
    ".......##############.......#############.......####............",
    ".......#############........############........####..##........",
    ".......############.........###########.........########........",
    ".......############.........##########..........########........",
    ".......############.........#########..........#######..........",
    ".......###########..........########..........######...........",
    ".......##########...........########.........#####.............",
    ".......#########............#######...#......######............",
    ".......########.............######...#......######.............",
    ".......########.............######..........######.............",
    ".......#######..............#####...........######.............",
    ".......######...............####............#####.##...........",
    ".......######...............###.............####..##...........",
    ".......#####...............................###..##............",
    ".......####.................................#................",
    ".......###....................................................",
    ".......##.....................................................",
    ".......#......................................................",
]

# (lon, lat, label) pins on the map
PINS = [
    (-80, 26, "1"),   # Vice City / Miami
    (-77, 39, "2"),   # Washington
    (50, 26, "3"),    # Gulf / Bahrain
    (-122, 37, "4"),  # Santa Clara / Nvidia
    (-122, 37, "5"),  # San Francisco / Anthropic (offset below)
    (-74, 41, "6"),   # New York / Dow
    (-118, 34, "7"),  # Pasadena / Voyager
    (114, 22, "8"),   # Shenzhen / APEC
    (34, 31, "9"),    # Gaza
    (34, 45, "10"),   # Crimea
    (4, 51, "11"),    # Brussels
    (80, 16, "12"),   # India east coast / Akvan
]

# pin offsets (dx, dy in px) so overlapping pins do not collide
PIN_OFF = {4: (0, 0), 5: (16, -12), 6: (16, -8), 2: (0, 0), 7: (-2, 14)}


def lonlat_to_xy(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (84.0 - lat) / 140.0 * (y1 - y0)
    return x, y


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 230, 240))
    cols, rows = 72, 34
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / rows
    for r, row in enumerate(LAND):
        row = row.ljust(cols, ".")
        for c, ch2 in enumerate(row):
            if ch2 == "#":
                cx = x0 + (c + 0.5) * cw
                cy = y0 + (r + 0.5) * ch
                draw.ellipse([cx - 2.4, cy - 2.4, cx + 2.4, cy + 2.4],
                             fill=(58, 110, 88))
    # graticule
    for gx in range(1, 6):
        xx = x0 + (x1 - x0) * gx / 6
        draw.line([(xx, y0), (xx, y1)], fill=(255, 255, 255), width=1)
    for gy in range(1, 4):
        yy = y0 + (y1 - y0) * gy / 4
        draw.line([(x0, yy), (x1, yy)], fill=(255, 255, 255), width=1)
    # pins
    for lon, lat, label in PINS:
        px, py = lonlat_to_xy(lon, lat, box)
        ox, oy = PIN_OFF.get(int(label), (0, 0))
        px, py = px + ox, py + oy
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                     outline=(255, 255, 255), width=2)
        f = font(SANS_B, 11)
        tw = draw.textlength(label, font=f)
        draw.text((px - tw / 2, py - 7), label, font=f, fill=(255, 255, 255))
    return


# ---------------------------------------------------------------- illustrations
# Each draws a small flat scene inside box (x0, y0, x1, y1).

def _sky(draw, box, top, bottom, steps=12):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        yy0 = y0 + (y1 - y0) * i / steps
        yy1 = y0 + (y1 - y0) * (i + 1) / steps
        draw.rectangle([x0, yy0, x1, yy1], fill=col)


def _sun(draw, box, cx, cy, r, col=(255, 214, 90)):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def _buildings(draw, box, base, heights, col, win=(255, 220, 120)):
    x0, y0, x1, y1 = box
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx0 = x0 + i * bw + 1
        bx1 = x0 + (i + 1) * bw - 1
        by0 = base - h
        draw.rectangle([bx0, by0, bx1, base], fill=col)
        for wy in range(int(by0) + 5, int(base) - 4, 9):
            for wx in range(int(bx0) + 3, int(bx1) - 3, 8):
                if (wx + wy) % 17 < 8:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=win)


def _palm(draw, x, y, s, col=(20, 90, 60)):
    draw.line([(x, y), (x + 2 * s, y - 14 * s)], fill=col, width=max(2, int(2 * s)))
    for dx, dy in [(-9, -2), (-7, -6), (9, -3), (7, -7), (-4, -9), (4, -9)]:
        draw.line([(x + 2 * s, y - 14 * s),
                   (x + 2 * s + dx * s, y - 14 * s + dy * s)], fill=col,
                  width=max(1, int(1.5 * s)))


def ill_gta(draw, box):
    _sky(draw, box, (255, 120, 130), (255, 190, 90))
    x0, y0, x1, y1 = box
    _sun(draw, box, (x1 + x0) / 2, y0 + 26, 20)
    _buildings(draw, (x0, y0 + 30, x1, y1 - 12),
               y1 - 12, [46, 70, 38, 84, 55, 64, 40], (40, 30, 70))
    _palm(draw, x0 + 16, y1 - 12, 1.0)
    _palm(draw, x1 - 30, y1 - 12, 0.9)
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(20, 20, 40))


def ill_capitol(draw, box):
    _sky(draw, box, (170, 205, 230), (225, 235, 245))
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    # dome
    draw.rectangle([cx - 34, y1 - 52, cx + 34, y1 - 14], fill=(235, 235, 225))
    draw.pieslice([cx - 30, y0 + 8, cx + 30, y0 + 62], 180, 360, fill=(235, 235, 225))
    draw.rectangle([cx - 3, y0 + 2, cx + 3, y0 + 12], fill=(180, 40, 40))
    draw.rectangle([cx - 46, y1 - 14, cx + 46, y1 - 8], fill=(200, 200, 190))
    for i in range(-2, 3):
        draw.rectangle([cx + i * 14 - 3, y1 - 50, cx + i * 14 + 3, y1 - 14],
                       fill=(210, 210, 200))
    draw.rectangle([x0, y1 - 8, x1, y1], fill=(60, 120, 70))
    # flag
    draw.line([(x1 - 22, y0 + 6), (x1 - 22, y0 + 34)], fill=(80, 80, 80), width=2)
    draw.rectangle([x1 - 22, y0 + 6, x1 - 6, y0 + 18], fill=(178, 34, 34))
    draw.rectangle([x1 - 22, y0 + 10, x1 - 6, y0 + 12], fill=(255, 255, 255))
    draw.rectangle([x1 - 22, y0 + 14, x1 - 6, y0 + 16], fill=(255, 255, 255))


def ill_gulf(draw, box):
    _sky(draw, box, (250, 200, 120), (240, 120, 60))
    x0, y0, x1, y1 = box
    _sun(draw, box, x0 + 30, y0 + 22, 15, (255, 240, 180))
    draw.rectangle([x0, y0 + 62, x1, y1], fill=(25, 80, 130))
    for i in range(4):
        yy = y0 + 72 + i * 10
        draw.line([(x0 + 4, yy), (x1 - 4, yy)], fill=(120, 180, 220), width=2)
    # ship
    draw.polygon([(x0 + 60, y0 + 58), (x0 + 150, y0 + 58), (x0 + 140, y0 + 74),
                  (x0 + 70, y0 + 74)], fill=(60, 60, 70))
    draw.rectangle([x0 + 92, y0 + 40, x0 + 118, y0 + 58], fill=(90, 90, 100))
    draw.line([(x0 + 105, y0 + 40), (x0 + 105, y0 + 28)], fill=(60, 60, 70), width=3)
    # missile arcs
    for sx, sy, ex, ey in [(x1 - 70, y0 + 46, x1 - 34, y0 + 14),
                           (x1 - 100, y0 + 56, x1 - 62, y0 + 26)]:
        draw.arc([sx - 34, sy - 30, ex + 8, ey + 30], 305, 55, fill=(255, 60, 40), width=3)
        draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 200, 60))
    # radar rings, in the sea at lower left
    for r in (8, 15, 22):
        draw.ellipse([x0 + 30 - r, y0 + 84 - r, x0 + 30 + r, y0 + 84 + r],
                     outline=(255, 255, 255), width=1)


def ill_chip(draw, box):
    _sky(draw, box, (15, 40, 25), (25, 90, 50))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    cx, cy = (x0 + x1) / 2 - 18, (y0 + y1) / 2
    # chip
    draw.rectangle([cx - 26 * s, cy - 26 * s, cx + 26 * s, cy + 26 * s],
                   fill=(20, 160, 90), outline=(120, 255, 180), width=2)
    draw.rectangle([cx - 12 * s, cy - 12 * s, cx + 12 * s, cy + 12 * s],
                   fill=(15, 90, 55))
    for i in range(-2, 3):
        draw.line([(cx + i * 10 * s, cy - 26 * s), (cx + i * 10 * s, cy - 34 * s)],
                  fill=(120, 255, 180), width=2)
        draw.line([(cx + i * 10 * s, cy + 26 * s), (cx + i * 10 * s, cy + 34 * s)],
                  fill=(120, 255, 180), width=2)
        draw.line([(cx - 26 * s, cy + i * 10 * s), (cx - 34 * s, cy + i * 10 * s)],
                  fill=(120, 255, 180), width=2)
        draw.line([(cx + 26 * s, cy + i * 10 * s), (cx + 34 * s, cy + i * 10 * s)],
                  fill=(120, 255, 180), width=2)
    # rising chart
    pts = [(x1 - 78, y1 - 22 * s), (x1 - 58, y1 - 34 * s), (x1 - 42, y1 - 28 * s),
           (x1 - 26, y1 - 44 * s), (x1 - 10, y1 - 38 * s)]
    draw.line(pts, fill=(255, 220, 90), width=3, joint="curve")
    draw.ellipse([x1 - 13, y1 - 41 * s, x1 - 7, y1 - 35 * s], fill=(255, 220, 90))


def ill_ipo(draw, box):
    _sky(draw, box, (235, 245, 255), (200, 220, 245))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # bell
    draw.pieslice([x0 + 30, y0 + 14 * s, x0 + 110, y0 + 86 * s], 180, 360,
                  fill=(255, 200, 40))
    draw.rectangle([x0 + 28, y0 + 48 * s, x0 + 112, y0 + 56 * s], fill=(230, 170, 20))
    draw.ellipse([x0 + 62, y0 + 56 * s, x0 + 78, y0 + 68 * s], fill=(230, 170, 20))
    # up arrow
    draw.line([(x1 - 62, y1 - 18 * s), (x1 - 34, y1 - 52 * s), (x1 - 14, y1 - 62 * s)],
              fill=(20, 140, 70), width=4, joint="curve")
    draw.polygon([(x1 - 26, y1 - 66 * s), (x1 - 8, y1 - 66 * s), (x1 - 14, y1 - 48 * s)],
                 fill=(20, 140, 70))
    f = font(SANS_B, max(11, int(16 * s)))
    draw.text((x1 - 66, y0 + 8 * s), "$83", font=f, fill=(20, 140, 70))


def ill_market(draw, box):
    _sky(draw, box, (250, 235, 235), (240, 200, 200))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # candlesticks falling
    xs = [x0 + 14 + i * 22 for i in range(6)]
    tops = [y0 + 16 * s, y0 + 22 * s, y0 + 30 * s, y0 + 26 * s, y0 + 40 * s, y0 + 48 * s]
    bots = [y0 + 34 * s, y0 + 40 * s, y0 + 52 * s, y0 + 48 * s, y0 + 62 * s, y0 + 72 * s]
    for x, t, b in zip(xs, tops, bots):
        draw.line([(x, t - 8 * s), (x, b + 8 * s)], fill=(178, 34, 34), width=2)
        draw.rectangle([x - 6, t, x + 6, b], fill=(178, 34, 34))
    draw.line([(x0 + 8, y1 - 18 * s), (x1 - 8, y1 - 18 * s)], fill=(120, 120, 120), width=2)


def ill_voyager(draw, box):
    _sky(draw, box, (8, 10, 35), (20, 30, 80))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    for fx, fy, r in [(0.08, 0.16, 2), (0.25, 0.30, 1), (0.45, 0.12, 2),
                      (0.62, 0.40, 1), (0.16, 0.55, 1), (0.54, 0.60, 2),
                      (0.37, 0.08, 1)]:
        sx, sy = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    # probe: dish + body + boom
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 3 * s
    draw.line([(cx, cy), (cx + 17 * s, cy - 13 * s)], fill=(200, 200, 210), width=2)
    draw.ellipse([cx + 13 * s, cy - 17 * s, cx + 22 * s, cy - 8 * s],
                 outline=(230, 230, 240), width=2)
    draw.rectangle([cx - 11 * s, cy - 4 * s, cx + 3 * s, cy + 4 * s], fill=(220, 220, 230))
    draw.rectangle([cx - 15 * s, cy - 2 * s, cx - 11 * s, cy + 2 * s], fill=(255, 200, 60))
    draw.line([(cx - 11 * s, cy), (cx - 22 * s, cy + 9 * s)], fill=(200, 200, 210), width=2)


def ill_summit(draw, box):
    _sky(draw, box, (225, 235, 245), (200, 215, 235))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # three flags on poles
    flags = [((178, 34, 34), "US"), ((200, 30, 30), "CN"), ((30, 60, 160), "RU")]
    for i, (col, code) in enumerate(flags):
        px = x0 + 22 + i * 52
        draw.line([(px, y0 + 10 * s), (px, y0 + 66 * s)], fill=(90, 90, 90), width=3)
        draw.rectangle([px, y0 + 10 * s, px + 40, y0 + 34 * s], fill=col)
        draw.rectangle([px, y0 + 18 * s, px + 40, y0 + 22 * s], fill=(255, 255, 255))
        f = font(SANS_B, max(8, int(10 * s)))
        draw.text((px + 6, y0 + 24 * s), code, font=f, fill=(255, 255, 255))
    # table
    draw.rectangle([x0 + 16, y1 - 26 * s, x1 - 16, y1 - 14 * s], fill=(120, 80, 40))
    draw.rectangle([x0 + 26, y1 - 14 * s, x0 + 32, y1 - 4 * s], fill=(90, 60, 30))
    draw.rectangle([x1 - 32, y1 - 14 * s, x1 - 26, y1 - 4 * s], fill=(90, 60, 30))
    for i in range(3):
        draw.ellipse([x0 + 30 + i * 52, y1 - 40 * s, x0 + 44 + i * 52, y1 - 26 * s],
                     fill=(60, 60, 70))


def ill_gaza(draw, box):
    _sky(draw, box, (240, 220, 180), (220, 180, 130))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    # blocks
    _buildings(draw, (x0, y0 + 20 * s, x1, y1 - 10 * s), y1 - 10 * s,
               [30 * s, 48 * s, 26 * s, 40 * s, 34 * s], (150, 130, 100),
               win=(90, 80, 70))
    # smoke columns
    for sx in (x0 + 40, x0 + 110):
        for i, r in enumerate((6 * s, 9 * s, 12 * s)):
            draw.ellipse([sx - r, y0 + 12 * s + i * 12 * s - r,
                          sx + r, y0 + 12 * s + i * 12 * s + r],
                         fill=(120, 110, 100))
    # tents
    for tx in (x0 + 30, x0 + 90, x0 + 150):
        draw.polygon([(tx, y1 - 26 * s), (tx + 18, y1 - 26 * s), (tx + 9, y1 - 40 * s)],
                     fill=(240, 240, 230), outline=(150, 150, 140))


def ill_bridge(draw, box):
    _sky(draw, box, (200, 220, 240), (170, 200, 225))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    my = y0 + 58 * s
    # deck, broken in the middle
    draw.rectangle([x0 + 6, my - 4 * s, x0 + 78, my + 4 * s], fill=(90, 90, 100))
    draw.rectangle([x0 + 108, my - 4 * s, x1 - 6, my + 4 * s], fill=(90, 90, 100))
    draw.polygon([(x0 + 78, my - 4 * s), (x0 + 92, my + 14 * s), (x0 + 108, my - 4 * s)],
                 fill=(90, 90, 100))
    # towers + cables
    for tx in (x0 + 34, x1 - 40):
        draw.rectangle([tx - 3, y0 + 14 * s, tx + 3, my], fill=(70, 70, 80))
        draw.line([(tx, y0 + 14 * s), (x0 + 6, my)], fill=(120, 120, 130), width=1)
        draw.line([(tx, y0 + 14 * s), (x1 - 6, my)], fill=(120, 120, 130), width=1)
    # blast star
    cx, cy = (x0 + x1) / 2, my - 22 * s
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        draw.line([(cx, cy), (cx + dx * 16 * s, cy + dy * 16 * s)], fill=(255, 140, 20), width=3)
    draw.ellipse([cx - 7 * s, cy - 7 * s, cx + 7 * s, cy + 7 * s],
                 fill=(255, 200, 60))
    # water
    draw.rectangle([x0, y1 - 16 * s, x1, y1], fill=(40, 110, 160))
    for i in range(3):
        draw.line([(x0 + 10 + i * 40, y1 - 9 * s), (x0 + 34 + i * 40, y1 - 9 * s)],
                  fill=(140, 200, 240), width=2)


def ill_eu(draw, box):
    _sky(draw, box, (20, 40, 110), (40, 80, 170))
    x0, y0, x1, y1 = box
    s = (y1 - y0) / 100.0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    import math
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        sx, sy = cx + 44 * s * math.cos(ang), cy + 44 * s * math.sin(ang)
        draw.regular_polygon((sx, sy, max(2, int(4 * s))), 5, fill=(255, 220, 60))
    f = font(SERIF_B, max(14, int(34 * s)))
    draw.text((cx - 13 * s, cy - 20 * s), "\u20ac", font=f, fill=(255, 255, 255))
    f2 = font(SANS_B, max(8, int(11 * s)))
    draw.text((cx - 26 * s, y1 - 16 * s), "45 BN", font=f2, fill=(255, 220, 60))


# ---------------------------------------------------------------- stories
# (kicker, headline, deck, illustration)
HEROES = [
    ("CULTURE · GAMING", "Vice City opens: GTA VI begins its global rollout",
     "After 13 years, Rockstar's game unlocks at midnight, NZ first \u2014 "
     "~16m copies pre-sold, $1.5bn+.",
     ill_gta),
    ("USA · POLITICS", "Democrats nominate Jeffries for Speaker",
     "Hakeem Jeffries becomes the first African-American nominated to lead "
     "the House; the full chamber votes next.",
     ill_capitol),
    ("MIDDLE EAST · GULF", "Iran widens its fire across the Gulf",
     "Tehran's attacks reach Kuwait and Bahrain after the US struck a "
     "missile site on Qeshm Island; the region braces.",
     ill_gulf),
]

MEDIUM = [
    ("TECH · CHIPS", "Nvidia's $115.8bn quarter, shares slide",
     "Record revenue, $130bn guide; shares -2.9%.", ill_chip),
    ("MARKETS · IPO", "Anthropic's $81.3bn debut",
     "Shares at $83 in the biggest IPO ever.", ill_ipo),
    ("MARKETS · WALL ST", "Dow drops 561 as the Fed turns hawkish",
     "UnitedHealth -10%; 50bp hike floated.", ill_market),
    ("SPACE", "Voyager 1, one light-day out",
     "NASA confirms the milestone today.", ill_voyager),
    ("DIPLOMACY · APEC", "Trump says Xi and Putin to meet at APEC",
     "Trilateral talks reported in Shenzhen.", ill_summit),
    ("MIDDLE EAST · GAZA", "Israeli troops push into central Gaza",
     "Families flee a rare ground operation.", ill_gaza),
    ("EUROPE · WAR", "Crimea bridge hit again",
     "Traffic suspended after a new attack.", ill_bridge),
    ("EUROPE · UKRAINE", "EU proposes a \u20ac45bn loan for Kyiv",
     "Lend now; repaid once Russia pays up.", ill_eu),
]

ALSO = [
    "Cyclone Akvan bears down on India's east coast",
    "Australia sanctions Israeli settlement expansion",
    "Albanese photographed with Putin; Kyiv backing vowed",
    "Trump praises 'friend' Albanese at Quad summit",
    "Canada rethinks China ties; Carney seeks US deal",
    "Spain's general strike: police clash with protesters",
    "France: minister says M\u00e9lenchon could win presidency",
    "Saudi Arabia: danger passed in three southern cities",
    "Libya seizes cocaine and millions of pills in east",
    "Somalia accuses UAE of building secret bases",
    "US panel urges punishing China over ship detentions",
    "NSA classified network suffered outage, reports say",
    "Deutsche Bank handled $582m in Epstein deals \u2014 FT",
    "Russian agent arrested 'targeting Silicon Valley firm'",
    "Bukele hails action on gang leader's Haiti home",
    "Pew: Islam on track to be largest faith by 2035",
    "Earth 'missing a billion years' \u2014 clue found",
    "Modi meets Prince and Princess of Wales",
    "Alibaba earnings test Chinese consumer spending",
    "Walmart reports earnings today",
    "Oil slides: WTI -3.5% to $83; Brent $93",
    "Bitcoin -2.1% to $62,630 on ETF outflows",
    "Microsoft in talks to sell AI services to ByteDance",
    "Tencent misses revenue; Asia chips diverge",
    "ASX falls for a fifth straight day; BHP drags",
    "Taiwan's Liu Yunping elected House caucus chair",
    "China's micro-EVs crowd city streets",
    "Merck launches mRNA rabies vaccine for pets",
    "US senators warn AI cyber threats outpacing defences",
    "US service outages spark stockpiling of essentials",
    "One Nation unveils latest migration pitch",
    "Notts County 2-0 Grimsby, unbeaten run ends",
    "Chhattisgarh beat Odisha by 51 runs",
    "Chitwan Rhinos beat Kathmandu by 61 runs",
    "NFL tonight: Colts at Texans, Week 11 opener",
    "NBA tonight: Warriors at Grizzlies; Knicks at Wolves",
    "Nikkei +0.28% to 59,024; Nifty -0.63%",
    "US midterms a 'verdict' on Iran war, says Chalmers",
    "GTA VI festival to light up Miami on Saturday",
]

NUMBERS = [
    ("16M", "GTA VI pre-sales"),
    ("$115.8BN", "Nvidia quarter"),
    ("561", "Dow points lost"),
    ("$81.3BN", "Anthropic IPO"),
    ("1 LIGHT-DAY", "Voyager 1"),
]

TIMELINE = [
    ("MIDNIGHT NZ", "GTA VI unlocks"),
    ("MORNING ASIA", "Markets slide"),
    ("MIDDAY EUROPE", "EU's \u20ac45bn loan"),
    ("AFTERNOON US", "Jeffries nominated"),
    ("EVENING US", "Anthropic IPO"),
    ("TONIGHT", "Colts at Texans"),
]

PIN_KEY = [
    "1 Miami \u00b7 GTA VI", "2 Washington \u00b7 Speaker", "3 Gulf \u00b7 Iran fire",
    "4 Santa Clara \u00b7 Nvidia", "5 San Francisco \u00b7 Anthropic",
    "6 New York \u00b7 Dow", "7 Pasadena \u00b7 Voyager 1", "8 Shenzhen \u00b7 APEC",
    "9 Gaza \u00b7 Ground op", "10 Crimea \u00b7 Bridge", "11 Brussels \u00b7 \u20ac45bn",
    "12 East India \u00b7 Akvan",
]


# ---------------------------------------------------------------- layout
def card(draw, box, kicker, headline, deck, ill, hero=False):
    x0, y0, x1, y1 = box
    rrect(draw, box, fill=(255, 255, 255), outline=RULE, width=1, radius=6)
    draw.rectangle([x0, y0, x1, y0 + 2], fill=RED)
    pad = 10
    if hero:
        ih = 104
        ill(draw, (x0 + 1, y0 + 3, x1 - 1, y0 + 3 + ih))
        ty = y0 + 3 + ih + 6
        kf = font(SANS_B, 11)
        hf = font(SERIF_B, 19)
        df = font(SANS, 12)
        draw.text((x0 + pad, ty), kicker, font=kf, fill=RED)
        ty += 15
        ty = draw_wrapped(draw, x0 + pad, ty, headline, hf, x1 - x0 - 2 * pad,
                          INK, leading=21, max_lines=2)
        draw_wrapped(draw, x0 + pad, ty + 2, deck, df, x1 - x0 - 2 * pad,
                     (60, 60, 60), leading=15, max_lines=2)
    else:
        ih = 50
        ill(draw, (x0 + 1, y0 + 3, x1 - 1, y0 + 3 + ih))
        ty = y0 + 3 + ih + 4
        kf = font(SANS_B, 9)
        hf = font(SERIF_B, 14)
        df = font(SANS, 10)
        draw.text((x0 + pad, ty), kicker, font=kf, fill=RED)
        ty += 12
        ty = draw_wrapped(draw, x0 + pad, ty, headline, hf, x1 - x0 - 2 * pad,
                          INK, leading=16, max_lines=2)
        draw_wrapped(draw, x0 + pad, ty + 1, deck, df, x1 - x0 - 2 * pad,
                     (60, 60, 60), leading=12, max_lines=1)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([0, 92, W, 95], fill=GOLD)
    f = font(SANS_B, 13)
    t = "THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(t, font=f)) / 2, 8), t, font=f, fill=GOLD)
    f = font(SERIF_B, 40)
    t = "THURSDAY 19 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, 26), t, font=f, fill=(255, 255, 255))
    f = font(SANS, 13)
    t = "50 STORIES  \u00b7  6 CONTINENTS  \u00b7  ALL REPORTED ON THURSDAY"
    d.text(((W - d.textlength(t, font=f)) / 2, 70), t, font=f, fill=(200, 210, 225))

    # ---- heroes
    hw, gap = 328, 10
    for i, (k, h, deck, ill) in enumerate(HEROES):
        x0 = 10 + i * (hw + gap)
        card(d, (x0, 103, x0 + hw, 299), k, h, deck, ill, hero=True)

    # ---- medium cards, two rows of four
    mw = 244
    for row in range(2):
        for col in range(4):
            idx = row * 4 + col
            k, h, deck, ill = MEDIUM[idx]
            x0 = 10 + col * (mw + gap)
            y0 = 307 + row * 124
            card(d, (x0, y0, x0 + mw, y0 + 116), k, h, deck, ill)

    # ---- by the numbers
    y0 = 563
    d.rectangle([10, y0, 1014, y0 + 30], fill=NAVY2)
    f = font(SANS_B, 12)
    d.text((16, y0 + 8), "BY THE NUMBERS", font=f, fill=GOLD)
    x = 170
    for val, lab in NUMBERS:
        fv = font(SANS_B, 14)
        fl = font(SANS, 11)
        d.text((x, y0 + 7), val, font=fv, fill=(255, 255, 255))
        x += d.textlength(val, font=fv) + 6
        d.text((x, y0 + 9), lab, font=fl, fill=(190, 200, 215))
        x += d.textlength(lab, font=fl) + 26

    # ---- bottom: map (left) + also today (right)
    y0 = 601
    # map panel
    d.rectangle([10, y0, 430, 968], fill=(255, 255, 255), outline=RULE, width=1)
    f = font(SANS_B, 13)
    d.text((22, y0 + 8), "WHERE IT HAPPENED", font=f, fill=NAVY)
    d.line([(22, y0 + 28), (418, y0 + 28)], fill=RULE, width=1)
    draw_map(d, (22, y0 + 36, 418, y0 + 236))
    # pin key, two columns
    f = font(SANS, 11)
    for i, item in enumerate(PIN_KEY):
        kx = 22 + (i % 2) * 200
        ky = y0 + 246 + (i // 2) * 17
        num = item.split(" ", 1)[0]
        d.ellipse([kx, ky + 1, kx + 11, ky + 12], fill=RED)
        fn = font(SANS_B, 8)
        tw = d.textlength(num, font=fn)
        d.text((kx + (11 - tw) / 2, ky + 1), num, font=fn, fill=(255, 255, 255))
        d.text((kx + 16, ky), item, font=f, fill=INK)

    # also-today panel
    d.rectangle([440, y0, 1014, 968], fill=(255, 255, 255), outline=RULE, width=1)
    d.text((452, y0 + 8), "ALSO ON THURSDAY 19 NOVEMBER", font=f, fill=NAVY)
    d.line([(452, y0 + 28), (1002, y0 + 28)], fill=RULE, width=1)
    f = font(SANS, 11)
    col_w = 272
    for i, item in enumerate(ALSO):
        col = 0 if i < 20 else 1
        row = i if i < 20 else i - 20
        x = 452 + col * (col_w + 12)
        yy = y0 + 36 + row * 14
        num = str(12 + i) + "."
        fn = font(SANS_B, 11)
        d.text((x, yy), num, font=fn, fill=RED)
        s, ff = fit(d, item, f, col_w - 26)
        d.text((x + 26, yy), s, font=ff, fill=INK)
    # timeline strip
    ty = y0 + 36 + 20 * 14 + 8
    d.line([(452, ty), (1002, ty)], fill=RULE, width=1)
    d.text((452, ty + 6), "THE DAY, IN ORDER", font=font(SANS_B, 11), fill=NAVY)
    tx = 452
    for lab, ev in TIMELINE:
        fl = font(SANS_B, 9)
        fe = font(SANS, 10)
        d.text((tx, ty + 22), lab, font=fl, fill=RED)
        d.text((tx, ty + 34), ev, font=fe, fill=INK)
        tx += max(d.textlength(lab, font=fl), d.textlength(ev, font=fe)) + 18
        if tx < 1002:
            d.line([(tx - 9, ty + 22), (tx - 9, ty + 46)], fill=RULE, width=1)

    # ---- footer
    d.rectangle([0, 976, W, H], fill=NAVY)
    f = font(SANS, 11)
    t1 = ("Every story here happened or was first reported on Thursday 19 November 2026. "
          "Contested claims are labelled as claims.")
    d.text((10, 982), t1, font=f, fill=(200, 210, 225))
    t2 = ("Sources: AP, Reuters, AFP, BBC, Al Jazeera, CNBC, NDTV, The Hindu, FT, "
          "NASA, Fed, Rockstar Games.")
    d.text((10, 1000), t2, font=f, fill=(160, 175, 195))
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
