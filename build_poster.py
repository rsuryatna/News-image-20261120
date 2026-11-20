#!/usr/bin/env python3
"""Build the news-image-20261120 poster from scratch with PIL.

Newspaper front page, 1024x1024 PNG, 36 verified stories of Friday
20 November 2026. Drawn at 2x (2048x2048) and downscaled with LANCZOS.
All drawings are original vector-style scenes made here with PIL
primitives (gradients, arcs, polygons, soft shadows, seeded grain).
No network, no randomness except seeded numpy (deterministic output).
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2                      # supersampling factor
W, H = 1024 * S, 1024 * S
M = 28 * S                 # side margin
CW = W - 2 * M             # content width

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (163, 22, 33)
RED_DK = (120, 16, 24)
NAVY = (18, 32, 58)
NAVY2 = (24, 46, 80)
TEAL = (14, 94, 96)
GOLD = (176, 132, 40)
GREY = (110, 108, 100)
LGREY = (200, 196, 184)
CREAM = (238, 232, 214)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size * S / 2) if False else int(size))


def F(path, px):
    """Font sized in 1x pixels; internally we draw at 2x."""
    return ImageFont.truetype(path, int(px * S))


def wrap(text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(size, stops):
    """Vertical multi-stop gradient. stops: list of (pos0..1, rgb)."""
    w, h = size
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    ys = np.linspace(0, 1, h)
    cols = np.array([c for _, c in stops], dtype=float)
    pos = np.array([p for p, _ in stops], dtype=float)
    for ch in range(3):
        arr[:, :, ch] = np.interp(ys, pos, cols[:, ch])[:, None]
    return Image.fromarray(arr, "RGB")


def hgrad(size, stops):
    w, h = size
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    xs = np.linspace(0, 1, w)
    cols = np.array([c for _, c in stops], dtype=float)
    pos = np.array([p for p, _ in stops], dtype=float)
    for ch in range(3):
        arr[:, :, ch] = np.interp(xs, pos, cols[:, ch])[None, :]
    return Image.fromarray(arr, "RGB")


def radial_glow(size, color, max_alpha=200):
    """Soft round glow, transparent at edges."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w / 2, h / 2
    d = np.sqrt(((xx - cx) / (w / 2)) ** 2 + ((yy - cy) / (h / 2)) ** 2)
    a = np.clip(1 - d, 0, 1) ** 2 * max_alpha
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = color
    arr[:, :, 3] = a.astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def soft_shape(draw_layer, draw_fn, blur):
    """Draw shapes on a layer, blur it, return RGBA overlay."""
    ov = Image.new("RGBA", draw_layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    draw_fn(d)
    return ov.filter(ImageFilter.GaussianBlur(blur))


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def grain(img, seed=1234, amount=0.05):
    rng = np.random.RandomState(seed)
    noise = rng.randint(118, 139, size=(img.height, img.width, 1), dtype=np.uint8)
    noise = np.repeat(noise, 3, axis=2)
    nimg = Image.fromarray(noise, "RGB")
    return Image.blend(img, nimg, amount)


# ---------------------------------------------------------------- data
STATS = [
    ("300,000+", "evacuated ahead of Cyclone Akvan"),
    ("~30", "ballistic missiles fired at Kyiv"),
    ("\u221217.5%", "Taiex's worst week since 1991"),
    ("2.2%", "Japan Oct CPI; BoJ hike eyed"),
    ("118", "Phillips' historic century vs India"),
    ("$97.17", "Anthropic first close, +17%"),
]

REGIONS = [
    ("EUROPE", 7, (26, 64, 110)),
    ("AMERICAS", 7, (163, 22, 33)),
    ("ASIA-PACIFIC", 10, (14, 94, 96)),
    ("MIDEAST", 3, (120, 90, 20)),
    ("AFRICA", 3, (60, 90, 40)),
    ("OCEANIA", 4, (90, 60, 110)),
    ("WORLD / SPACE", 2, (80, 80, 80)),
]

# featured: num, kicker, stamp, tag, headline, body, source
FEATURED_BIG = [
    (1, "ODISHA, INDIA \u00b7 CYCLONE", "GOPALPUR \u00b7 03:00 UTC", "REPORTED",
     "Cyclone Akvan makes landfall in eastern India",
     "Severe storm crosses near Gopalpur; 300,000+ evacuated, winds 70\u201380 "
     "gusting 90 km/h, 423 rescue teams deployed, schools shut.",
     "IMD, Reuters"),
    (2, "KYIV, UKRAINE \u00b7 WAR", "KYIV \u00b7 01:25 LOCAL", "REPORTED",
     "Russia fires wave of ~30 ballistic missiles at Kyiv",
     "Seven overnight waves hit energy and transport sites; fires burn in "
     "three districts; 3 killed, ~15 hurt; 3 Dnipro bridges damaged.",
     "Kyiv Independent, Reuters"),
    (3, "ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE", "ANTALYA \u00b7 20 NOV", "REPORTED",
     "COP31 reaches its final day deadlocked",
     "Closing draft omits fossil-fuel phase-out while $120bn adaptation "
     "finance stays unresolved; hosts push \u201c35 by 35\u201d clean-power goal.",
     "UN News, Reuters"),
]

FEATURED_MED = [
    (4, "SEOUL / TOKYO \u00b7 MARKETS", "TOKYO CLOSE \u00b7 06:00 UTC", "REPORTED",
     "AI sell-off sinks Asia to worst week since 2020",
     "Nikkei \u22124.9%, KOSPI \u22125.4%, Taiex \u22126.8%; SoftBank \u221214.6%.",
     "Reuters"),
    (5, "MERCURY \u00b7 SPACE", "MERCURY \u00b7 20 NOV", "REPORTED",
     "BepiColombo reaches Mercury after 8 years",
     "ESA/JAXA probe ends 6bn-mile trip; orbit insertion set for Saturday.",
     "ESA, BBC"),
    (6, "BRUSSELS \u00b7 EUROPE", "BRUSSELS \u00b7 20 NOV", "REPORTED",
     "Burnham holds first EU\u2013UK reset summit",
     "Costa & von der Leyen host UK PM; agrifood & carbon-market links eyed.",
     "EU Council"),
    (7, "TOKYO \u00b7 ECONOMY", "TOKYO \u00b7 08:30 LOCAL", "REPORTED",
     "Japan inflation hits 2.2%; BoJ hike eyed",
     "Oct headline CPI rises from 2.1%; core stays above 2% for second month.",
     "Reuters"),
    (8, "BEIJING \u00b7 RATES", "BEIJING \u00b7 20 NOV", "REPORTED",
     "China holds lending rates for 18th month",
     "1-year LPR stays at 3.0%, 5-year at 3.5% as expected.",
     "PBOC, Reuters"),
    (9, "WELLINGTON \u00b7 CRICKET", "WELLINGTON \u00b7 20 NOV", "REPORTED",
     "Phillips makes history with 118 vs India",
     "First NZ batter with centuries in all 3 formats vs India in a year.",
     "ICC, AP"),
    (10, "SAN SALVADOR \u00b7 POLITICS", "SAN SALVADOR \u00b7 20 NOV", "REPORTED",
     "Bukele registers for third-term bid",
     "Files with electoral tribunal for Feb 2027 vote; rights groups object.",
     "AP"),
    (11, "SENEGAL \u00b7 MIGRATION", "YENNE COAST \u00b7 20 NOV", "REPORTED",
     "Migrant boat capsizes off Yenne; 4 dead",
     "Dozens missing from ~50\u2013100 aboard as Canary arrivals surge.",
     "Al Jazeera"),
    (12, "ROME \u00b7 LABOUR", "ROME \u00b7 20 NOV", "REPORTED",
     "Italy's CGIL holds 24-hr general strike",
     "Unions rally across ~100 squares against 2027 budget; transit hit.",
     "CGIL, AFP"),
    (13, "BARCELONA \u00b7 HEALTH", "BARCELONA \u00b7 20 NOV", "REPORTED",
     "Pancreatic cancer pill shrinks tumours 60.7%",
     "Daraxonrasib + chemo beats chemo alone (23\u201342%) in early trial.",
     "Reuters"),
]

BRIEFS = [
    (14, "BRAZIL", "Lula meets chief Raoni as Indigenous land is recognised", "Al Jazeera"),
    (15, "SEOUL", "Ruling party moves to impeach Chief Justice Cho Hee-dae", "SBS"),
    (16, "BOUGAINVILLE", "Rio Tinto pledges $370m for Panguna mine legacy", "Reuters"),
    (17, "CANBERRA", "CBO warns AUKUS sub sales could shrink US fleet", "Reuters"),
    (18, "FLORIDA", "St. Johns River hits record 18.3 ft; four counties shut schools", "AP"),
    (19, "IOWA", "US Army sets noon detonation of 68 unstable explosive barrels", "AP"),
    (20, "TONGA", "Pacific kingdom declares emergency as El Ni\u00f1o drought bites", "RNZ"),
    (21, "WASHINGTON", "Pentagon puts US war cost against Iran at $4.8bn", "Reuters"),
    (22, "LONDON", "UK & Norway fund \u00a3100m+ for two Ukrainian naval vessels", "BBC"),
    (23, "COPENHAGEN", "Denmark's parliament approves Greenland defence bill", "AFP"),
    (24, "JAKARTA", "Indonesia's parliament passes asset-forfeiture bill", "Reuters"),
    (25, "GLOBAL", "UN marks World Children's Day across member states", "UN News"),
    (26, "SENEGAL", "President Faye enacts supplementary budget by decree", "AFP"),
    (27, "HORMUZ", "Four attacks on vessels in 96 hours, maritime centre says", "UKMTO"),
    (28, "NEW DELHI", "Pakistan minister to lead delegation to SCO dialogue", "The Hindu"),
    (29, "QATAR", "U17 World Cup: Australia stun Argentina 2\u20130", "FIFA"),
    (30, "SOUTH AFRICA", "Hamza spins Proteas to Test win; Bavuma sets record", "ICC"),
    (31, "TAIWAN", "Short-sell curbs take effect; two Russian bombers tracked", "Reuters"),
    (32, "TURIN", "Alcaraz\u2013Cobolli & Medvedev\u2013Tiafoe close ATP Finals groups", "ATP"),
    (33, "LOS ANGELES", "GTA VI's first full day on sale; Metacritic 99", "Sensor Tower"),
    (34, "NEW YORK", "Anthropic ends first day up 17%, closing at $97.17", "Reuters"),
    (35, "COX'S BAZAR", "Rohingya camps weep and pray after ICJ ruling", "Reuters"),
    (36, "AUSTRALIA", "Xi meets Albanese a day after APEC summit", "AP"),
]

DATE_CHECK = [
    "Trump\u2013Xi\u2013Putin Shenzhen summit itself",
    "Anthropic's $83bn IPO pricing & Nasdaq debut",
    "ICJ Myanmar Rohingya genocide verdict",
    "GTA VI midnight launch",
    "$190.4m Van Gogh sale (Wed 18 Nov evening)",
    "EU \u20ac45bn loan for Ukraine (18 Nov)",
    "US\u2013Venezuela military deal",
    "Houthi strike on Riyadh PIF tower",
    "Kerch / Crimea Bridge strike (17 Nov)",
    "Senate 48\u201351 Iran war-powers vote",
    "Drone strike on Kyiv embassies",
]

# (num, lon, lat) pins on the map
PINS = [
    (1, 84.9, 19.3), (2, 30.5, 50.5), (3, 30.7, 36.9), (4, 127.0, 37.5),
    (6, 4.4, 50.8), (7, 139.7, 35.7), (8, 116.4, 39.9), (9, 174.8, -41.3),
    (10, -89.2, 13.7), (11, -17.4, 14.7), (12, 12.5, 41.9), (13, -2.0, 43.0),
]

# ---------------------------------------------------------------- illustrations
# Each returns an RGB image of size (w, h). All original drawings.

def ill_akvan(w, h):
    img = vgrad((w, h), [(0.0, (16, 44, 66)), (0.55, (22, 78, 96)), (1.0, (10, 60, 78))])
    d = ImageDraw.Draw(img)
    # landmass (India coast) left, sandy
    d.polygon([(0, 0), (w * 0.34, 0), (w * 0.30, h * 0.30), (w * 0.22, h * 0.62),
               (w * 0.26, h), (0, h)], fill=(214, 196, 150))
    d.line([(w * 0.34, 0), (w * 0.30, h * 0.30), (w * 0.22, h * 0.62), (w * 0.26, h)],
           fill=(120, 100, 60), width=max(2, w // 220))
    # rain streaks
    rng = np.random.RandomState(5)
    for _ in range(46):
        x = rng.randint(int(w * 0.36), w)
        y = rng.randint(0, h)
        ln = rng.randint(h // 14, h // 7)
        d.line([(x, y), (x - ln // 4, y + ln)], fill=(200, 225, 235, 90), width=max(2, w // 300))
    # cyclone spiral: concentric arcs, white/blue
    cx, cy = int(w * 0.62), int(h * 0.52)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for i, r in enumerate(range(12, int(w * 0.34), 16)):
        a0 = i * 55
        od.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 250,
               fill=(255, 255, 255, 235 - i * 14), width=max(3, w // 130))
    ov = ov.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(240, 244, 246),
              outline=(120, 150, 165), width=2)
    # landfall marker
    mx, my = int(w * 0.27), int(h * 0.46)
    d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=RED, outline=(255, 255, 255), width=2)
    d.text((mx + 12, my - 8), "Gopalpur", font=F(SANS_B, 11), fill=(255, 255, 255))
    return img


def ill_kyiv(w, h):
    img = vgrad((w, h), [(0.0, (8, 12, 28)), (0.6, (20, 28, 52)), (1.0, (40, 30, 34))])
    d = ImageDraw.Draw(img)
    # stars
    rng = np.random.RandomState(11)
    for _ in range(40):
        x, y = rng.randint(0, w), rng.randint(0, int(h * 0.55))
        r = rng.randint(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(220, 225, 240))
    # missile trails with glow
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    trails = [(0.12, 0.92, 0.55, 0.18), (0.30, 0.95, 0.72, 0.10), (0.55, 0.95, 0.90, 0.30)]
    for (x0, y0, x1, y1) in trails:
        pts = []
        for t in np.linspace(0, 1, 24):
            x = w * (x0 + (x1 - x0) * t)
            y = h * (y0 + (y1 - y0) * t - 0.16 * math.sin(t * math.pi))
            pts.append((x, y))
        od.line(pts, fill=(255, 140, 40, 230), width=max(3, w // 110), joint="curve")
        ex, ey = pts[-1]
        od.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=(255, 180, 80, 220))
    ov = ov.filter(ImageFilter.GaussianBlur(2.5))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)
    # city skyline
    base = int(h * 0.86)
    x = 0
    rng2 = np.random.RandomState(3)
    while x < w:
        bw = rng2.randint(w // 14, w // 8)
        bh = rng2.randint(h // 5, h // 2)
        d.rectangle([x, base - bh, x + bw, base], fill=(10, 12, 22))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(x + 5, x + bw - 5, 12):
                if rng2.rand() < 0.35:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 205, 110))
        x += bw + 3
    # river + bridge
    d.rectangle([0, base, w, h], fill=(16, 26, 46))
    d.line([(0, base + h * 0.05), (w, base + h * 0.05)], fill=(90, 120, 160), width=2)
    bx = int(w * 0.55)
    d.line([(bx, base), (bx + w * 0.28, base)], fill=(200, 200, 210), width=4)
    for px in range(bx, bx + int(w * 0.28), 26):
        d.line([(px, base), (px, base - 18)], fill=(200, 200, 210), width=2)
    # explosion glow at bridge
    gl = radial_glow((int(w * 0.3), int(h * 0.34)), (255, 120, 30), 170)
    img.paste(gl, (int(w * 0.62), int(h * 0.60)), gl)
    return img


def ill_cop31(w, h):
    img = vgrad((w, h), [(0.0, (250, 214, 150)), (0.5, (240, 170, 110)), (1.0, (30, 110, 120))])
    d = ImageDraw.Draw(img)
    # sun
    sx, sy = int(w * 0.78), int(h * 0.30)
    gl = radial_glow((int(w * 0.5), int(h * 0.5)), (255, 220, 130), 190)
    img.paste(gl, (sx - int(w * 0.25), sy - int(h * 0.25)), gl)
    d = ImageDraw.Draw(img)
    d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=(255, 226, 140),
              outline=(230, 180, 80), width=3)
    # sea
    d.rectangle([0, int(h * 0.62), w, h], fill=(16, 88, 102))
    for i in range(5):
        yy = int(h * (0.68 + i * 0.07))
        d.arc([-20, yy - 8, w + 20, yy + 8], 200, 340, fill=(140, 210, 220), width=3)
    # globe
    cx, cy, r = int(w * 0.30), int(h * 0.38), int(w * 0.17)
    gl2 = radial_glow((r * 2, r * 2), (120, 200, 230), 120)
    img.paste(gl2, (cx - r, cy - r), gl2)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 150, 200), outline=(255, 255, 255), width=3)
    for ang in (-50, -20, 15, 50):
        a = math.radians(ang)
        d.ellipse([cx - r * abs(math.cos(a)), cy - r, cx + r * abs(math.cos(a)), cy + r],
                  outline=(220, 240, 245), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(220, 240, 245), width=2)
    d.ellipse([cx - r * 0.55, cy - r * 0.5, cx - r * 0.05, cy - r * 0.1], fill=(70, 150, 90))
    d.ellipse([cx + r * 0.1, cy + r * 0.05, cx + r * 0.6, cy + r * 0.55], fill=(70, 150, 90))
    d.ellipse([cx - r * 0.2, cy + r * 0.35, cx + r * 0.25, cy + r * 0.7], fill=(90, 170, 100))
    # thermometer
    tx = int(w * 0.60)
    d.rounded_rectangle([tx, int(h * 0.14), tx + 22, int(h * 0.72)], radius=11,
                        fill=(245, 245, 240), outline=(120, 60, 60), width=2)
    d.rounded_rectangle([tx + 4, int(h * 0.42), tx + 18, int(h * 0.68)], radius=8, fill=RED)
    d.ellipse([tx - 8, int(h * 0.66), tx + 30, int(h * 0.92)], fill=RED, outline=(120, 60, 60), width=2)
    return img


def ill_aiselloff(w, h):
    img = vgrad((w, h), [(0.0, (28, 10, 12)), (1.0, (52, 14, 16))])
    d = ImageDraw.Draw(img)
    # grid
    for i in range(1, 5):
        y = int(h * i / 5)
        d.line([(0, y), (w, y)], fill=(90, 45, 48), width=1)
    # falling candlesticks
    n = 9
    cw = w / (n + 1)
    top = h * 0.16
    for i in range(n):
        x = cw * (i + 0.7)
        o = top + i * h * 0.055 + (i % 3) * h * 0.02
        c = o + h * 0.16
        body = (x - cw * 0.22, o, x + cw * 0.22, c)
        d.line([(x, o - h * 0.05), (x, c + h * 0.05)], fill=(230, 60, 60), width=3)
        d.rectangle(body, fill=(215, 40, 40), outline=(255, 120, 110), width=2)
    # red trend line + arrow
    pts = [(cw * (i + 0.7), top + i * h * 0.055 + (i % 3) * h * 0.02 + h * 0.08) for i in range(n)]
    d.line(pts, fill=(255, 90, 80), width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey + 26), (ex - 16, ey + 2), (ex + 16, ey + 2)], fill=(255, 90, 80))
    return img


def ill_bepi(w, h):
    img = Image.new("RGB", (w, h), (6, 8, 18))
    d = ImageDraw.Draw(img)
    rng = np.random.RandomState(21)
    for _ in range(70):
        x, y = rng.randint(0, w), rng.randint(0, h)
        r = rng.randint(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(200, 210, 230))
    # trajectory (dotted arc)
    for t in np.linspace(0, 1, 40):
        x = w * (0.06 + 0.62 * t)
        y = h * (0.82 - 0.55 * t - 0.12 * math.sin(t * math.pi))
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(150, 190, 230))
    # Mercury
    cx, cy, r = int(w * 0.68), int(h * 0.42), int(w * 0.20)
    gl = radial_glow((r * 2, r * 2), (190, 170, 140), 110)
    img.paste(gl, (cx - r, cy - r), gl)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 152, 128),
              outline=(210, 195, 170), width=3)
    for (ox, oy, cr) in [(-0.4, -0.3, 0.22), (0.25, 0.1, 0.16), (-0.1, 0.35, 0.13),
                         (0.45, -0.35, 0.11), (0.0, -0.05, 0.09)]:
        d.ellipse([cx + ox * r - cr * r, cy + oy * r - cr * r,
                   cx + ox * r + cr * r, cy + oy * r + cr * r],
                  fill=(140, 125, 105), outline=(120, 105, 88), width=1)
    # spacecraft
    sx, sy = int(w * 0.24), int(h * 0.30)
    d.rectangle([sx - 34, sy - 8, sx - 8, sy + 8], fill=(40, 90, 160), outline=(150, 200, 255), width=2)
    d.rectangle([sx + 8, sy - 8, sx + 34, sy + 8], fill=(40, 90, 160), outline=(150, 200, 255), width=2)
    d.rectangle([sx - 8, sy - 12, sx + 8, sy + 12], fill=(220, 225, 235), outline=(120, 130, 150), width=2)
    return img


