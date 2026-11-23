#!/usr/bin/env python3
"""R7 news-image-20261122 — render entry.png 1024x1024.

Struktur R7: 3 lead berdampingan + adegan lebar di atas, masthead 58px,
peta 216px + pin bernomor, ALSO 2 kolom, red restraint (kicker hanya lead).
Python + PIL saja, tanpa dependensi / network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (20, 20, 20)
NAVY = (27, 42, 74)
RED = (176, 30, 36)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
CREAM = (250, 246, 236)
BODY = (60, 60, 60)
FRAME = (200, 190, 170)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

REGION_COLORS = {
    "EUROPE": (14, 107, 122),
    "MIDDLE EAST": (176, 30, 36),
    "ASIA-PACIFIC": (217, 122, 31),
    "AMERICAS": (43, 94, 167),
    "AFRICA": (61, 139, 64),
    "OCEANIA": (122, 79, 163),
    "WORLD": (51, 51, 51),
}


def F(name, size):
    """Font DejaVu dari FONT_DIR, fallback load_default."""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


def wrap(d, text, font, max_w):
    """Bungkus teks ke beberapa baris agar muat max_w (per kata)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, font, fill, lh):
    """Gambar baris-baris teks, kembalikan y setelah baris terakhir."""
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- data
# LEADS (3): (nomor, region, topik, kicker, headline, isi, status, sumber)
LEADS = [
    (1, "EUROPE", "WAR", "186 DRONES OVERNIGHT",
     "Russia fires 186 drones at Ukraine overnight; 161 downed",
     "Air defences down or jam 161 of 186 strike drones fired from "
     "eight directions; a five-storey block in Dymer is destroyed, "
     "14 may be trapped.",
     "CONFIRMED", "Ukrainian Air Force, Reuters"),
    (2, "WORLD", "CLIMATE", "COP31: FINAL TEXT",
     "COP31's final text lands at dawn — with no mention of fossil fuels",
     "The ten-page package drops the $120bn adaptation target, keeps a "
     "35% clean-electricity goal for 2035, and admits the world will "
     "overshoot 1.5C.",
     "ONGOING", "BBC, Reuters, The Guardian"),
    (3, "MIDDLE EAST", "GULF", "CLAIM VS DENIAL",
     "Iran claims strikes on US bases in Bahrain; two radars hit",
     "Tehran says it hit two Patriot radars at Al-Riffa and Awali Sakir. "
     "Bahrain says its defences intercepted the attacks; a facility "
     "burned, no casualties.",
     "CLAIM", "Al Jazeera, Reuters, IRGC statement"),
]

# TEN (10): (nomor, region, headline, isi, status, sumber)
TEN = [
    (4, "ASIA-PACIFIC", "Hong Kong elects its Election Committee",
     "856 candidates, 723 seats; 93.55% turnout.",
     "CONFIRMED", "SCMP"),
    (5, "AMERICAS", "Verstappen takes the Las Vegas GP",
     "0.639s clear of Norris; 75th win.",
     "CONFIRMED", "Reuters, F1"),
    (6, "OCEANIA", "India declare 720/9 — a record in NZ",
     "Rahul 136, Pant 128, Gill 98; record NZ total.",
     "CONFIRMED", "Reuters, AP"),
    (7, "AFRICA", "Bayelsa boat toll rises to 26",
     "Mourners' boat capsized Friday; recovery goes on.",
     "CONFIRMED", "RIA, Vanguard"),
    (8, "MIDDLE EAST", "Iran starts rationing electricity",
     "Two-hour daily cuts begin as gas output falls.",
     "CONFIRMED", "Tavani, RFE/RL"),
    (9, "ASIA-PACIFIC", "Candy-factory fire in Serang: 3 dead, 36 missing",
     "Benten plant blaze; search goes on.",
     "CONFIRMED", "Detiknews"),
    (10, "AMERICAS", "FBI probes hack of its crime database",
     "Washington pauses gun checks; breach assessed.",
     "REPORTED", "AP"),
    (11, "EUROPE", "Belgian controllers join strike",
     "Most flights grounded 07:00-21:00.",
     "CONFIRMED", "Reuters"),
    (12, "ASIA-PACIFIC", "Toxic-liquor toll in Manipur climbs to 19",
     "600 in hospital, six held; toll up from 11.",
     "CONFIRMED", "Xinhua"),
    (13, "AMERICAS", "Bolsonaro in intensive care",
     "Bowel obstruction, stable, breathing on his own.",
     "CONFIRMED", "Al Jazeera, Reuters"),
]

