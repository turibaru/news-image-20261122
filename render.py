"""R7-FIX news-image-20261122 — render.py (compose baru dari spec R7-FIX).

SATU FIX vs R7: masthead 64px DejaVu Serif Bold, satu baris
"Sunday 22 November 2026" di (10, 28); kotak merah DIHAPUS dari band
masthead dan dipindah ke top bar kanan sebagai hitungan
"38 STORIES · 7 REGIONS · ONE DAY — ONE PICTURE". Semua yang lain
tetap seperti spec R7: 38 cerita (3 LEADS + 10 TEN + 1 kartu 35 +
24 ALSO), peta 330x216 + pin bernomor, ALSO 2 kolom, red restraint.
Kanvas 1024x1024, total vertikal 1024 tepat. Python + PIL saja.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (20, 20, 20)
NAVY = (27, 42, 74)
RED = (176, 30, 36)
GREY = (90, 90, 90)
LIGHT = (255, 255, 255)
CREAM = (250, 246, 236)
BODY = (60, 60, 60)
FRAME = (200, 190, 170)
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
REGION_COLORS = {
    "EUROPE": (14, 107, 122), "MIDDLE EAST": (176, 30, 36),
    "ASIA-PACIFIC": (217, 122, 31), "AMERICAS": (43, 94, 167),
    "AFRICA": (61, 139, 64), "OCEANIA": (122, 79, 163),
    "WORLD": (51, 51, 51),
}


def F(name, size):
    """Font DejaVu dari FONT_DIR, fallback load_default."""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def text_w(d, text, font):
    return d.textlength(text, font=font)


def wrap(d, text, font, max_w):
    """Bungkus teks per kata supaya tiap baris <= max_w."""
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(d, trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- DATA §3
# (nomor, region, topik, headline, isi, status, sumber) — LEADS
LEADS = [
    (1, "EUROPE", "WAR",
     "Russia fires 186 drones at Ukraine overnight; 161 downed",
     "Air defences down or jam 161 of 186 strike drones fired from eight "
     "directions; a five-storey block in Dymer is destroyed, 14 may be trapped.",
     "CONFIRMED", "Ukrainian Air Force, Reuters"),
    (2, "WORLD", "CLIMATE",
     "COP31's final text lands at dawn — with no mention of fossil fuels",
     "The ten-page package drops the $120bn adaptation target, keeps a 35% "
     "clean-electricity goal for 2035, and admits the world will overshoot 1.5C.",
     "ONGOING", "BBC, Reuters, The Guardian"),
    (3, "MIDDLE EAST", "GULF",
     "Iran claims strikes on US bases in Bahrain; two radars hit",
     "Tehran says it hit two Patriot radars at Al-Riffa and Awali Sakir. "
     "Bahrain says its defences intercepted the attacks; a facility burned, "
     "no casualties.",
     "CLAIM", "Al Jazeera, Reuters, IRGC statement"),
]
KICKERS = {1: "186 DRONES OVERNIGHT", 2: "COP31: FINAL TEXT",
           3: "CLAIM VS DENIAL"}

# (nomor, region, headline, isi, status, sumber) — TEN
TEN = [
    (4, "ASIA-PACIFIC", "Hong Kong elects its Election Committee",
     "856 candidates, 723 seats; 93.55% turnout.", "CONFIRMED", "SCMP"),
    (5, "AMERICAS", "Verstappen takes the Las Vegas GP",
     "0.639s clear of Norris; 75th win.", "CONFIRMED", "Reuters, F1"),
    (6, "OCEANIA", "India declare 720/9 — a record in NZ",
     "Rahul 136, Pant 128, Gill 98; record NZ total.", "CONFIRMED", "Reuters, AP"),
    (7, "AFRICA", "Bayelsa boat toll rises to 26",
     "Mourners' boat capsized Friday; recovery goes on.", "CONFIRMED", "RIA, Vanguard"),
    (8, "MIDDLE EAST", "Iran starts rationing electricity",
     "Two-hour daily cuts begin as gas output falls.", "CONFIRMED", "Tavani, RFE/RL"),
    (9, "ASIA-PACIFIC", "Candy-factory fire in Serang: 3 dead, 36 missing",
     "Benten plant blaze; search goes on.", "CONFIRMED", "Detiknews"),
    (10, "AMERICAS", "FBI probes hack of its crime database",
     "Washington pauses gun checks; breach assessed.", "REPORTED", "AP"),
    (11, "EUROPE", "Belgian controllers join strike",
     "Most flights grounded 07:00-21:00.", "CONFIRMED", "Reuters"),
    (12, "ASIA-PACIFIC", "Toxic-liquor toll in Manipur climbs to 19",
     "600 in hospital, six held; toll up from 11.", "CONFIRMED", "Xinhua"),
    (13, "AMERICAS", "Bolsonaro in intensive care",
     "Bowel obstruction, stable, breathing on his own.", "CONFIRMED", "Al Jazeera, Reuters"),
]

# (nomor, region, headline, status, sumber) — ALSO, 24 tampil.
# Nomor 15, 30, 32, 37, 38, 43, 44, 45 dibuang; 35 jadi kartu strip.
ALSO = [
    (14, "MIDDLE EAST", "Gaza: Israeli fire kills 4", "REPORTED", "Al Jazeera"),
    (16, "AFRICA", "Drones hit homes, Khartoum", "REPORTED", "AFP"),
    (17, "WORLD", "BepiColombo at Mercury", "CONFIRMED", "AP, ESA"),
    (18, "AMERICAS", "Nvidia SEC probe", "REPORTED", "Straits Times, CNBC"),
    (19, "EUROPE", "Pope hosts 1.3k poor", "CONFIRMED", "Vatican News"),
    (20, "AMERICAS", "Wembanyama 50, Spurs win", "CONFIRMED", "AP"),
    (21, "ASIA-PACIFIC", "Education minister quits", "CONFIRMED", "Reuters"),
    (22, "MIDDLE EAST", "Eisenkot asks Likud to talks", "REPORTED", "Reuters"),
    (23, "OCEANIA", "Marles: AUKUS claim wrong", "REPORTED", "Reuters"),
    (24, "ASIA-PACIFIC", "PM Shah begins India visit", "CONFIRMED", "Reuters"),
    (25, "ASIA-PACIFIC", "Snow strands 1,500 in Japan", "CONFIRMED", "dpa"),
    (26, "AFRICA", "Mlambo-Ngcuka dies, 71", "CONFIRMED", "Reuters"),
    (27, "EUROPE", "ATP Finals title match later today", "PENDING", "AP"),
    (28, "EUROPE", "Russia downs 170 Kyiv drones", "CLAIM", "Reuters"),
    (29, "EUROPE", "Estonia bars Russia line", "CONFIRMED", "Reuters"),
    (31, "WORLD", "Trump weighs nuclear talks, Putin, Xi", "REPORTED", ""),
    (33, "AFRICA", "Kenya frees last Ebola case", "CONFIRMED", "Wires"),
    (34, "EUROPE", "Denmark expels Russian attache", "REPORTED", "Guardian"),
    (36, "EUROPE", "EU hunts new ECB chief", "REPORTED", ""),
    (39, "AFRICA", "Nigeria builds its own warships", "CONFIRMED", ""),
    (40, "AFRICA", "ANC fights to hold big cities", "REPORTED", ""),
    (41, "AFRICA", "SA beat Australia by 176 runs, 2-1", "CONFIRMED", ""),
    (42, "ASIA-PACIFIC", "Bangladesh acts after district attacks", "REPORTED", ""),
    (46, "AFRICA", "DRC president signs reform law", "CONFIRMED", ""),
]
# Hitungan: 3 LEADS + 10 TEN + 1 kartu 35 + 24 ALSO = 38 cerita.
CARD35 = (35, "EUROPE", "Russian cargo ship Sparta II still burning",
          "CONFIRMED", "Reuters")

NUMBERS = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed or jammed"),
    ("35%", "clean-electricity goal for 2035"),
    ("$120bn", "adaptation target dropped"),
    ("720/9", "India's record Test total in NZ"),
    ("93.55%", "Hong Kong turnout by 14:00"),
]
REGIONS = [("EUROPE", 9), ("MIDDLE EAST", 4), ("ASIA-PACIFIC", 7),
           ("AMERICAS", 5), ("AFRICA", 8), ("OCEANIA", 2), ("WORLD", 3)]
UTC_ITEMS = [
    ("01:00", "HK polls open"), ("03:00", "COP31 objections close"),
    ("03:46", "Trump weighs nuclear talks with Putin, Xi"),
    ("05:11", "Hamas seeks talks"), ("05:30", "Verstappen wins Las Vegas GP"),
    ("06:00", "COP31 approval due"),
]
DATE_CHECK = (
    "DATE CHECK — READ THIS FIRST. Wires read to 07:00 UTC, Sunday "
    "22 November 2026. Every story here happened or was first reported on "
    "22 November 2026 (UTC). Left out on purpose: Russia's 400-drone barrage "
    "(19-20 Nov) — tonight's barrage was 186 drones, not 400; the Peru quake "
    "(Fri 20 Nov, USGS 6.7) — only the toll update is today's news; "
    "'El Chapo Isidro' arrest (Sat 21 Nov); the Shenzhen summit (19 Nov); "
    "Poland: two Russian missiles landed (Fri 20 Nov).")
LEGEND = (
    "HOW TO READ THE TAGS — CONFIRMED 2+ outlets · OFFICIAL on the record · "
    "REPORTED one outlet or witnesses · CLAIM one side's claim, contested · "
    "PENDING not settled yet · ONGOING still developing as we print.")
FOOTER = (
    "Sources: Reuters · AP · AFP · BBC · Al Jazeera · The Guardian · SCMP · "
    "dpa · Xinhua · Kyiv Independent · IRGC statement · Bahrain MoI · "
    "HK Govt · F1 · Cricbuzz · Vatican News — Scenes are drawn illustrations "
    "of reported events, not photographs. THE WORLD IN ONE DAY · 22 NOV 2026")
DECK = ("186 drones over Ukraine overnight · COP31's deal names no fossil "
        "fuels · Iran's radar claim meets Bahrain's denial")
TOP_RIGHT = "38 STORIES · 7 REGIONS · ONE DAY — ONE PICTURE"

# Peta: grid 44 kolom x 11 baris, tiap baris daftar rentang (c0, c1).
LAND = [
    [(5, 12), (16, 20)], [(3, 13), (15, 22), (30, 33)],
    [(2, 14), (16, 24), (28, 38)], [(4, 13), (17, 25), (27, 40)],
    [(6, 12), (18, 26), (28, 38), (40, 42)], [(8, 13), (19, 27), (30, 36)],
    [(10, 14), (20, 26), (31, 34)], [(12, 16), (22, 26)],
    [(24, 27)], [(38, 41)], [(39, 42)],
]
PINS = [
    (1, 0.494, 0.085), (2, 0.539, 0.341), (3, 0.607, 0.427),
    (4, 0.809, 0.341), (5, 0.135, 0.341), (6, 0.899, 0.768),
    (7, 0.472, 0.512), (8, 0.674, 0.256), (9, 0.719, 0.530),
    (10, 0.216, 0.341), (11, 0.404, 0.256), (12, 0.742, 0.230),
    (13, 0.270, 0.548),
]
MAP_LABELS = [
    ("AMERICAS", 0.15, 0.88), ("EUROPE", 0.395, 0.88),
    ("AFRICA", 0.49, 0.88), ("MIDDLE EAST", 0.58, 0.88),
    ("ASIA", 0.76, 0.88), ("OCEANIA", 0.88, 0.12),
]


# ---------------------------------------------------------------- ADEGAN §6
def scene(d, box, idx):
    """Gambar adegan idx di box (x, y, w, h); semua koordinat fraksi w/h."""
    x, y, w, h = box
    X = lambda f: x + f * w
    Y = lambda f: y + f * h

    def rect(fx0, fy0, fx1, fy1, fill):
        d.rectangle([X(fx0), Y(fy0), X(fx1), Y(fy1)], fill=fill)

    def ell(fx0, fy0, fx1, fy1, fill=None, outline=None, width=1):
        d.ellipse([X(fx0), Y(fy0), X(fx1), Y(fy1)], fill=fill,
                  outline=outline, width=width)

    def poly(pts, fill):
        d.polygon([(X(a), Y(b)) for a, b in pts], fill=fill)

    def line(pts, fill, width=2):
        d.line([(X(a), Y(b)) for a, b in pts], fill=fill, width=width)

    if idx == 1:  # Drones malam
        rect(0, 0, 1, 1, (16, 24, 52))
        for sx, sy in [(0.08, 0.12), (0.22, 0.06), (0.38, 0.16), (0.55, 0.08),
                       (0.68, 0.18), (0.82, 0.06), (0.93, 0.22), (0.30, 0.24)]:
            ell(sx - 0.006, sy - 0.012, sx + 0.006, sy + 0.012, (255, 214, 90))
        ell(0.78, 0.04, 0.92, 0.28, (240, 230, 200))
        ell(0.82, 0.02, 0.96, 0.26, (16, 24, 52))
        for dx in (0.12, 0.34, 0.56, 0.78):
            rect(dx, 0.30, dx + 0.09, 0.36, (200, 200, 210))
            line([(dx + 0.045, 0.30), (dx + 0.045, 0.24)], (200, 200, 210), 2)
        rect(0, 0.78, 1, 1, (40, 44, 60))
        line([(0, 0.78), (1, 0.78)], (176, 30, 36), 3)
        for bx in (0.05, 0.25, 0.45, 0.65, 0.85):
            for wy in (0.82, 0.90):
                rect(bx, wy, bx + 0.03, wy + 0.04, (255, 200, 80))
    elif idx == 2:  # COP31
        rect(0, 0, 1, 0.55, (122, 62, 140))
        rect(0, 0.55, 1, 1, (214, 122, 31))
        ell(0.40, 0.06, 0.60, 0.38, (255, 214, 90))
        for ang in range(5):
            sx = 0.5 + (ang - 2) * 0.16
            line([(sx, 0.02), (sx, 0.10)], (255, 214, 90), 3)
        rect(0.15, 0.62, 0.85, 0.78, (90, 50, 30))
        for px in (0.20, 0.35, 0.50, 0.65, 0.80):
            ell(px - 0.035, 0.42, px + 0.035, 0.56, (240, 200, 170))
            poly([(px - 0.05, 0.62), (px + 0.05, 0.62),
                  (px + 0.035, 0.56), (px - 0.035, 0.56)], (30, 30, 40))
    elif idx == 3:  # Radar Bahrain
        rect(0, 0, 1, 0.72, (18, 20, 38))
        for sx, sy in [(0.1, 0.1), (0.3, 0.06), (0.5, 0.14), (0.7, 0.07),
                       (0.9, 0.12), (0.2, 0.2), (0.85, 0.24)]:
            ell(sx - 0.005, sy - 0.01, sx + 0.005, sy + 0.01, LIGHT)
        for rx in (0.25, 0.60):
            line([(rx, 0.62), (rx, 0.30)], (180, 180, 180), 3)
            ell(rx - 0.11, 0.14, rx + 0.11, 0.36, outline=(255, 214, 90), width=2)
        poly([(0.60, 0.62), (0.72, 0.62), (0.66, 0.38)], (230, 90, 30))
        poly([(0.63, 0.62), (0.69, 0.62), (0.66, 0.46)], (255, 190, 60))
        rect(0, 0.72, 1, 1, (20, 60, 90))
        poly([(0.08, 0.86), (0.20, 0.86), (0.14, 0.80)], LIGHT)
        line([(0.35, 0.88), (0.55, 0.88), (0.75, 0.88)], LIGHT, 2)
    elif idx == 4:  # Hong Kong vote
        rect(0, 0, 1, 1, (232, 222, 200))
        rect(0.30, 0.30, 0.70, 0.92, (176, 30, 36))
        rect(0.42, 0.18, 0.58, 0.34, LIGHT)
        line([(0.45, 0.24), (0.55, 0.24)], (176, 30, 36), 2)
        line([(0.45, 0.29), (0.55, 0.29)], (176, 30, 36), 2)
        d.text((X(0.5), Y(0.62)), "VOTE", font=F(SANS_B, 11), fill=LIGHT,
               anchor="mm")
    elif idx == 5:  # F1
        rect(0, 0, 1, 1, (30, 60, 110))
        for cx in (0, 1):
            for k in range(4):
                rect(cx * 0.14 + (k % 2) * 0.035, 0.04 + (k // 2) * 0.05,
                     cx * 0.14 + (k % 2) * 0.035 + 0.035,
                     0.04 + (k // 2) * 0.05 + 0.05,
                     LIGHT if (k % 2 == 0) == (cx == 0) else INK)
        rect(0, 0.55, 1, 0.95, (60, 60, 60))
        line([(0, 0.75), (1, 0.75)], LIGHT, 2)
        poly([(0.30, 0.62), (0.70, 0.62), (0.66, 0.78), (0.34, 0.78)],
             (220, 30, 40))
        ell(0.36, 0.74, 0.44, 0.86, INK)
        ell(0.58, 0.74, 0.66, 0.86, INK)
        rect(0.82, 0.08, 0.94, 0.26, LIGHT)
        d.text((X(0.88), Y(0.17)), "1", font=F(SANS_B, 12), fill=INK, anchor="mm")
    elif idx == 6:  # Cricket
        rect(0, 0, 1, 1, (90, 160, 80))
        ell(0.10, 0.15, 0.90, 0.90, (214, 190, 140))
        rect(0.42, 0.20, 0.58, 0.85, (150, 110, 70))
        for sx in (0.46, 0.50, 0.54):
            line([(sx, 0.28), (sx, 0.44)], (255, 220, 120), 3)
        ell(0.68, 0.60, 0.74, 0.70, LIGHT)
    elif idx == 7:  # Boat
        rect(0, 0, 1, 0.45, (255, 200, 120))
        rect(0, 0.45, 1, 1, (30, 90, 140))
        line([(0.50, 0.10), (0.50, 0.55)], (120, 70, 40), 3)
        poly([(0.52, 0.14), (0.52, 0.50), (0.72, 0.50)], LIGHT)
        poly([(0.32, 0.55), (0.68, 0.55), (0.60, 0.68), (0.40, 0.68)],
             (120, 70, 40))
        poly([(0.78, 0.62), (0.92, 0.62), (0.88, 0.70), (0.82, 0.70)],
             (120, 70, 40))
        d.arc([X(0.05), Y(0.78), X(0.25), Y(0.95)], 0, 180, fill=LIGHT, width=2)
        d.arc([X(0.60), Y(0.82), X(0.80), Y(0.98)], 0, 180, fill=LIGHT, width=2)
    elif idx == 8:  # Power pylon
        rect(0, 0, 1, 1, (200, 220, 240))
        poly([(0.46, 0.95), (0.54, 0.95), (0.52, 0.15), (0.48, 0.15)],
             (90, 70, 50))
        line([(0.30, 0.25), (0.70, 0.25)], INK, 2)
        line([(0.35, 0.40), (0.65, 0.40)], INK, 2)
        line([(0.20, 0.18), (0.80, 0.18)], INK, 2)
        line([(0.82, 0.95), (0.82, 0.35)], (150, 150, 150), 3)
        ell(0.78, 0.28, 0.86, 0.40, (255, 220, 100))
    elif idx == 9:  # Factory fire
        rect(0, 0, 1, 0.45, (240, 200, 120))
        rect(0, 0.45, 1, 1, (90, 90, 95))
        rect(0.15, 0.45, 0.65, 0.90, (140, 60, 50))
        rect(0.70, 0.20, 0.80, 0.90, (120, 120, 125))
        ell(0.68, 0.06, 0.78, 0.18, (180, 180, 180))
        ell(0.74, 0.12, 0.86, 0.24, (160, 160, 160))
        poly([(0.30, 0.45), (0.50, 0.45), (0.40, 0.18)], (230, 90, 30))
        poly([(0.36, 0.45), (0.46, 0.45), (0.41, 0.30)], (255, 190, 60))
    elif idx == 10:  # FBI
        rect(0, 0, 1, 1, (210, 225, 235))
        rect(0.12, 0.18, 0.55, 0.88, LIGHT)
        for i, ly in enumerate((0.32, 0.46, 0.60)):
            line([(0.20, ly), (0.48, ly)], (43, 94, 167), 3)
        ell(0.58, 0.22, 0.86, 0.62, outline=INK, width=3)
        line([(0.82, 0.58), (0.96, 0.78)], INK, 4)
    elif idx == 11:  # Flights
        rect(0, 0, 1, 0.75, (170, 200, 235))
        rect(0, 0.75, 1, 1, (90, 110, 90))
        for cx, cy, cw in [(0.12, 0.14, 0.20), (0.55, 0.08, 0.16), (0.80, 0.22, 0.14)]:
            ell(cx, cy, cx + cw, cy + 0.12, LIGHT)
        poly([(0.30, 0.48), (0.68, 0.48), (0.72, 0.54), (0.32, 0.54)], LIGHT)
        poly([(0.46, 0.48), (0.52, 0.30), (0.56, 0.48)], LIGHT)
        poly([(0.78, 0.30), (0.90, 0.30), (0.92, 0.34), (0.80, 0.34)], LIGHT)
    elif idx == 12:  # Poison
        rect(0, 0, 1, 1, (240, 230, 210))
        rect(0.42, 0.30, 0.58, 0.85, LIGHT)
        line([(0.42, 0.45), (0.58, 0.45)], (176, 30, 36), 3)
        line([(0.42, 0.60), (0.58, 0.60)], (176, 30, 36), 3)
        rect(0.47, 0.20, 0.53, 0.30, LIGHT)
        poly([(0.10, 0.95), (0.28, 0.95), (0.19, 0.62)], (40, 120, 60))
        poly([(0.72, 0.95), (0.90, 0.95), (0.81, 0.62)], (60, 140, 80))
    elif idx == 13:  # Hospital
        rect(0, 0, 1, 1, (200, 220, 235))
        rect(0.10, 0.62, 0.80, 0.82, LIGHT)
        rect(0.10, 0.62, 0.80, 0.72, (40, 120, 60))
        line([(0.10, 0.72), (0.80, 0.72)], (255, 200, 60), 2)
        ell(0.14, 0.48, 0.26, 0.64, (240, 200, 170))
        line([(0.86, 0.15), (0.86, 0.85)], (150, 150, 150), 3)
        rect(0.80, 0.22, 0.92, 0.42, LIGHT)
        d.rectangle([X(0.80), Y(0.22), X(0.92), Y(0.42)],
                    outline=(176, 30, 36), width=2)
        line([(0.86, 0.26), (0.86, 0.38)], (176, 30, 36), 2)
        line([(0.81, 0.32), (0.91, 0.32)], (176, 30, 36), 2)
    elif idx == 35:  # Sparta II
        rect(0, 0, 1, 0.55, (200, 220, 235))
        rect(0, 0.55, 1, 1, (30, 90, 140))
        poly([(0.10, 0.55), (0.75, 0.55), (0.68, 0.72), (0.16, 0.72)],
             (40, 40, 50))
        rect(0.55, 0.32, 0.62, 0.55, (40, 40, 50))
        poly([(0.38, 0.55), (0.52, 0.55), (0.45, 0.32)], (230, 90, 30))
        poly([(0.42, 0.55), (0.49, 0.55), (0.455, 0.42)], (255, 190, 60))
        ell(0.60, 0.18, 0.70, 0.30, (180, 180, 180))
        ell(0.66, 0.24, 0.78, 0.36, (160, 160, 160))
        poly([(0.78, 0.78), (0.92, 0.78), (0.88, 0.86), (0.82, 0.86)], LIGHT)
        d.arc([X(0.05), Y(0.80), X(0.25), Y(0.96)], 0, 180, fill=LIGHT, width=2)


# ---------------------------------------------------------------- KARTU §4
def kicker_bar(d, x, y, w, label, status):
    """Bar kicker merah 16px (hanya lead): label kiri + pil status kanan."""
    d.rectangle([x, y, x + w, y + 16], fill=RED)
    d.text((x + 6, y + 3), label, font=F(SANS_B, 9), fill=LIGHT)
    pil = F(SANS_B, 8)
    tw = text_w(d, status, pil)
    px1, py1 = x + w - 6 - tw - 12, y + 2
    px2, py2 = x + w - 6, y + 14
    d.rounded_rectangle([px1, py1, px2, py2], radius=6, fill=NAVY)
    d.text((px1 + 6, y + 3), status, font=pil, fill=LIGHT)


def draw_map(d, mx, my, mw, mh):
    """Peta 330x216: header navy 16px + daratan titik + pin + label."""
    d.rectangle([mx, my, mx + mw, my + mh], fill=(214, 228, 235))
    d.rectangle([mx, my, mx + mw, my + 16], fill=NAVY)
    d.text((mx + 6, my + 3), "WHERE IT HAPPENED — pins match story numbers",
           font=F(SANS_B, 9), fill=LIGHT)
    ax, ay, aw, ah = mx, my + 16, mw, mh - 16  # area daratan/pin
    cw, ch = aw / 44.0, ah / 11.0
    for r, spans in enumerate(LAND):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = ax + (c + 0.5) * cw
                cy = ay + (r + 0.5) * ch
                d.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=(70, 100, 70))
    for num, fx, fy in PINS:
        px, py = ax + fx * aw, ay + fy * ah
        r = 10 if num in (9, 10, 12, 13) else 11
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=LIGHT, width=1)
        d.text((px, py), str(num), font=F(SANS_B, 10), fill=LIGHT, anchor="mm")
    lab = F(SANS_B, 6)
    for name, fx, fy in MAP_LABELS:
        d.text((ax + fx * aw, ay + fy * ah), name, font=lab, fill=NAVY,
               anchor="mm")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Top bar (0, 24): navy; kiri nama koran, kanan hitungan R7-FIX.
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.text((10, 5), "THE WORLD IN ONE DAY", font=F(SANS_B, 12), fill=LIGHT)
    d.text((1014, 6), TOP_RIGHT, font=F(SANS_B, 11), fill=LIGHT, anchor="ra")

    # --- Masthead (24, 88): 64px SERIF_B satu baris, TANPA kotak merah.
    # "Sunday 22 November 2026" di (10, 28), lebar terukur 963px -> 10..973.
    d.text((10, 28), "Sunday 22 November 2026", font=F(SERIF_B, 64),
           fill=NAVY)
    d.text((10, 98), DECK, font=F(SERIF, 12), fill=RED)

    # --- NUMBERS (112, 62): header y114 + 6 kolom satu baris.
    d.text((10, 114), "THE DAY IN NUMBERS", font=F(SANS_B, 10), fill=NAVY)
    for i, (num, cap) in enumerate(NUMBERS):
        cx = 10 + i * 167
        d.text((cx, 126), num, font=F(SERIF_B, 26), fill=RED)
        # Caption maks 2 baris (y154, lh 10) — "drones fired at Ukraine
        # overnight" paling panjang, tetap muat sebelum blok berakhir (174).
        draw_lines(d, cx, 154, wrap(d, cap, F(SANS, 9), 165)[:2],
                   F(SANS, 9), GREY, 10)

    # --- Region bar (174, 20): "REGIONS:" + 7 chip warna.
    d.text((10, 177), "REGIONS:", font=F(SANS_B, 10), fill=NAVY)
    rx = 10 + text_w(d, "REGIONS: ", F(SANS_B, 10)) + 6
    for name, count in REGIONS:
        label = "%s %d" % (name, count)
        fnt = F(SANS_B, 9)
        tw = text_w(d, label, fnt)
        d.rounded_rectangle([rx, 175, rx + tw + 12, 193], radius=4,
                            fill=REGION_COLORS[name])
        d.text((rx + 6, 177), label, font=fnt, fill=LIGHT)
        rx += tw + 12 + 5

    # --- UTC strip (194, 16).
    ux = 10 + text_w(d, "THE DAY IN UTC  ", F(SANS_B, 9)) + 4
    d.text((10, 196), "THE DAY IN UTC", font=F(SANS_B, 9), fill=NAVY)
    parts = ["%s %s" % (t, s) for t, s in UTC_ITEMS]
    d.text((ux, 196), " · ".join(parts), font=F(SANS, 9), fill=INK)

    # --- LEADS (210, 200): 3 kartu 330x200.
    lead_xs = [10, 346, 682]
    for (num, region, topic, head, body, status, src), lx in zip(LEADS, lead_xs):
        ly, lw, lh = 210, 330, 200
        d.rectangle([lx, ly, lx + lw, ly + lh], fill=CREAM, outline=FRAME)
        kicker_bar(d, lx, ly, lw, KICKERS[num], status)
        scene(d, (lx + 4, ly + 16, lw - 8, 92), num)
        # Anggaran dalam kartu (200): 16 kicker + 92 adegan + 1 celah +
        # 12 baris region (huruf kapital, tanpa descender) + headline 2x17 +
        # isi 3x11 + 11 sumber = 199. Adegan TETAP 92px (min 88px).
        cy = ly + 16 + 92 + 1
        d.text((lx + 6, cy), "%d %s · %s" % (num, region, topic),
               font=F(SANS_B, 9), fill=RED)
        cy += 12
        hf = F(SERIF_B, 15)
        hlines = wrap(d, head, hf, lw - 12)
        if len(hlines) > 2:  # headline 15 -> 14px bila perlu
            hf = F(SERIF_B, 14)
            hlines = wrap(d, head, hf, lw - 12)[:2]
        cy = draw_lines(d, lx + 6, cy, hlines[:2], hf, INK, 17)
        bf = F(SANS, 10)
        blines = wrap(d, body, bf, lw - 12)
        if len(blines) > 3:
            bf = F(SANS, 9)
            blines = wrap(d, body, bf, lw - 12)[:3]
        cy = draw_lines(d, lx + 6, cy, blines[:3], bf, BODY, 11)
        d.text((lx + 6, ly + lh - 11), "Source: %s" % src,
               font=F(SANS, 8), fill=GREY)


    # --- TEN header (410, 18) + TEN grid (428, 254): 2x5 kartu 196x124.
    d.rectangle([10, 410, 1014, 428], fill=NAVY)
    d.text((14, 413), "THE DAY IN TEN", font=F(SANS_B, 11), fill=LIGHT)
    for k, (num, region, head, body, status, src) in enumerate(TEN):
        tx = 10 + (k % 5) * 202
        ty = 428 + (k // 5) * 130
        tw, th = 196, 124
        d.rectangle([tx, ty, tx + tw, ty + th], fill=CREAM, outline=FRAME)
        d.rectangle([tx, ty, tx + tw, ty + 3], fill=RED)  # garis merah 3px
        scene(d, (tx + 3, ty + 3, tw - 6, 50), num)
        # Anggaran dalam kartu (124): 3 garis + 50 adegan + 1 celah +
        # 11 label (kapital) + headline 2x13 + isi 2x10 + 11 status = 122.
        cy = ty + 3 + 50 + 1
        d.text((tx + 5, cy), "%d %s" % (num, region), font=F(SANS_B, 8),
               fill=RED)
        cy += 11
        hf = F(SERIF_B, 11)
        hlines = wrap(d, head, hf, tw - 10)
        if len(hlines) > 2:  # headline 11 -> 10px bila perlu
            hf = F(SERIF_B, 10)
            hlines = wrap(d, head, hf, tw - 10)[:2]
        cy = draw_lines(d, tx + 5, cy, hlines[:2], hf, INK, 13)
        bf = F(SANS, 9)
        blines = wrap(d, body, bf, tw - 10)[:2]
        cy = draw_lines(d, tx + 5, cy, blines, bf, BODY, 10)
        d.text((tx + 5, ty + th - 11), "%s · %s" % (status, src),
               font=F(SANS, 8), fill=GREY)

    # --- Kartu 35 (682, 54): strip full-width, HANYA headline + status.
    # ISI KOSONG — jangan fabrikasi isi apa pun.
    d.rectangle([10, 682, 1014, 736], fill=CREAM, outline=FRAME)
    scene(d, (13, 685, 90, 48), 35)
    d.text((110, 686), "SHIP ABLAZE", font=F(SANS_B, 9), fill=RED)
    d.text((110, 698), CARD35[2], font=F(SERIF_B, 13), fill=INK)
    d.text((110, 720), "%s · %s" % (CARD35[3], CARD35[4]),
           font=F(SANS, 8), fill=GREY)

    # --- Bawah (736, 216): peta kiri + ALSO kanan.
    draw_map(d, 10, 736, 330, 216)
    ax, ay, aw = 346, 736, 666
    d.rectangle([ax, ay, ax + aw, ay + 16], fill=NAVY)
    d.text((ax + 6, ay + 2), "ALSO ON SUNDAY 22 NOVEMBER — 24 MORE STORIES",
           font=F(SANS_B, 11), fill=LIGHT)
    col_w = aw // 2  # 333
    for i, (num, region, head, status, src) in enumerate(ALSO):
        col, row = i // 12, i % 12
        rx0 = ax + col * col_w
        ry = ay + 16 + row * 16
        nf = F(SANS_B, 11)
        ntxt = str(num)
        d.text((rx0 + 4, ry + 2), ntxt, font=nf, fill=RED)
        tx0 = rx0 + 4 + text_w(d, ntxt, nf) + 5
        # Ruang teks = tepi kanan kolom dikurangi awal teks (tanpa margin
        # kanan tambahan — ambang ini setara avail R6 ~308: baris 12px
        # yang muat berakhir >=3px sebelum tepi kolom, terukur dari tinta
        # hasil render; yang tidak muat turun ke 11px, lantai 11px).
        # (Rumus lama "rx0 + col_w - 4 - (tx0 - rx0)" SALAH: menambah rx0
        # sehingga avail 651/984 dan loop shrink tidak pernah jalan —
        # #18/#19 meluber ke kolom 2, #34 terpotong di tepi gambar.
        # Koordinator perbaiki 23 Nov ~13:45 WIB; margin 4px dihapus
        # ~13:50 WIB karena memberi 6 baris 11px, di atas batas spec
        # maks 3 baris — ambang tepi kolom memberi tepat 3 baris 11px.)
        avail = (rx0 + col_w) - tx0
        full = "%s — %s" % (head, status)
        if src:
            full += " (%s)" % src
        size = 12
        # Toleransi 1px: lebar advance dibulatkan sub-pixel — #24 lebih
        # 0,06px dari avail tapi tintanya berakhir 3px di dalam tepi
        # kolom (676 vs 679), jadi 12px benar. Tanpa toleransi, #24
        # turun ke 11px tanpa manfaat visual apa pun (4 baris 11px,
        # di atas batas spec maks 3). Dengan toleransi: tepat 3 baris
        # 11px (#18, #19, #34) — sama seperti R6.
        while size > 11 and text_w(d, full, F(SANS, size)) > avail + 1:
            size -= 1  # shrink-to-fit, lantai 11px — JANGAN di bawah 11px
        d.text((tx0, ry + 2), full, font=F(SANS, size), fill=INK)

    # --- Legend (952, 9).
    d.text((10, 952), LEGEND, font=F(SANS, 8), fill=GREY)

    # --- DATE CHECK (961, 34): kotak berbingkai RED, teks JANGAN diubah.
    d.rectangle([10, 961, 1014, 995], outline=RED, width=1)
    dcf = F(SANS, 9)
    draw_lines(d, 14, 964, wrap(d, DATE_CHECK, dcf, 996), dcf, INK, 11)

    # --- Footer (995, 17): maks 2 baris, lh 8 supaya baris ke-2
    # berakhir 1011, sebelum bottom strip (1012).
    ff = F(SANS, 8)
    draw_lines(d, 10, 995, wrap(d, FOOTER, ff, 1004)[:2], ff, GREY, 8)

    # --- Bottom strip (1012, 12): bar navy penuh, kosong.
    d.rectangle([0, 1012, W, H], fill=NAVY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out)
    return out


if __name__ == "__main__":
    print(build())
