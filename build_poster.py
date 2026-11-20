#!/usr/bin/env python3
"""Build THE WORLD TODAY — news-image-20261120 v2 poster (1024x1024 PNG).

Reads the story data from image-data.ts (strict-JSON literal), renders at
2x supersampling (2048) and downscales to 1024 with LANCZOS. Deterministic:
fixed seed, no timestamps, no network, no random placement without the seed.
"""
import json
import math
import os
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SEED = 20261120
S = 2  # supersampling factor
W, H = 1024 * S, 1024 * S
HERE = Path(__file__).resolve().parent
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

PAPER = (255, 255, 255)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
NAVY2 = (27, 42, 74)
RED = (192, 57, 43)
GRAY = (110, 110, 110)
RULE = (205, 205, 200)
STAT_BG = (247, 242, 230)
MAP_BG = (251, 248, 240)
LAND_DOT = (214, 190, 140)
YELLOW = (242, 201, 76)
NOTYET_BG = (255, 246, 214)
TEAL = (46, 134, 171)
GREEN = (46, 125, 50)


def sc(v):
    """Scale a 1024-space coordinate to supersampled pixels."""
    return int(round(v * S))


def F(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), max(1, int(round(size * S))))


def serif_b(size):
    return F("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return F("DejaVuSerif.ttf", size)


def sans(size):
    return F("DejaVuSans.ttf", size)


def sans_b(size):
    return F("DejaVuSans-Bold.ttf", size)


def load_data():
    text = (HERE / "image-data.ts").read_text(encoding="utf-8")
    anchor = text.index("export const DATA")
    start = text.index("{", anchor)
    end = text.rindex("}") + 1
    return json.loads(text[start:end])


def wrap(text, font, max_w):
    """Greedy word wrap; max_w in supersampled pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(d, cx, y, text, font, fill):
    w = font.getlength(text)
    d.text((cx - w / 2, y), text, font=font, fill=fill)


# ---------------------------------------------------------------- continents
# Coarse lon/lat outlines for the dot-matrix world map.
CONTINENTS = [
    # North America
    [(-168, 66), (-160, 60), (-152, 58), (-142, 60), (-134, 57), (-128, 51),
     (-124, 44), (-121, 35), (-114, 29), (-108, 23), (-100, 18), (-94, 16),
     (-89, 14), (-84, 11), (-80, 9), (-78, 9), (-81, 13), (-85, 16),
     (-88, 21), (-91, 19), (-95, 18), (-97, 16), (-97, 23), (-95, 28),
     (-90, 29), (-85, 30), (-81, 26), (-80, 31), (-76, 35), (-74, 40),
     (-70, 43), (-66, 45), (-60, 47), (-55, 47), (-59, 51), (-64, 56),
     (-68, 58), (-74, 62), (-80, 63), (-86, 66), (-92, 66), (-97, 69),
     (-104, 68), (-112, 68), (-120, 70), (-128, 70), (-136, 70), (-144, 70),
     (-152, 71), (-160, 71), (-166, 68)],
    # South America
    [(-78, 8), (-76, 4), (-80, -3), (-81, -6), (-77, -12), (-73, -18),
     (-70, -22), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-68, -50), (-65, -45), (-62, -40), (-58, -34), (-53, -33),
     (-49, -28), (-42, -23), (-38, -15), (-35, -8), (-38, -4), (-42, -2),
     (-47, 0), (-51, 4), (-54, 6), (-58, 8), (-62, 10), (-68, 11),
     (-72, 12), (-76, 10)],
    # Africa
    [(-17, 15), (-17, 21), (-15, 27), (-11, 31), (-6, 34), (-1, 35),
     (5, 37), (10, 37), (11, 33), (15, 32), (20, 32), (25, 31), (30, 31),
     (33, 28), (35, 24), (38, 20), (40, 15), (43, 11), (48, 11), (51, 10),
     (47, 6), (42, 2), (40, -4), (37, -10), (35, -18), (33, -26),
     (29, -32), (24, -34), (19, -35), (17, -32), (15, -27), (13, -21),
     (12, -17), (13, -11), (11, -4), (9, 0), (9, 4), (-6, 5), (-11, 7),
     (-14, 10), (-17, 13)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49),
     (0, 51), (4, 53), (7, 55), (8, 57), (10, 59), (5, 60), (6, 62),
     (12, 65), (18, 69), (25, 71), (32, 70), (40, 68), (48, 69), (56, 69),
     (64, 70), (72, 72), (80, 73), (88, 75), (96, 76), (104, 77), (112, 75),
     (120, 73), (128, 72), (136, 72), (144, 71), (152, 70), (158, 69),
     (164, 66), (170, 66), (178, 65), (178, 61), (170, 60), (162, 60),
     (158, 54), (155, 51), (150, 59), (143, 58), (142, 53), (140, 48),
     (135, 44), (130, 42), (127, 39), (122, 38), (120, 33), (117, 28),
     (112, 22), (109, 19), (106, 11), (103, 8), (100, 8), (98, 11),
     (95, 16), (92, 21), (89, 22), (86, 20), (82, 16), (79, 10), (77, 9),
     (75, 14), (72, 20), (69, 22), (66, 25), (61, 25), (57, 25), (59, 22),
     (55, 18), (51, 15), (47, 14), (43, 12), (40, 17), (38, 21), (36, 25),
     (35, 29), (34, 31), (35, 33), (36, 36), (33, 36), (30, 36), (27, 37),
     (23, 36), (19, 40), (16, 38), (12, 44), (8, 44), (3, 43), (0, 39),
     (-2, 37), (-6, 36), (-9, 37)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (137, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
    # Greenland
    [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68), (-25, 70),
     (-20, 70), (-22, 74), (-30, 76), (-40, 76), (-50, 74), (-58, 70)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-3, 50)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 37),
     (141, 40), (141, 44), (143, 42), (141, 39), (139, 36), (137, 34),
     (135, 33), (132, 31)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (174, -41),
     (171, -43), (168, -46)],
    # Sumatra
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -6), (101, -3),
     (98, 1), (95, 4)],
    # Borneo
    [(109, 1), (111, 3), (114, 4), (117, 6), (119, 2), (117, -2),
     (114, -3), (110, -3), (109, 0)],
    # New Guinea
    [(131, -1), (135, -2), (138, -4), (141, -5), (145, -7), (147, -9),
     (146, -8), (142, -8), (138, -7), (134, -4), (131, -2)],
]


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < xin:
                inside = not inside
    return inside


def on_land(lon, lat):
    return any(point_in_poly(lon, lat, poly) for poly in CONTINENTS)


# ---------------------------------------------------------------- art
# Each illustration draws inside (x0, y0, x1, y1) in supersampled pixels.

def art_cyclone(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(220, 233, 242))
    cx, cy = (x0 + x1) // 2 - sc(8), (y0 + y1) // 2
    for r, w in ((sc(20), 3), (sc(14), 3), (sc(8), 3)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=TEAL, width=max(2, w * S // 2))
    d.ellipse([cx - sc(3), cy - sc(3), cx + sc(3), cy + sc(3)], fill=(255, 255, 255))
    d.polygon([(x1 - sc(2), y1), (x1 - sc(16), y1), (x1 - sc(2), y1 - sc(10))],
              fill=(120, 170, 120))


def art_missiles(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(247, 227, 222))
    for i, (sx, ex) in enumerate(((0.15, 0.45), (0.35, 0.65), (0.55, 0.85))):
        ax0 = x0 + int((x1 - x0) * sx)
        ax1 = x0 + int((x1 - x0) * ex)
        ay = y1 - sc(10)
        by = y0 + sc(8) + i * sc(4)
        d.arc([ax0, by - sc(14), ax1, ay + sc(6)], start=270, end=360,
              fill=RED, width=max(2, 2 * S))
        d.ellipse([ax1 - sc(2), by - sc(2), ax1 + sc(2), by + sc(2)], fill=RED)
    for i in range(5):
        bx = x0 + sc(6) + i * sc(14)
        bh = sc(6) + (i % 2) * sc(4)
        d.rectangle([bx, y1 - bh, bx + sc(9), y1], fill=(60, 60, 60))


def art_climate(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(221, 238, 221))
    cx, cy = (x0 + x1) // 2 - sc(10), (y0 + y1) // 2
    r = sc(15)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GREEN, width=max(2, 2 * S))
    d.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=GREEN,
              width=max(1, S))
    d.line([cx - r, cy, cx + r, cy], fill=GREEN, width=max(1, S))
    tx = x1 - sc(12)
    d.rounded_rectangle([tx, y0 + sc(6), tx + sc(6), y1 - sc(6)],
                        radius=sc(3), outline=RED, width=max(1, S), fill=(255, 255, 255))
    d.ellipse([tx - sc(2), y1 - sc(12), tx + sc(8), y1 - sc(2)], fill=RED)
    d.rectangle([tx + sc(2), y0 + sc(10), tx + sc(4), y1 - sc(10)], fill=RED)


def art_candles(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(242, 242, 242))
    n = 5
    w = (x1 - x0) // (n + 1)
    tops = [0.25, 0.35, 0.5, 0.62, 0.75]
    for i, t in enumerate(tops):
        cx = x0 + w * (i + 1)
        top = y0 + int((y1 - y0) * t)
        bot = y1 - sc(6)
        d.line([cx, top - sc(5), cx, bot + sc(3)], fill=(60, 60, 60),
               width=max(1, S))
        d.rectangle([cx - sc(4), top, cx + sc(4), bot], fill=RED)
    d.line([x0 + sc(4), y0 + sc(8), x1 - sc(4), y1 - sc(10)], fill=GRAY,
           width=max(1, S))


def art_mercury(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=NAVY2)
    rnd = random.Random(SEED)
    for _ in range(14):
        sx = rnd.randint(x0 + 2, x1 - 2)
        sy = rnd.randint(y0 + 2, y1 - 2)
        d.ellipse([sx, sy, sx + max(1, S), sy + max(1, S)], fill=(255, 255, 255))
    cx, cy = (x0 + x1) // 2 - sc(6), (y0 + y1) // 2
    r = sc(13)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(154, 154, 154))
    for ox, oy, cr in ((-5, -4, 3), (4, 2, 2), (-1, 6, 2), (6, -6, 2)):
        d.ellipse([cx + sc(ox) - sc(cr), cy + sc(oy) - sc(cr),
                   cx + sc(ox) + sc(cr), cy + sc(oy) + sc(cr)], fill=(120, 120, 120))
    px, py = x1 - sc(12), y0 + sc(8)
    d.polygon([(px, py), (px + sc(6), py + sc(3)), (px, py + sc(6))],
              fill=(255, 255, 255))
    d.rectangle([px - sc(6), py + sc(2), px - sc(1), py + sc(4)], fill=(200, 200, 200))


def art_flags(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(234, 240, 248))
    mid = (x0 + x1) // 2
    # EU flag (left half)
    ex0, ey0, ex1, ey1 = x0 + sc(4), y0 + sc(8), mid - sc(3), y1 - sc(8)
    d.rectangle([ex0, ey0, ex1, ey1], fill=(0, 51, 153))
    ccx, ccy = (ex0 + ex1) // 2, (ey0 + ey1) // 2
    rr = (ey1 - ey0) // 3
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        sx = ccx + int(rr * math.cos(a))
        sy = ccy + int(rr * math.sin(a))
        d.ellipse([sx - S, sy - S, sx + S, sy + S], fill=(255, 209, 0))
    # UK flag, simplified (right half)
    ux0, uy0, ux1, uy1 = mid + sc(3), y0 + sc(8), x1 - sc(4), y1 - sc(8)
    d.rectangle([ux0, uy0, ux1, uy1], fill=(0, 36, 125))
    d.polygon([(ux0, uy0), (ux1, uy1), (ux1, uy1 - sc(4)), (ux0 + sc(4), uy0)],
              fill=(255, 255, 255))
    d.polygon([(ux1, uy0), (ux0, uy1), (ux0, uy1 - sc(4)), (ux1 - sc(4), uy0)],
              fill=(255, 255, 255))
    d.rectangle([(ux0 + ux1) // 2 - sc(2), uy0, (ux0 + ux1) // 2 + sc(2), uy1],
                fill=(200, 16, 46))
    d.rectangle([ux0, (uy0 + uy1) // 2 - sc(2), ux1, (uy0 + uy1) // 2 + sc(2)],
                fill=(200, 16, 46))


def art_bars(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(234, 240, 248))
    d.text((x0 + sc(4), y0 + sc(2)), "¥", font=sans_b(11), fill=NAVY)
    base = y1 - sc(6)
    heights = [0.45, 0.6, 0.78]
    w = (x1 - x0) // 4
    for i, h in enumerate(heights):
        bx = x0 + w * (i + 1) - sc(4)
        top = base - int((y1 - y0 - sc(12)) * h)
        d.rectangle([bx, top, bx + sc(8), base], fill=NAVY)
    d.line([x0 + sc(4), y0 + sc(8), x1 - sc(4), y0 + sc(8)], fill=RED,
           width=max(1, S))


def art_bank(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(242, 239, 230))
    cx = (x0 + x1) // 2
    d.polygon([(cx - sc(16), y0 + sc(12)), (cx + sc(16), y0 + sc(12)),
               (cx, y0 + sc(4))], fill=NAVY)
    for i in range(3):
        colx = x0 + sc(8) + i * sc(12)
        d.rectangle([colx, y0 + sc(14), colx + sc(5), y1 - sc(8)], fill=NAVY)
    d.rectangle([x0 + sc(5), y1 - sc(8), x1 - sc(5), y1 - sc(4)], fill=NAVY)
    d.text((x1 - sc(14), y0 + sc(2)), "%", font=sans_b(10), fill=RED)


def art_cricket(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 240, 228))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # bat (tan, angled)
    d.polygon([(cx - sc(2), cy - sc(14)), (cx + sc(4), cy - sc(12)),
               (cx - sc(2), cy + sc(12)), (cx - sc(8), cy + sc(10))],
              fill=(210, 180, 140))
    d.rectangle([cx - sc(4), cy - sc(18), cx - sc(1), cy - sc(13)],
                fill=(120, 90, 60))
    # ball
    d.ellipse([cx + sc(6), cy + sc(4), cx + sc(12), cy + sc(10)], fill=RED)
    # stumps
    for i in range(3):
        sx = x1 - sc(16) + i * sc(4)
        d.rectangle([sx, y1 - sc(14), sx + sc(2), y1 - sc(4)], fill=(180, 140, 90))


def art_ballot(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(239, 230, 242))
    cx = (x0 + x1) // 2
    d.rectangle([cx - sc(14), y0 + sc(16), cx + sc(14), y1 - sc(4)],
                fill=NAVY)
    d.rectangle([cx - sc(8), y0 + sc(14), cx + sc(8), y0 + sc(17)],
                fill=(255, 255, 255))
    d.polygon([(cx - sc(4), y0 + sc(4)), (cx + sc(8), y0 + sc(2)),
               (cx + sc(6), y0 + sc(12)), (cx - sc(6), y0 + sc(14))],
              fill=(255, 255, 255))
    # green check on the slip
    d.line([cx - sc(3), y0 + sc(8), cx, y0 + sc(11), cx + sc(5), y0 + sc(5)],
           fill=GREEN, width=max(2, 2 * S))


def art_boat(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(220, 233, 242))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([x0 + sc(3), y1 - sc(12), x1 - sc(3), y1 - sc(12)], fill=TEAL,
           width=max(2, 2 * S))
    d.arc([x0 + sc(2), y1 - sc(18), x1 - sc(2), y1 - sc(4)], start=0, end=180,
          fill=TEAL, width=max(1, S))
    d.polygon([(cx - sc(12), cy), (cx + sc(12), cy), (cx + sc(8), cy + sc(8)),
               (cx - sc(8), cy + sc(8))], fill=(139, 90, 43))
    d.polygon([(cx, cy - sc(12)), (cx, cy), (cx + sc(10), cy)], fill=(255, 255, 255))
    d.line([cx, cy - sc(13), cx, cy], fill=(60, 60, 60), width=max(1, S))


def art_strike(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(247, 232, 232))
    cx = (x0 + x1) // 2
    d.rectangle([cx - sc(2), y0 + sc(16), cx + sc(2), y1 - sc(2)],
                fill=(120, 90, 60))
    px0, py0, px1, py1 = cx - sc(24), y0 + sc(4), cx + sc(24), y0 + sc(18)
    d.rectangle([px0, py0, px1, py1], fill=(255, 255, 255),
                outline=RED, width=max(1, S))
    f = sans_b(9)
    t = "SCIOPERO"
    draw_centered(d, cx, py0 + sc(3), t, f, RED)


def art_pill(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(230, 242, 236))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - sc(2)
    d.rounded_rectangle([cx - sc(16), cy - sc(6), cx + sc(16), cy + sc(6)],
                        radius=sc(6), fill=(255, 255, 255), outline=GRAY,
                        width=max(1, S))
    d.rounded_rectangle([cx - sc(16), cy - sc(6), cx, cy + sc(6)],
                        radius=sc(6), fill=RED)
    d.rectangle([cx - sc(4), cy - sc(6), cx, cy + sc(6)], fill=RED)
    for ox, oy in ((-12, 12), (10, 12), (0, 14)):
        d.ellipse([cx + sc(ox) - sc(2), cy + sc(oy) - sc(2),
                   cx + sc(ox) + sc(2), cy + sc(oy) + sc(2)], fill=TEAL)


ART = {
    "cyclone": art_cyclone,
    "missiles": art_missiles,
    "climate": art_climate,
    "candles": art_candles,
    "mercury": art_mercury,
    "flags": art_flags,
    "bars": art_bars,
    "bank": art_bank,
    "cricket": art_cricket,
    "ballot": art_ballot,
    "boat": art_boat,
    "strike": art_strike,
    "pill": art_pill,
}


# ---------------------------------------------------------------- build

def build():
    random.seed(SEED)
    data = load_data()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header: eyebrow, masthead, subhead, rule
    draw_centered(d, sc(512), sc(9), data["eyebrow"], sans_b(11), NAVY)
    draw_centered(d, sc(512), sc(26), data["masthead"], serif_b(46), NAVY)
    draw_centered(d, sc(512), sc(86), data["subhead"], sans(12), (70, 70, 70))
    d.line([sc(8), sc(106), sc(1016), sc(106)], fill=NAVY, width=sc(2))

    # ---- stat strip
    d.rectangle([sc(8), sc(108), sc(1016), sc(160)], fill=STAT_BG)
    stats = data["stats"]
    cell_w = (1016 - 8) / 6
    for i, st in enumerate(stats):
        cx = 8 + cell_w * (i + 0.5)
        draw_centered(d, sc(cx), sc(114), st["value"], sans_b(20), NAVY)
        label_lines = wrap(st["label"], sans(9), sc(cell_w - 12))
        ly = sc(140)
        for ln in label_lines[:2]:
            draw_centered(d, sc(cx), ly, ln, sans(9), (70, 70, 70))
            ly += sc(11)
        if i:
            x = sc(8 + cell_w * i)
            d.line([x, sc(114), x, sc(154)], fill=RULE, width=sc(1))

    # ---- region strip
    region_text = "  ·  ".join(f"{r['name']} {r['count']}" for r in data["regions"])
    draw_centered(d, sc(512), sc(164), region_text, sans_b(10), NAVY)

    # ---- featured stories: big 3, then two rows of 5
    featured = data["featured"]

    def story_cell(s, x, y, w, h, big):
        art = ART[s["art"]]
        art(d, sc(x + 4), sc(y + 4), sc(x + w - 4),
            sc(y + (48 if big else 44)))
        place_size = 11 if big else 10
        head_size = 15 if big else 11
        body_size = 10 if big else 9
        stamp_size = 9 if big else 8
        ycur = y + (52 if big else 48)
        if big:
            # big cells carry the stamp on the place line (no room for a
            # separate stamp row under a 3-line body)
            d.text((sc(x + 4), sc(ycur)),
                   f"{s['place']} · {s['topic']} · {s['stamp']}",
                   font=sans_b(place_size), fill=NAVY)
        else:
            d.text((sc(x + 4), sc(ycur)),
                   f"{s['place']} · {s['topic']}",
                   font=sans_b(place_size), fill=NAVY)
        ycur += 13 if big else 12
        head_lines = wrap(s["headline"],
                          serif_b(head_size) if big else sans_b(head_size),
                          sc(w - 8))
        for ln in head_lines[:2]:
            d.text((sc(x + 4), sc(ycur)), ln,
                   font=serif_b(head_size) if big else sans_b(head_size),
                   fill=INK)
            ycur += 17 if big else 13
        body = f"{s['body']} ({s['source']})"
        body_lines = wrap(body, sans(body_size), sc(w - 8))
        for ln in body_lines[:3]:
            d.text((sc(x + 4), sc(ycur)), ln, font=sans(body_size),
                   fill=(50, 50, 50))
            ycur += 12 if big else 11
        if not big:
            d.text((sc(x + 4), sc(y + h - 11)), s["stamp"],
                   font=sans(stamp_size), fill=GRAY)

    # big 3
    bw = (1008 - 12) / 3
    for i, s in enumerate(featured[:3]):
        x = 8 + i * (bw + 6)
        story_cell(s, x, 180, bw, 138, big=True)
        if i:
            d.line([sc(x - 3), sc(184), sc(x - 3), sc(314)], fill=RULE,
                   width=sc(1))
    # medium rows
    mw = (1008 - 4 * 6) / 5
    for row in range(2):
        y = 318 + row * 142
        for i, s in enumerate(featured[3 + row * 5: 3 + (row + 1) * 5]):
            x = 8 + i * (mw + 6)
            story_cell(s, x, y, mw, 142, big=False)
            if i:
                d.line([sc(x - 3), sc(y + 4), sc(x - 3), sc(y + 138)],
                       fill=RULE, width=sc(1))

    # ---- map: dot-matrix world, light land, big numbered pins
    mx0, my0, mx1, my1 = 8, 602, 1016, 736
    d.rectangle([sc(mx0), sc(my0), sc(mx1), sc(my1)], fill=MAP_BG)
    d.rectangle([sc(mx0), sc(my0), sc(mx1), sc(my1)], outline=RULE,
                width=sc(1))
    step = 7
    dot_r = 2.6
    for gx in range(mx0 + 4, mx1 - 2, step):
        for gy in range(my0 + 4, my1 - 2, step):
            lon = (gx - mx0) / (mx1 - mx0) * 360.0 - 180.0
            lat = 85.0 - (gy - my0) / (my1 - my0) * 145.0
            if on_land(lon, lat):
                d.ellipse([sc(gx - dot_r), sc(gy - dot_r),
                           sc(gx + dot_r), sc(gy + dot_r)], fill=LAND_DOT)
    d.text((sc(mx0 + 6), sc(my0 + 4)), "WORLD MAP — WHERE IT HAPPENED",
           font=sans_b(9), fill=GRAY)

    def lonlat_to_xy(lon, lat):
        x = mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)
        y = my0 + (85.0 - lat) / 145.0 * (my1 - my0)
        return [x, y]

    true_pts = [lonlat_to_xy(s["lon"], s["lat"]) for s in featured]
    adj = [list(p) for p in true_pts]
    min_d = 26.0
    for _ in range(60):
        moved = False
        for i in range(len(adj)):
            for j in range(i + 1, len(adj)):
                dx = adj[j][0] - adj[i][0]
                dy = adj[j][1] - adj[i][1]
                dist = math.hypot(dx, dy)
                if 0.01 < dist < min_d:
                    push = (min_d - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    adj[i][0] -= ux * push
                    adj[i][1] -= uy * push
                    adj[j][0] += ux * push
                    adj[j][1] += uy * push
                    moved = True
        if not moved:
            break
    for p in adj:
        p[0] = max(mx0 + 13, min(mx1 - 13, p[0]))
        p[1] = max(my0 + 13, min(my1 - 13, p[1]))
    pin_r = 11
    for s, tp, ap in zip(featured, true_pts, adj):
        if math.hypot(ap[0] - tp[0], ap[1] - tp[1]) > 3:
            d.line([sc(tp[0]), sc(tp[1]), sc(ap[0]), sc(ap[1])],
                   fill=(120, 120, 120), width=sc(1))
            d.ellipse([sc(tp[0] - 2), sc(tp[1] - 2), sc(tp[0] + 2),
                       sc(tp[1] + 2)], fill=RED)
        d.ellipse([sc(ap[0] - pin_r - 1), sc(ap[1] - pin_r - 1),
                   sc(ap[0] + pin_r + 1), sc(ap[1] + pin_r + 1)],
                  fill=(255, 255, 255))
        d.ellipse([sc(ap[0] - pin_r), sc(ap[1] - pin_r),
                   sc(ap[0] + pin_r), sc(ap[1] + pin_r)], fill=RED)
        num = str(s["id"])
        nf = sans_b(12)
        draw_centered(d, sc(ap[0]), sc(ap[1] - 8), num, nf, (255, 255, 255))
    d.text((sc(mx0 + 6), sc(my1 - 12)), data["mapNote"], font=sans(8),
           fill=GRAY)

    # ---- briefs 14–36
    by = 736
    d.text((sc(8), sc(by)), "THE DAY IN BRIEF", font=sans_b(11), fill=NAVY)
    # right-align the 14-36 label
    tw = sans_b(11).getlength("14–36")
    d.text((sc(1016) - tw, sc(by)), "14–36", font=sans_b(11), fill=GRAY)
    d.line([sc(8), sc(by + 14), sc(1016), sc(by + 14)], fill=RULE,
           width=sc(1))
    briefs = data["briefs"]
    col_w = (1008 - 12) / 2
    row_h = 12.5
    for idx, b in enumerate(briefs):
        col = idx // 12
        row = idx % 12
        x = 8 + col * (col_w + 12)
        y = by + 16 + row * row_h
        num = f"{b['id']}"
        place = b["place"]
        rest = f" — {b['text']} ({b['source']})"
        for size in (10, 9.5, 9, 8.5, 8):
            f_num = sans_b(size)
            f_pl = sans_b(size)
            f_tx = sans(size)
            total = (f_num.getlength(num + " ")
                     + f_pl.getlength(place)
                     + f_tx.getlength(rest))
            if total <= sc(col_w):
                break
        cx = sc(x)
        d.text((cx, sc(y)), num + " ", font=f_num, fill=RED)
        cx += f_num.getlength(num + " ")
        d.text((cx, sc(y)), place, font=f_pl, fill=NAVY)
        cx += f_pl.getlength(place)
        d.text((cx, sc(y)), rest, font=f_tx, fill=INK)

    # ---- DATE CHECK strip
    dy = 902
    d.rectangle([sc(8), sc(dy), sc(1016), sc(978)], fill=NAVY2)
    d.text((sc(16), sc(dy + 5)), data["dateCheckTitle"], font=sans_b(11),
           fill=YELLOW)
    items = data["dateCheck"]
    half = 6
    for col in range(2):
        col_items = items[col * half:(col + 1) * half]
        x = 16 + col * 500
        for k, item in enumerate(col_items):
            yy = dy + 20 + k * 10
            d.text((sc(x), sc(yy)), "×  " + item, font=sans(9),
                   fill=(255, 255, 255))

    # ---- NOT YET band
    d.rectangle([sc(8), sc(978), sc(1016), sc(992)], fill=NOTYET_BG)
    draw_centered(d, sc(512), sc(980), data["notYet"], sans_b(10), NAVY)

    # ---- footer
    d.text((sc(8), sc(994)), data["footerDisclaimer"], font=sans(8),
           fill=GRAY)
    d.text((sc(8), sc(1005)), data["footerSources"], font=sans(8),
           fill=GRAY)

    out = img.resize((1024, 1024), Image.LANCZOS)
    # In the grader the repo is read-only: write the poster to
    # MAKEFUN_OUTPUT_DIR when it is set, else next to this script.
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", HERE))
    out.save(out_dir / "entry.png")
    print(f"saved entry.png {out.size[0]}x{out.size[1]}")


if __name__ == "__main__":
    build()