# Kartu 35 (strip): (nomor, region, label, headline, status, sumber)
# TIDAK ADA isi — R6 juga tanpa isi (hanya headline + status/sumber).
CARD35 = (35, "EUROPE", "SHIP ABLAZE",
          "Russian cargo ship Sparta II still burning",
          "CONFIRMED", "Reuters")

# ALSO (24 tampil, urutan nomor naik): (nomor, region, headline, status, sumber)
# Sumber kosong ("") berarti tanpa kurung. Nomor 15, 30, 32, 37, 38, 43,
# 44, 45 dibuang; nomor 35 jadi kartu strip, bukan di ALSO.
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

# NUMBERS (6, satu baris): (angka, caption)
NUMBERS = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed or jammed"),
    ("35%", "clean-electricity goal for 2035"),
    ("$120bn", "adaptation target dropped"),
    ("720/9", "India's record Test total in NZ"),
    ("93.55%", "Hong Kong turnout by 14:00"),
]

# REGIONS (7 chip, urutan ini): (region, jumlah)
REGIONS = [
    ("EUROPE", 9), ("MIDDLE EAST", 4), ("ASIA-PACIFIC", 7),
    ("AMERICAS", 5), ("AFRICA", 8), ("OCEANIA", 2), ("WORLD", 3),
]

# UTC (6 item, urutan ini): (jam, peristiwa)
UTC_ITEMS = [
    ("01:00", "HK polls open"),
    ("03:00", "COP31 objections close"),
    ("03:46", "Trump weighs nuclear talks with Putin, Xi"),
    ("05:11", "Hamas seeks talks"),
    ("05:30", "Verstappen wins Las Vegas GP"),
    ("06:00", "COP31 approval due"),
]

DATE_CHECK = (
    "DATE CHECK — READ THIS FIRST. Wires read to 07:00 UTC, Sunday "
    "22 November 2026. Every story here happened or was first reported "
    "on 22 November 2026 (UTC). Left out on purpose: Russia's 400-drone "
    "barrage (19-20 Nov) — tonight's barrage was 186 drones, not 400; "
    "the Peru quake (Fri 20 Nov, USGS 6.7) — only the toll update is "
    "today's news; 'El Chapo Isidro' arrest (Sat 21 Nov); the Shenzhen "
    "summit (19 Nov); Poland: two Russian missiles landed (Fri 20 Nov)."
)

LEGEND = (
    "HOW TO READ THE TAGS — CONFIRMED 2+ outlets · OFFICIAL on the "
    "record · REPORTED one outlet or witnesses · CLAIM one side's claim, "
    "contested · PENDING not settled yet · ONGOING still developing as "
    "we print."
)

FOOTER = (
    "Sources: Reuters · AP · AFP · BBC · Al Jazeera · The Guardian · "
    "SCMP · dpa · Xinhua · Kyiv Independent · IRGC statement · Bahrain "
    "MoI · HK Govt · F1 · Cricbuzz · Vatican News — Scenes are drawn "
    "illustrations of reported events, not photographs. "
    "THE WORLD IN ONE DAY · 22 NOV 2026"
)

# PETA — daratan: grid 44 kolom x 11 baris, tiap baris daftar (c0, c1)
LAND = [
    [(5, 12), (16, 20)],
    [(3, 13), (15, 22), (30, 33)],
    [(2, 14), (16, 24), (28, 38)],
    [(4, 13), (17, 25), (27, 40)],
    [(6, 12), (18, 26), (28, 38), (40, 42)],
    [(8, 13), (19, 27), (30, 36)],
    [(10, 14), (20, 26), (31, 34)],
    [(12, 16), (22, 26)],
    [(24, 27)],
    [(38, 41)],
    [(39, 42)],
]

# PETA — pin bernomor: (nomor, fx, fy) fraksi lebar/tinggi area peta
PINS = [
    (1, 0.494, 0.085), (2, 0.539, 0.341), (3, 0.607, 0.427),
    (4, 0.809, 0.341), (5, 0.135, 0.341), (6, 0.899, 0.768),
    (7, 0.472, 0.512), (8, 0.674, 0.256), (9, 0.719, 0.530),
    (10, 0.216, 0.341), (11, 0.404, 0.256), (12, 0.742, 0.230),
    (13, 0.270, 0.548),
]