def ill_flags_eu_uk(w, h):
    img = vgrad((w, h), [(0.0, (232, 226, 208)), (1.0, (210, 202, 180))])
    d = ImageDraw.Draw(img)
    # EU flag
    ex, ey, ew, eh = int(w * 0.04), int(h * 0.18), int(w * 0.44), int(h * 0.64)
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(0, 51, 153))
    ccx, ccy = ex + ew // 2, ey + eh // 2
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = ccx + int(eh * 0.30 * math.cos(a))
        sy = ccy + int(eh * 0.30 * math.sin(a))
        d.polygon(star_points(sx, sy, 7, 3), fill=(255, 204, 0))
    # Union Jack (simplified but correct layout)
    ux, uy, uw, uh = int(w * 0.52), ey, ew, eh
    d.rectangle([ux, uy, ux + uw, uy + uh], fill=(1, 33, 105))
    d.polygon([(ux, uy), (ux + uw // 6, uy), (ux + uw, uy + uh - uh // 6), (ux + uw, uy + uh),
               (ux + uw - uw // 6, uy + uh), (ux, uy + uh // 6)], fill=(255, 255, 255))
    d.polygon([(ux + uw, uy), (ux + uw - uw // 6, uy), (ux, uy + uh - uh // 6), (ux, uy + uh),
               (ux + uw // 6, uy + uh), (ux + uw, uy + uh // 6)], fill=(255, 255, 255))
    d.polygon([(ux, uy), (ux + uw // 12, uy), (ux + uw, uy + uh - uh // 12), (ux + uw, uy + uh),
               (ux + uw - uw // 12, uy + uh), (ux, uy + uh // 12)], fill=(200, 16, 46))
    d.polygon([(ux + uw, uy), (ux + uw - uw // 12, uy), (ux, uy + uh - uh // 12), (ux, uy + uh),
               (ux + uw // 12, uy + uh), (ux + uw, uy + uh // 12)], fill=(200, 16, 46))
    d.rectangle([ux, uy + uh // 2 - uh // 10, ux + uw, uy + uh // 2 + uh // 10], fill=(255, 255, 255))
    d.rectangle([ux + uw // 2 - uw // 16, uy, ux + uw // 2 + uw // 16, uy + uh], fill=(255, 255, 255))
    d.rectangle([ux, uy + uh // 2 - uh // 18, ux + uw, uy + uh // 2 + uh // 18], fill=(200, 16, 46))
    d.rectangle([ux + uw // 2 - uw // 28, uy, ux + uw // 2 + uw // 28, uy + uh], fill=(200, 16, 46))
    return img


def ill_japan_cpi(w, h):
    img = vgrad((w, h), [(0.0, (244, 240, 228)), (1.0, (226, 220, 204))])
    d = ImageDraw.Draw(img)
    vals = [1.2, 1.5, 1.9, 2.1, 2.2]
    bw = w // 7
    base = int(h * 0.82)
    for i, v in enumerate(vals):
        x = int(w * 0.08 + i * bw)
        bh = int(h * 0.42 * v / 2.4)
        col = RED if i == len(vals) - 1 else (70, 90, 120)
        d.rectangle([x, base - bh, x + bw - 10, base], fill=col, outline=(40, 40, 40), width=1)
    d.line([(0, base), (w, base)], fill=INK, width=2)
    d.text((int(w * 0.05), int(h * 0.03)), "2.2%", font=F(SANS_B, 20), fill=RED_DK)
    return img


def ill_china_rates(w, h):
    img = vgrad((w, h), [(0.0, (222, 40, 44)), (1.0, (160, 20, 26))])
    d = ImageDraw.Draw(img)
    # bank building
    bx, by = int(w * 0.28), int(h * 0.36)
    bw, bh = int(w * 0.44), int(h * 0.46)
    d.polygon([(bx - 8, by), (bx + bw // 2, by - int(h * 0.14)), (bx + bw + 8, by)],
              fill=(245, 240, 225), outline=(120, 20, 20), width=2)
    for i in range(4):
        cx = bx + int(bw * (0.12 + i * 0.25))
        d.rectangle([cx, by + 6, cx + int(w * 0.05), by + bh], fill=(245, 240, 225))
    d.rectangle([bx - 6, by + bh, bx + bw + 6, by + bh + 10], fill=(245, 240, 225))
    d.text((int(w * 0.06), int(h * 0.12)), "3.0%  /  3.5%", font=F(SANS_B, 15),
           fill=(255, 235, 200))
    return img


def ill_cricket(w, h):
    img = vgrad((w, h), [(0.0, (120, 170, 90)), (1.0, (60, 120, 60))])
    d = ImageDraw.Draw(img)
    # pitch
    d.rectangle([int(w * 0.30), 0, int(w * 0.70), h], fill=(214, 190, 140))
    d.line([(int(w * 0.30), 0), (int(w * 0.30), h)], fill=(255, 255, 255), width=2)
    d.line([(int(w * 0.70), 0), (int(w * 0.70), h)], fill=(255, 255, 255), width=2)
    # stumps
    for sx in (int(w * 0.44), int(w * 0.50), int(w * 0.56)):
        d.rectangle([sx, int(h * 0.10), sx + 5, int(h * 0.24)], fill=(240, 210, 90))
    # bat (diagonal)
    d.rounded_rectangle([int(w * 0.58), int(h * 0.42), int(w * 0.72), int(h * 0.86)],
                        radius=8, fill=(222, 184, 120), outline=(120, 80, 30), width=2)
    d.rectangle([int(w * 0.63), int(h * 0.30), int(w * 0.67), int(h * 0.44)], fill=(150, 100, 40))
    # ball
    d.ellipse([int(w * 0.16), int(h * 0.62), int(w * 0.16) + 26, int(h * 0.62) + 26],
              fill=(178, 30, 30), outline=(255, 255, 255), width=2)
    d.text((int(w * 0.06), int(h * 0.06)), "118", font=F(SERIF_B, 26), fill=(255, 255, 255))
    return img


def ill_bukele(w, h):
    img = vgrad((w, h), [(0.0, (240, 236, 222)), (1.0, (222, 216, 200))])
    d = ImageDraw.Draw(img)
    # El Salvador stripes
    d.rectangle([0, 0, w, int(h * 0.30)], fill=(0, 71, 171))
    d.rectangle([0, int(h * 0.30), w, int(h * 0.62)], fill=(245, 245, 240))
    d.rectangle([0, int(h * 0.62), w, h], fill=(0, 71, 171))
    d.ellipse([int(w * 0.44), int(h * 0.34), int(w * 0.56), int(h * 0.58)],
              fill=(255, 205, 0), outline=(0, 71, 171), width=2)
    # ballot box
    bx, by = int(w * 0.30), int(h * 0.58)
    d.rounded_rectangle([bx, by, bx + int(w * 0.40), by + int(h * 0.34)], radius=6,
                        fill=(30, 60, 110), outline=(255, 255, 255), width=3)
    d.line([(bx + 8, by + 4), (bx + int(w * 0.40) - 8, by + 4)], fill=(255, 255, 255), width=3)
    d.rectangle([bx + int(w * 0.14), by - int(h * 0.16), bx + int(w * 0.26), by + 2],
                fill=(255, 255, 255), outline=(120, 120, 120), width=1)
    d.text((int(w * 0.05), int(h * 0.04)), "2027", font=F(SANS_B, 18), fill=(255, 255, 255))
    return img


def ill_senegal(w, h):
    img = vgrad((w, h), [(0.0, (250, 210, 140)), (0.45, (230, 160, 90)), (1.0, (14, 60, 96))])
    d = ImageDraw.Draw(img)
    d.ellipse([int(w * 0.72), int(h * 0.06), int(w * 0.72) + 44, int(h * 0.06) + 44],
              fill=(255, 220, 130), outline=(230, 180, 80), width=2)
    # sea
    d.rectangle([0, int(h * 0.55), w, h], fill=(16, 70, 110))
    for i in range(4):
        yy = int(h * (0.60 + i * 0.11))
        d.arc([-30, yy - 10, w + 30, yy + 10], 195, 345, fill=(150, 210, 235), width=3)
    # boat
    bx, by = int(w * 0.22), int(h * 0.52)
    d.polygon([(bx, by), (bx + int(w * 0.52), by), (bx + int(w * 0.44), by + int(h * 0.20)),
               (bx + int(w * 0.08), by + int(h * 0.20))], fill=(120, 72, 32),
              outline=(60, 35, 15), width=2)
    d.line([(bx + int(w * 0.26), by), (bx + int(w * 0.26), by - int(h * 0.22))],
           fill=(70, 45, 20), width=3)
    d.polygon([(bx + int(w * 0.26), by - int(h * 0.22)), (bx + int(w * 0.26), by - int(h * 0.02)),
               (bx + int(w * 0.46), by - int(h * 0.02))], fill=(245, 240, 225),
              outline=(150, 140, 120), width=1)
    # lifebuoy
    lx, ly = int(w * 0.70), int(h * 0.78)
    d.ellipse([lx, ly, lx + 34, ly + 34], fill=(255, 255, 255), outline=(230, 60, 40), width=6)
    d.ellipse([lx + 11, ly + 11, lx + 23, ly + 23], fill=(16, 70, 110))
    return img


def ill_italy(w, h):
    img = vgrad((w, h), [(0.0, (240, 236, 222)), (1.0, (214, 206, 188))])
    d = ImageDraw.Draw(img)
    # red banner
    d.rectangle([0, int(h * 0.06), w, int(h * 0.40)], fill=RED)
    d.text((int(w * 0.06), int(h * 0.12)), "SCIOPERO", font=F(SANS_B, 15), fill=(255, 255, 255))
    # crowd: heads + raised arms
    rng = np.random.RandomState(9)
    for i in range(9):
        x = int(w * (0.06 + i * 0.11))
        y = int(h * 0.70) + int(rng.randint(-8, 8))
        d.ellipse([x, y, x + 22, y + 22], fill=(60, 50, 45))
        d.line([(x + 20, y + 20), (x + 34, y - 6)], fill=(60, 50, 45), width=4)
        d.rectangle([x - 4, y + 22, x + 26, h], fill=(90, 80, 70))
    return img


def ill_cancer(w, h):
    img = vgrad((w, h), [(0.0, (235, 244, 246)), (1.0, (200, 225, 232))])
    d = ImageDraw.Draw(img)
    # medical cross
    cx, cy = int(w * 0.78), int(h * 0.22)
    d.rectangle([cx - 8, cy - 26, cx + 8, cy + 26], fill=(40, 140, 160))
    d.rectangle([cx - 26, cy - 8, cx + 26, cy + 8], fill=(40, 140, 160))
    # capsule, rotated via polygon approximation
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    cap = Image.new("RGBA", (int(w * 0.62), int(h * 0.30)), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cap)
    cd.rounded_rectangle([0, 0, cap.width, cap.height], radius=cap.height // 2, fill=(255, 255, 255),
                         outline=(40, 140, 160), width=3)
    cd.rectangle([cap.width // 2, 0, cap.width, cap.height], fill=(40, 160, 170))
    cd.rounded_rectangle([0, 0, cap.width, cap.height], radius=cap.height // 2,
                         outline=(40, 140, 160), width=3)
    cap = cap.rotate(28, expand=True, resample=Image.BICUBIC)
    ov.alpha_composite(cap, (int(w * 0.16), int(h * 0.42)))
    ov = ov.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((int(w * 0.06), int(h * 0.06)), "60.7%", font=F(SANS_B, 22), fill=(16, 110, 130))
    return img


ILLUSTRATORS = {
    1: ill_akvan, 2: ill_kyiv, 3: ill_cop31, 4: ill_aiselloff, 5: ill_bepi,
    6: ill_flags_eu_uk, 7: ill_japan_cpi, 8: ill_china_rates, 9: ill_cricket,
    10: ill_bukele, 11: ill_senegal, 12: ill_italy, 13: ill_cancer,
}

# ---------------------------------------------------------------- world map
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 62), (-55, 47),
     (-70, 42), (-75, 35), (-80, 25), (-90, 21), (-97, 16), (-105, 20), (-115, 30),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    # South America
    [(-80, 10), (-60, 10), (-50, 0), (-40, -10), (-35, -20), (-40, -30), (-55, -35),
     (-65, -40), (-70, -50), (-75, -55), (-70, -30), (-80, -15), (-80, 5)],
    # Europe
    [(-10, 36), (-5, 44), (0, 46), (5, 55), (10, 58), (18, 56), (25, 60), (30, 62),
     (30, 70), (20, 70), (10, 65), (5, 60), (-5, 58), (-10, 50), (-10, 43), (-15, 40)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
     (50, 10), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
     (12, -18), (10, -5), (5, 5), (-5, 5), (-15, 10)],
    # Asia
    [(30, 70), (50, 70), (70, 72), (90, 75), (110, 75), (130, 72), (150, 70),
     (170, 67), (178, 65), (170, 60), (160, 55), (140, 45), (135, 40), (130, 35),
     (122, 30), (120, 25), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
     (80, 15), (75, 8), (70, 20), (60, 25), (55, 26), (50, 30), (45, 30),
     (40, 35), (35, 36), (30, 40), (30, 55), (35, 65)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -35), (130, -32), (135, -35),
     (140, -38), (145, -38), (150, -37), (153, -30), (150, -22), (145, -15),
     (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
    # Greenland
    [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-25, 70), (-20, 72), (-30, 75),
     (-45, 76), (-55, 75), (-60, 70), (-58, 65)],
]


def point_in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and \
           (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=(90, 110, 140), width=2)
    # dotted continents
    step_lon, step_lat = 5.0, 5.0
    lon = -180.0
    while lon <= 180:
        lat = -55.0
        while lat <= 85:
            if any(point_in_poly(lon, lat, p) for p in CONTINENTS):
                px = x0 + (lon + 180) / 360 * w
                py = y0 + (85 - lat) / 140 * h
                r = 3.0
                d.ellipse([px - r, py - r, px + r, py + r], fill=(214, 198, 150))
            lat += step_lat
        lon += step_lon
    # pins
    fnum = F(SANS_B, 8)
    for num, plon, plat in PINS:
        px = x0 + (plon + 180) / 360 * w
        py = y0 + (85 - plat) / 140 * h
        r = 12
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=2)
        tw = d.textlength(str(num), font=fnum)
        d.text((px - tw / 2, py - 8), str(num), font=fnum, fill=(255, 255, 255))
    # space callout (story 5)
    bx, by = x0 + 14, y0 + h - 52
    d.rounded_rectangle([bx, by, bx + 150, by + 40], radius=5, fill=(20, 40, 70),
                        outline=(120, 140, 170), width=1)
    d.ellipse([bx + 10, by + 13, bx + 24, by + 27], fill=RED, outline=(255, 255, 255), width=1)
    d.text((bx + 15, by + 14), "5", font=F(SANS_B, 8), fill=(255, 255, 255))
    d.text((bx + 32, by + 11), "SPACE", font=F(SANS_B, 8), fill=(255, 255, 255))
    d.text((bx + 32, by + 24), "Mercury", font=F(SANS, 8), fill=(200, 210, 225))
    # legend
    lx, ly = x0 + w - 250, y0 + h - 34
    d.ellipse([lx, ly + 2, lx + 12, ly + 14], fill=RED, outline=(255, 255, 255), width=1)
    d.text((lx + 17, ly), "1\u201313 Feature stories", font=F(SANS, 8), fill=(210, 220, 235))


# ---------------------------------------------------------------- panels
def stamp_bar(img, w, stamp, tag):
    """Dark overlay strip at the bottom of an illustration."""
    d = ImageDraw.Draw(img, "RGBA")
    bh = int(img.height * 0.16)
    d.rectangle([0, img.height - bh, w, img.height], fill=(10, 12, 18, 215))
    f1 = F(SANS_B, 8)
    d.text((10, img.height - bh + 6), stamp, font=f1, fill=(255, 255, 255))
    tag_col = (34, 120, 60) if tag == "REPORTED" else ((170, 120, 20) if tag == "CLAIM" else (30, 90, 160))
    tw = d.textlength(tag, font=f1)
    tx = w - tw - 18
    d.rounded_rectangle([tx - 6, img.height - bh + 4, w - 8, img.height - 4],
                        radius=5, fill=tag_col)
    d.text((tx, img.height - bh + 6), tag, font=f1, fill=(255, 255, 255))


def featured_panel(d, x, y, w, h, item, big):
    num, kicker, stamp, tag, headline, body, source = item
    ill_h = 150 if big else 132
    ill_w = w - 4
    ill = ILLUSTRATORS[num](ill_w, ill_h)
    ill = ill.resize((ill_w, ill_h))
    stamp_bar(ill, ill_w, stamp, tag)
    # paste illustration via main image paste in caller; here draw border + text
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    ty = y + ill_h + 8
    fk = F(SANS_B, 9 if big else 8)
    d.text((x + 6, ty), f"{num:02d} \u00b7 {kicker}", font=fk, fill=RED_DK)
    ty += 22 if big else 20
    fh = F(SERIF_B, 15 if big else 13)
    lh = 36 if big else 31
    for line in wrap(headline, fh, w - 12)[:2]:
        d.text((x + 6, ty), line, font=fh, fill=INK)
        ty += lh
    fb = F(SANS, 10 if big else 9)
    lb = 25 if big else 22
    full = body + f" ({source})"
    for line in wrap(full, fb, w - 12)[:3]:
        d.text((x + 6, ty), line, font=fb, fill=(50, 48, 44))
        ty += lb
    return ill


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- eyebrow
    d.text((M, 24), "THE WORLD IN ONE DAY", font=F(SANS_B, 11), fill=RED)
    right = "FRIDAY'S NEWS \u00b7 ONE PAGE \u00b7 36 STORIES \u00b7 6 CONTINENTS"
    fr = F(SANS_B, 10)
    d.text((W - M - d.textlength(right, font=fr), 26), right, font=fr, fill=GREY)

    # ---- masthead
    d.text((M, 52), "Friday 20 November 2026", font=F(SERIF_B, 52), fill=INK)
    d.text((M, 162), "Cyclone Akvan strikes India \u2022 Ballistic missiles hit Kyiv \u2022 "
                     "COP31 deadlocked on final day \u2022 Asian AI sell-off",
           font=F(SERIF, 15), fill=RED)
    # double rule
    d.line([(M, 200), (W - M, 200)], fill=INK, width=4)
    d.line([(M, 206), (W - M, 206)], fill=INK, width=2)

    # ---- stat strip
    y0, y1 = 212, 308
    cell = CW // 6
    for i, (num, lab) in enumerate(STATS):
        cx = M + i * cell
        fn = F(SERIF_B, 21)
        tw = d.textlength(num, font=fn)
        d.text((cx + (cell - tw) / 2, y0 + 8), num, font=fn, fill=RED_DK)
        fl = F(SANS, 9)
        for j, line in enumerate(wrap(lab, fl, cell - 16)):
            tw2 = d.textlength(line, font=fl)
            d.text((cx + (cell - tw2) / 2, y0 + 52 + j * 20), line, font=fl, fill=(70, 68, 62))
        if i:
            d.line([(cx, y0 + 10), (cx, y1 - 10)], fill=LGREY, width=2)
    d.line([(M, y1), (W - M, y1)], fill=INK, width=2)

    # ---- region strip
    y0 = 316
    x = M
    for name, n, col in REGIONS:
        txt = f"{name} {n}"
        fnt = F(SANS_B, 10)
        tw = d.textlength(txt, font=fnt) + 22
        d.rounded_rectangle([x, y0, x + tw, y0 + 32], radius=4, fill=col)
        d.text((x + 11, y0 + 6), txt, font=fnt, fill=(255, 255, 255))
        x += tw + 10
    note = "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE"
    fn2 = F(SANS, 9)
    d.text((W - M - d.textlength(note, font=fn2), y0 + 8), note, font=fn2, fill=GREY)

    # ---- big 3 featured
    bw = (CW - 2 * 16) // 3
    y = 364
    for i, item in enumerate(FEATURED_BIG):
        x = M + i * (bw + 16)
        ill = featured_panel(d, x, y, bw, 340, item, big=True)
        img.paste(ill, (x + 2, y + 2))

    # ---- medium 10 featured (5 cols x 2 rows)
    mw = (CW - 4 * 14) // 5
    for row in range(2):
        y = 712 + row * 308
        for col in range(5):
            item = FEATURED_MED[row * 5 + col]
            x = M + col * (mw + 14)
            ill = featured_panel(d, x, y, mw, 300, item, big=False)
            img.paste(ill, (x + 2, y + 2))

    # ---- map + date check
    my = 1328
    mh = 320
    map_w = 880
    d.text((M, my), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=INK)
    sub = "Pins 1\u201313 (Lead & Feature)"
    d.text((M + map_w - d.textlength(sub, font=F(SANS, 9)), my + 2), sub,
           font=F(SANS, 9), fill=GREY)
    draw_map(d, M, my + 30, map_w, mh - 30)
    # date check box
    dx = M + map_w + 24
    dw = CW - map_w - 24
    d.rounded_rectangle([dx, my, dx + dw, my + mh], radius=6, fill=(253, 250, 240),
                        outline=RED, width=3)
    d.text((dx + 16, my + 10), "DATE CHECK", font=F(SANS_B, 12), fill=RED)
    d.text((dx + 16, my + 38),
           "First reported Thu 19 Nov, so NOT shown as Friday's news:",
           font=F(SANS_B, 9), fill=INK)
    fdc = F(SANS, 10)
    col_w = (dw - 32) // 2
    for i, item in enumerate(DATE_CHECK):
        c = i // 6
        r = i % 6
        xx = dx + 16 + c * col_w
        yy = my + 66 + r * 26
        d.text((xx, yy), "\u2022 " + item, font=fdc, fill=(60, 58, 52))
    # not-yet strip
    ny = my + mh - 44
    d.rectangle([dx + 16, ny, dx + dw - 16, ny + 32], fill=(238, 232, 214))
    d.text((dx + 24, ny + 6), "NOT YET \u2014 Sat 21 Nov: COP31 closing plenary \u00b7 "
                              "Las Vegas GP qualifying",
           font=F(SANS_B, 9), fill=RED_DK)

    # ---- briefs
    by = 1656
    d.text((M, by), "ALSO ON FRIDAY 20 NOVEMBER \u2014 23 MORE STORIES",
           font=F(SANS_B, 11), fill=INK)
    d.text((W - M - d.textlength("World Briefs (14\u201336)", font=F(SANS, 9)), by + 2),
           "World Briefs (14\u201336)", font=F(SANS, 9), fill=GREY)
    d.line([(M, by + 28), (W - M, by + 28)], fill=INK, width=2)
    fb = F(SANS, 10)
    fbb = F(SANS_B, 10)
    col_w = (CW - 24) // 2
    for i, (num, loc, head, src) in enumerate(BRIEFS):
        c = 0 if i < 12 else 1
        r = i if i < 12 else i - 12
        xx = M + c * (col_w + 24)
        yy = 1690 + r * 25
        d.text((xx, yy), f"{num}", font=fbb, fill=RED)
        nw = d.textlength(f"{num} ", font=fbb)
        d.text((xx + nw, yy), f"{loc} \u2014 ", font=fbb, fill=INK)
        lw = d.textlength(f"{loc} \u2014 ", font=fbb)
        d.text((xx + nw + lw, yy), f"{head} ({src})", font=fb, fill=(50, 48, 44))

    # ---- footer
    fy = 1998
    d.line([(M, fy), (W - M, fy)], fill=INK, width=2)
    d.text((M, fy + 8),
           "Every story here happened, or was first reported, on Friday 20 November 2026 "
           "in at least one time zone. Claims are attributed, not stated as fact.",
           font=F(SANS, 8), fill=(70, 68, 62))
    d.text((M, fy + 26),
           "Sources: Reuters, AP, AFP, BBC, IMD, UN News, Al Jazeera, ICC, EU Council, PBOC. "
           "Original vector drawings.",
           font=F(SANS, 8), fill=(90, 88, 82))

    # grain + downscale
    img = grain(img, seed=1234, amount=0.015)
    img = img.resize((1024, 1024), Image.LANCZOS)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    poster = build()
    poster.save(out, optimize=True, compress_level=9)
    print("saved", out)