# Label region peta: (teks, fx, fy)
MAP_LABELS = [
    ("AMERICAS", 0.15, 0.88), ("EUROPE", 0.395, 0.88),
    ("AFRICA", 0.49, 0.88), ("MIDDLE EAST", 0.58, 0.88),
    ("ASIA", 0.76, 0.88), ("OCEANIA", 0.88, 0.12),
]

# ---------------------------------------------------------------- adegan
def scene(d, box, idx):
    """Gambar satu adegan di dalam box (x0, y0, x1, y1), semua koordinat
    sebagai fraksi lebar (w) dan tinggi (h) kotak — proporsional."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    def X(f):
        return x0 + f * w

    def Y(f):
        return y0 + f * h

    def R(fx0, fy0, fx1, fy1, fill):
        d.rectangle([X(fx0), Y(fy0), X(fx1), Y(fy1)], fill=fill)

    def E(fx0, fy0, fx1, fy1, fill=None, outline=None, width=1):
        d.ellipse([X(fx0), Y(fy0), X(fx1), Y(fy1)],
                  fill=fill, outline=outline, width=width)

    if idx == 1:  # Drones malam
        R(0, 0, 1, 1, (16, 24, 52))
        for sx, sy in [(0.08, 0.12), (0.22, 0.08), (0.35, 0.18),
                       (0.55, 0.10), (0.68, 0.16), (0.85, 0.06),
                       (0.15, 0.30), (0.45, 0.26), (0.78, 0.28)]:
            d.ellipse([X(sx) - 1, Y(sy) - 1, X(sx) + 1, Y(sy) + 1],
                      fill=(255, 214, 90))
        E(0.78, 0.06, 0.92, 0.30, fill=(240, 230, 200))
        E(0.82, 0.04, 0.94, 0.26, fill=(16, 24, 52))
        for dx in (0.12, 0.34, 0.56, 0.76):
            d.rectangle([X(dx), Y(0.30), X(dx) + 0.055 * w, Y(0.30) + 4],
                        fill=(200, 200, 210))
            d.line([X(dx) + 0.027 * w, Y(0.30) + 4,
                    X(dx) + 0.027 * w, Y(0.30) + 10], fill=(200, 200, 210))
        R(0, 0.72, 1, 1, (40, 44, 60))
        d.line([X(0), Y(0.72), X(1), Y(0.72)], fill=(176, 30, 36), width=3)
        for bx in (0.05, 0.22, 0.40, 0.58, 0.76, 0.90):
            for wy in (0.78, 0.88):
                d.rectangle([X(bx), Y(wy), X(bx) + 0.02 * w, Y(wy) + 0.04 * h],
                            fill=(255, 200, 80))
    elif idx == 2:  # COP31
        R(0, 0, 1, 0.55, (122, 62, 140))
        R(0, 0.55, 1, 1, (214, 122, 31))
        E(0.42, 0.08, 0.58, 0.42, fill=(255, 214, 90))
        for ang in range(0, 360, 72):
            import math
            a = math.radians(ang)
            d.line([X(0.5) + 0.11 * w * math.cos(a),
                    Y(0.25) + 0.11 * h * math.sin(a),
                    X(0.5) + 0.16 * w * math.cos(a),
                    Y(0.25) + 0.16 * h * math.sin(a)],
                   fill=(255, 214, 90), width=3)
        R(0.18, 0.62, 0.82, 0.72, (90, 50, 30))
        for px in (0.22, 0.36, 0.50, 0.64, 0.78):
            E(px - 0.03, 0.42, px + 0.03, 0.58, fill=(240, 200, 170))
            d.rectangle([X(px) - 0.035 * w, Y(0.58),
                         X(px) + 0.035 * w, Y(0.78)], fill=(30, 30, 40))
    elif idx == 3:  # Radar Bahrain
        R(0, 0, 1, 1, (18, 20, 38))
        for sx, sy in [(0.10, 0.10), (0.30, 0.06), (0.55, 0.12),
                       (0.75, 0.08), (0.90, 0.15), (0.20, 0.22)]:
            d.ellipse([X(sx) - 1, Y(sy) - 1, X(sx) + 1, Y(sy) + 1],
                      fill=(255, 255, 255))
        for rx in (0.28, 0.62):
            d.line([X(rx), Y(0.35), X(rx), Y(0.70)],
                   fill=(180, 180, 180), width=3)
            d.ellipse([X(rx) - 0.09 * w, Y(0.18), X(rx) + 0.09 * w, Y(0.38)],
                      outline=(255, 214, 90), width=2)
        d.polygon([(X(0.72), Y(0.70)), (X(0.80), Y(0.45)), (X(0.88), Y(0.70))],
                  fill=(230, 90, 30))
        d.polygon([(X(0.76), Y(0.70)), (X(0.80), Y(0.55)), (X(0.84), Y(0.70))],
                  fill=(255, 190, 60))
        R(0, 0.72, 1, 1, (20, 60, 90))
        d.rectangle([X(0.08), Y(0.78), X(0.20), Y(0.84)], fill=(255, 255, 255))
        d.line([X(0.14), Y(0.78), X(0.14), Y(0.68)],
               fill=(255, 255, 255), width=2)
    elif idx == 4:  # Hong Kong vote
        R(0, 0, 1, 1, (232, 222, 200))
        d.rectangle([X(0.32), Y(0.30), X(0.68), Y(0.85)], fill=(176, 30, 36))
        d.rectangle([X(0.38), Y(0.12), X(0.62), Y(0.34)], fill=(255, 255, 255))
        d.line([X(0.38), Y(0.30), X(0.62), Y(0.30)], fill=(176, 30, 36), width=2)
        d.text((X(0.50), Y(0.52)), "VOTE", font=F(SANS_B, 11),
               fill=(255, 255, 255), anchor="mm")
    elif idx == 5:  # F1
        R(0, 0, 1, 1, (30, 60, 110))
        for cx in (0.12, 0.30):
            for cy in (0.10, 0.16):
                d.rectangle([X(cx), Y(cy), X(cx) + 0.06 * w, Y(cy) + 0.06 * h],
                            fill=(255, 255, 255))
        R(0, 0.55, 1, 1, (60, 60, 60))
        d.line([X(0), Y(0.68), X(1), Y(0.68)], fill=(255, 255, 255), width=2)
        d.rectangle([X(0.30), Y(0.42), X(0.62), Y(0.58)], fill=(220, 30, 40))
        d.ellipse([X(0.33), Y(0.55), X(0.39), Y(0.66)], fill=(0, 0, 0))
        d.ellipse([X(0.53), Y(0.55), X(0.59), Y(0.66)], fill=(0, 0, 0))
        d.rectangle([X(0.80), Y(0.10), X(0.94), Y(0.30)], fill=(255, 255, 255))
        d.text((X(0.87), Y(0.20)), "1", font=F(SANS_B, 14),
               fill=(20, 20, 20), anchor="mm")
    elif idx == 6:  # Cricket
        R(0, 0, 1, 1, (90, 160, 80))
        E(0.10, 0.15, 0.90, 0.95, fill=(214, 190, 140))
        d.rectangle([X(0.38), Y(0.25), X(0.62), Y(0.90)], fill=(150, 110, 70))
        for sx in (0.46, 0.50, 0.54):
            d.rectangle([X(sx), Y(0.30), X(sx) + 0.012 * w, Y(0.42)],
                        fill=(255, 220, 120))
        d.ellipse([X(0.68), Y(0.60), X(0.72), Y(0.66)], fill=(255, 255, 255))

    elif idx == 7:  # Boat
        R(0, 0, 1, 0.45, (255, 200, 120))
        R(0, 0.45, 1, 1, (30, 90, 140))
        d.line([X(0.32), Y(0.20), X(0.32), Y(0.55)],
               fill=(120, 70, 40), width=3)
        d.polygon([(X(0.32), Y(0.22)), (X(0.32), Y(0.52)),
                   (X(0.52), Y(0.52))], fill=(255, 255, 255))
        d.polygon([(X(0.18), Y(0.55)), (X(0.46), Y(0.55)),
                   (X(0.40), Y(0.66)), (X(0.24), Y(0.66))],
                  fill=(120, 70, 40))
        d.polygon([(X(0.68), Y(0.60)), (X(0.82), Y(0.60)),
                   (X(0.78), Y(0.68)), (X(0.72), Y(0.68))],
                  fill=(120, 70, 40))
        for wy in (0.75, 0.85):
            d.arc([X(0.10), Y(wy), X(0.35), Y(wy) + 0.12],
                  start=180, end=360, fill=(255, 255, 255), width=2)
            d.arc([X(0.60), Y(wy), X(0.85), Y(wy) + 0.12],
                  start=180, end=360, fill=(255, 255, 255), width=2)
    elif idx == 8:  # Power pylon
        R(0, 0, 1, 1, (200, 220, 240))
        d.line([X(0.50), Y(0.15), X(0.38), Y(0.95)], fill=(90, 70, 50), width=4)
        d.line([X(0.50), Y(0.15), X(0.62), Y(0.95)], fill=(90, 70, 50), width=4)
        d.line([X(0.42), Y(0.55), X(0.58), Y(0.55)], fill=(90, 70, 50), width=3)
        d.line([X(0.30), Y(0.25), X(0.50), Y(0.15)], fill=(0, 0, 0), width=2)
        d.line([X(0.50), Y(0.15), X(0.70), Y(0.25)], fill=(0, 0, 0), width=2)
        d.line([X(0.80), Y(0.30), X(0.80), Y(0.75)],
               fill=(120, 120, 120), width=3)
        E(0.76, 0.22, 0.84, 0.34, fill=(255, 220, 100))
    elif idx == 9:  # Factory fire
        R(0, 0, 1, 0.55, (240, 200, 120))
        R(0, 0.55, 1, 1, (90, 90, 95))
        d.rectangle([X(0.15), Y(0.45), X(0.65), Y(0.90)], fill=(140, 60, 50))
        d.rectangle([X(0.68), Y(0.25), X(0.80), Y(0.90)], fill=(120, 120, 125))
        E(0.62, 0.08, 0.78, 0.24, fill=(180, 180, 180))
        E(0.72, 0.02, 0.88, 0.16, fill=(200, 200, 200))
        d.polygon([(X(0.25), Y(0.55)), (X(0.38), Y(0.25)), (X(0.51), Y(0.55))],
                  fill=(230, 90, 30))
        d.polygon([(X(0.32), Y(0.55)), (X(0.38), Y(0.38)), (X(0.44), Y(0.55))],
                  fill=(255, 190, 60))
    elif idx == 10:  # FBI
        R(0, 0, 1, 1, (210, 225, 235))
        d.rectangle([X(0.15), Y(0.20), X(0.62), Y(0.85)], fill=(255, 255, 255))
        for i, ly in enumerate((0.32, 0.48, 0.64)):
            d.line([X(0.22), Y(ly), X(0.55), Y(ly)],
                   fill=(43, 94, 167), width=3)
        E(0.55, 0.45, 0.88, 0.90, outline=(0, 0, 0), width=3)
        d.line([X(0.82), Y(0.82), X(0.95), Y(0.98)], fill=(0, 0, 0), width=4)
    elif idx == 11:  # Flights
        R(0, 0, 1, 0.75, (170, 200, 235))
        R(0, 0.75, 1, 1, (90, 110, 90))
        for cx, cy in [(0.12, 0.15), (0.55, 0.10), (0.78, 0.22)]:
            E(cx, cy, cx + 0.18, cy + 0.12, fill=(255, 255, 255))
        d.ellipse([X(0.30), Y(0.40), X(0.70), Y(0.55)], fill=(255, 255, 255))
        d.polygon([(X(0.30), Y(0.47)), (X(0.18), Y(0.42)), (X(0.30), Y(0.52))],
                  fill=(255, 255, 255))
        d.ellipse([X(0.72), Y(0.18), X(0.88), Y(0.26)], fill=(255, 255, 255))
    elif idx == 12:  # Poison
        R(0, 0, 1, 1, (240, 230, 210))
        d.rectangle([X(0.38), Y(0.35), X(0.55), Y(0.80)], fill=(255, 255, 255))
        d.rectangle([X(0.44), Y(0.22), X(0.49), Y(0.35)], fill=(255, 255, 255))
        d.line([X(0.38), Y(0.55), X(0.55), Y(0.55)], fill=(176, 30, 36), width=3)
        E(0.10, 0.70, 0.35, 0.95, fill=(40, 120, 60))
        E(0.65, 0.70, 0.90, 0.95, fill=(60, 140, 80))
    elif idx == 13:  # Hospital
        R(0, 0, 1, 1, (200, 220, 235))
        d.line([X(0.80), Y(0.15), X(0.80), Y(0.75)],
               fill=(120, 120, 120), width=3)
        d.rectangle([X(0.74), Y(0.30), X(0.86), Y(0.48)],
                    outline=(176, 30, 36), width=2)
        d.line([X(0.80), Y(0.35), X(0.80), Y(0.43)], fill=(176, 30, 36), width=3)
        d.line([X(0.76), Y(0.39), X(0.84), Y(0.39)], fill=(176, 30, 36), width=3)
        d.rectangle([X(0.12), Y(0.55), X(0.68), Y(0.85)], fill=(255, 255, 255))
        d.rectangle([X(0.12), Y(0.68), X(0.68), Y(0.85)], fill=(40, 120, 60))
        d.line([X(0.12), Y(0.68), X(0.68), Y(0.68)], fill=(255, 200, 60), width=3)
        E(0.16, 0.42, 0.28, 0.58, fill=(240, 200, 170))
    elif idx == 35:  # Sparta II
        R(0, 0, 1, 0.55, (200, 220, 235))
        R(0, 0.55, 1, 1, (30, 90, 140))
        d.rectangle([X(0.12), Y(0.48), X(0.68), Y(0.68)], fill=(40, 40, 50))
        d.rectangle([X(0.55), Y(0.32), X(0.62), Y(0.48)], fill=(40, 40, 50))
        d.polygon([(X(0.25), Y(0.48)), (X(0.35), Y(0.28)), (X(0.45), Y(0.48))],
                  fill=(230, 90, 30))
        d.polygon([(X(0.32), Y(0.48)), (X(0.35), Y(0.36)), (X(0.38), Y(0.48))],
                  fill=(255, 190, 60))
        E(0.48, 0.18, 0.62, 0.32, fill=(180, 180, 180))
        E(0.58, 0.10, 0.72, 0.22, fill=(200, 200, 200))
        d.rectangle([X(0.75), Y(0.72), X(0.90), Y(0.80)], fill=(255, 255, 255))
        d.arc([X(0.10), Y(0.78), X(0.35), Y(0.92)],
              start=180, end=360, fill=(255, 255, 255), width=2)


def kicker_bar(d, x, y, w, label, status):
    """Bar kicker merah 16px penuh lebar kartu lead + pil status navy."""
    d.rectangle([x, y, x + w, y + 16], fill=RED)
    d.text((x + 6, y + 3), label, font=F(SANS_B, 9), fill=WHITE)
    pill = status
    pw = d.textlength(pill, font=F(SANS_B, 8)) + 12
    px = x + w - pw - 5
    d.rounded_rectangle([px, y + 2, px + pw, y + 14], radius=6, fill=NAVY)
    d.text((px + 6, y + 3), pill, font=F(SANS_B, 8), fill=WHITE)

# ---------------------------------------------------------------- peta
def draw_map(d, x, y, w, h):
    """Peta kiri bawah 330x216: latar, header, daratan titik, pin, label."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 235))
    d.rectangle([x, y, x + w, y + 16], fill=NAVY)
    d.text((x + 6, y + 3), "WHERE IT HAPPENED — pins match story numbers",
           font=F(SANS_B, 9), fill=WHITE)
    land_y0, land_h = y + 16, h - 16
    cell_w, cell_h = w / 44.0, land_h / 11.0
    for r, spans in enumerate(LAND):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = x + (c + 0.5) * cell_w
                cy = land_y0 + (r + 0.5) * cell_h
                d.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=(70, 100, 70))
    for label, fx, fy in MAP_LABELS:
        d.text((x + fx * w, y + fy * h), label, font=F(SANS_B, 6),
               fill=NAVY, anchor="mm")
    for num, fx, fy in PINS:
        px, py = x + fx * w, y + fy * h
        r = 10 if num in (9, 10, 12, 13) else 11
        d.ellipse([px - r, py - r, px + r, py + r],
                  fill=RED, outline=WHITE, width=1)
        d.text((px, py), str(num), font=F(SANS_B, 10),
               fill=WHITE, anchor="mm")


# ---------------------------------------------------------------- kartu
def draw_lead(d, x, y, w, h, item):
    """Kartu LEAD 330x200: kicker, adegan 92px, region, headline, isi, sumber."""
    num, region, topic, kicker, headline, body, status, source = item
    d.rectangle([x, y, x + w, y + h], fill=CREAM, outline=FRAME, width=1)
    kicker_bar(d, x + 1, y + 1, w - 2, kicker, status)
    scene(d, (x + 4, y + 17, x + w - 4, y + 109), num)
    d.text((x + 6, y + 111), "%d %s · %s" % (num, region, topic),
           font=F(SANS_B, 9), fill=RED)
    hl_font = F(SERIF_B, 15)
    hl = wrap(d, headline, hl_font, w - 12)
    if len(hl) > 2:
        hl_font = F(SERIF_B, 14)
        hl = wrap(d, headline, hl_font, w - 12)[:2]
    hy = draw_lines(d, x + 6, y + 124, hl[:2], hl_font, INK, 16)
    body_font = F(SANS, 10)
    bl = wrap(d, body, body_font, w - 12)
    if hy + len(bl[:3]) * 10 > y + h - 11:
        body_font = F(SANS, 9)
        bl = wrap(d, body, body_font, w - 12)
    draw_lines(d, x + 6, hy + 1, bl[:3], body_font, BODY, 10)
    d.text((x + 6, y + h - 11), "Source: %s" % source,
           font=F(SANS, 8), fill=GREY)


def draw_ten(d, x, y, w, h, item):
    """Kartu TEN ~196x124: garis merah 3px, adegan 50px, label, headline,
    isi 2 baris, status+sumber."""
    num, region, headline, body, status, source = item
    d.rectangle([x, y, x + w, y + h], fill=CREAM, outline=FRAME, width=1)
    d.rectangle([x, y, x + w, y + 3], fill=RED)
    scene(d, (x + 3, y + 4, x + w - 3, y + 54), num)
    d.text((x + 5, y + 55), "%d %s" % (num, region),
           font=F(SANS_B, 8), fill=RED)
    hl_font = F(SERIF_B, 11)
    hl = wrap(d, headline, hl_font, w - 10)
    if len(hl) > 2:
        hl_font = F(SERIF_B, 10)
        hl = wrap(d, headline, hl_font, w - 10)[:2]
    hy = draw_lines(d, x + 5, y + 67, hl[:2], hl_font, INK, 12)
    bl = wrap(d, body, F(SANS, 9), w - 10)
    draw_lines(d, x + 5, hy, bl[:2], F(SANS, 9), BODY, 10)
    d.text((x + 5, y + h - 11), "%s · %s" % (status, source),
           font=F(SANS, 8), fill=GREY)


def draw_card35(d, x, y, w, h):
    """Kartu 35 strip 1004x54: adegan 90x48 kiri + label + headline."""
    num, region, label, headline, status, source = CARD35
    d.rectangle([x, y, x + w, y + h], fill=CREAM, outline=FRAME, width=1)
    scene(d, (x + 4, y + 3, x + 94, y + 51), num)
    tx = x + 102
    d.text((tx, y + 3), label, font=F(SANS_B, 9), fill=RED)
    d.text((tx, y + 14), headline, font=F(SERIF_B, 13), fill=INK)
    d.text((tx, y + 34), "%s · %s" % (status, source),
           font=F(SANS, 8), fill=GREY)

# ---------------------------------------------------------------- build
def draw_also(d, x, y, w, h):
    """ALSO kanan bawah 666x216: header navy + 24 baris, 2 kolom x 12."""
    d.rectangle([x, y, x + w, y + 16], fill=NAVY)
    d.text((x + 6, y + 2), "ALSO ON SUNDAY 22 NOVEMBER — 24 MORE STORIES",
           font=F(SANS_B, 11), fill=WHITE)
    col_w = (w - 10) // 2
    for i, item in enumerate(ALSO):
        num, region, headline, status, source = item
        col, row = divmod(i, 12)
        cx = x + 6 + col * (col_w + 10)
        cy = y + 16 + row * 16 + 2
        d.text((cx, cy), str(num), font=F(SANS_B, 11), fill=RED)
        num_w = d.textlength(str(num), font=F(SANS_B, 11)) + 5
        text = "%s — %s" % (headline, status)
        if source:
            text += " (%s)" % source
        size = 12
        # Batas lebar: pakai gutter 10px antar kolom (minus 6px celah ke
        # nomor kolom berikut) — bukan col_w saja, supaya 23/24 baris
        # muat 12px (diukur: hanya #34 yang jatuh ke 11px).
        while size > 11 and d.textlength(text, font=F(SANS, size)) > col_w + 10 - num_w - 6:
            size -= 1
        d.text((cx + num_w, cy), text, font=F(SANS, size), fill=INK)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Top bar 0-24
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.text((10, 6), "THE WORLD IN ONE DAY", font=F(SANS_B, 12), fill=WHITE)
    right = "SUNDAY 22 NOVEMBER 2026 · ONE PAGE"
    d.text((W - 10, 7), right, font=F(SANS_B, 11), fill=WHITE, anchor="ra")

    # Masthead 24-112 — 48px (BUKAN 58px: diukur, 58px berakhir x=882,
    # menabrak kotak merah di x=764; 48px berakhir x=732, aman)
    d.text((10, 28), "Sunday 22 November 2026", font=F(SERIF_B, 48), fill=NAVY)
    d.rectangle([764, 30, 1014, 86], fill=RED)
    d.text((889, 38), "38 STORIES / 7 REGIONS", font=F(SANS_B, 15),
           fill=WHITE, anchor="ma")
    d.text((889, 60), "ONE DAY — ONE PICTURE", font=F(SANS_B, 13),
           fill=WHITE, anchor="ma")
    d.text((10, 96),
           "186 drones over Ukraine overnight · COP31's deal names no fossil "
           "fuels · Iran's radar claim meets Bahrain's denial",
           font=F(SERIF, 12), fill=RED)

    # NUMBERS 112-174
    d.text((10, 114), "THE DAY IN NUMBERS", font=F(SANS_B, 10), fill=NAVY)
    for i, (value, caption) in enumerate(NUMBERS):
        cx = 10 + i * 167
        d.text((cx, 130), value, font=F(SERIF_B, 26), fill=RED)
        cap = wrap(d, caption, F(SANS, 9), 160)
        draw_lines(d, cx, 160, cap[:2], F(SANS, 9), GREY, 11)

    # Region bar 174-194
    d.text((10, 178), "REGIONS:", font=F(SANS_B, 10), fill=NAVY)
    rx = 10 + d.textlength("REGIONS:", font=F(SANS_B, 10)) + 8
    for region, count in REGIONS:
        label = "%s %d" % (region, count)
        chip_w = d.textlength(label, font=F(SANS_B, 9)) + 12
        d.rounded_rectangle([rx, 176, rx + chip_w, 192], radius=4,
                            fill=REGION_COLORS[region])
        d.text((rx + 6, 179), label, font=F(SANS_B, 9), fill=WHITE)
        rx += chip_w + 4

    # UTC strip 194-210
    d.text((10, 197), "THE DAY IN UTC", font=F(SANS_B, 9), fill=NAVY)
    ux = 10 + d.textlength("THE DAY IN UTC", font=F(SANS_B, 9)) + 8
    utc_text = " · ".join("%s %s" % (t, e) for t, e in UTC_ITEMS)
    d.text((ux, 197), utc_text, font=F(SANS, 9), fill=INK)

    # LEADS 210-410: 3 kartu 330 lebar, gutter 6px
    lead_x = [10, 346, 682]
    for lx, item in zip(lead_x, LEADS):
        draw_lead(d, lx, 210, 330, 200, item)

    # TEN header 410-428 + grid 428-682
    d.rectangle([10, 410, 1014, 428], fill=NAVY)
    d.text((14, 413), "THE DAY IN TEN", font=F(SANS_B, 11), fill=WHITE)
    for i, item in enumerate(TEN):
        col, row = i % 5, i // 5
        tx = 10 + col * (196 + 6)
        ty = 428 + row * (124 + 6)
        draw_ten(d, tx, ty, 196, 124, item)

    # Kartu 35 strip 682-736
    draw_card35(d, 10, 682, 1004, 54)

    # Bawah 736-952: peta kiri + ALSO kanan — peta 300 (BUKAN 330) agar
    # ALSO 696 lebar: col_w 343, 23/24 baris muat 12px, #34 berakhir
    # x=1015 (di dalam gambar). Tinggi peta tetap 216px.
    draw_map(d, 10, 736, 300, 216)
    draw_also(d, 316, 736, 696, 216)

    # Legend 952-961
    d.text((10, 953), LEGEND, font=F(SANS, 8), fill=GREY)

    # DATE CHECK 961-995: kotak berbingkai RED, isi 2-3 baris
    d.rectangle([10, 961, 1014, 995], outline=RED, width=1)
    dc_lines = wrap(d, DATE_CHECK, F(SANS, 9), 1004 - 16)
    draw_lines(d, 18, 963, dc_lines[:3], F(SANS, 9), INK, 10)

    # Footer 995-1012, maks 2 baris
    ft_lines = wrap(d, FOOTER, F(SANS, 8), 1004)
    draw_lines(d, 10, 996, ft_lines[:2], F(SANS, 8), GREY, 8)

    # Bottom strip 1012-1024
    d.rectangle([0, 1012, W, 1024], fill=NAVY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out)
    return out


if __name__ == "__main__":
    print(build())
