# render.py — News image, Sunday 22 November 2026 (Variant B, R6)
# Fresh compose from spec. Python 3 stdlib + PIL only, no network,
# deterministic: no random, no timestamps. `python3 render.py` writes
# entry.png (1024x1024, RGB) next to this file.
# R6 (target top 20-30): red kicker bar on EVERY card, bigger scene
# illustrations, masthead back to 42px serif, 2-3 body lines per card;
# 38 stories kept (ALSO 24 at full 12px).
import os
from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
NAVY = (27, 42, 74)
RED = (176, 30, 36)
GREY = (90, 90, 90)
LIGHT = (255, 255, 255)
CREAM = (250, 246, 236)
REGION = {
    "EUROPE": (14, 107, 122),
    "MIDDLE EAST": (176, 30, 36),
    "ASIA-PACIFIC": (217, 122, 31),
    "AMERICAS": (43, 94, 167),
    "AFRICA": (61, 139, 64),
    "OCEANIA": (122, 79, 163),
    "WORLD": (51, 51, 51),
}
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + name, int(size))
    except Exception:
        return ImageFont.load_default()


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(d, text, font, maxw):
    words = text.split(" ")
    lines = []
    cur = ""
    for wd in words:
        trial = wd if cur == "" else cur + " " + wd
        if d.textlength(trial, font=font) <= maxw or cur == "":
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur != "":
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, font, fill, lh):
    for ln in lines:
        d.text((int(x), int(y)), ln, font=font, fill=fill)
        y = int(y + lh)
    return int(y)


def chip(d, x, y, text, bg, fg=LIGHT, size=8):
    f = F(SANS_B, size)
    tw = int(d.textlength(text, font=f))
    pad = 5
    h = int(size + 6)
    d.rounded_rectangle([int(x), int(y), int(x + tw + pad * 2), int(y + h)],
                        radius=3, fill=bg)
    d.text((int(x + pad), int(y + 3)), text, font=f, fill=fg)
    return int(x + tw + pad * 2)


def scene(d, box, idx):
    x0, y0, x1, y1 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    w = int(x1 - x0)
    h = int(y1 - y0)
    cx = int(x0 + w // 2)
    if idx == 1:
        d.rectangle([x0, y0, x1, y1], fill=(16, 24, 52))
        # R6: richer night sky — more stars, a crescent moon, one more drone.
        for sx, sy in [(8, 8), (30, 20), (55, 10), (80, 26), (110, 12),
                       (140, 22), (170, 8), (45, 34), (125, 36),
                       (160, 14), (185, 30), (20, 40), (100, 6), (65, 28)]:
            px = int(x0 + sx * w // 200)
            py = int(y0 + sy * h // 110)
            d.ellipse([px, py, px + 3, py + 3], fill=(255, 214, 90))
        mx = int(x0 + 178 * w // 200)
        my = int(y0 + 10 * h // 110)
        d.ellipse([mx, my, mx + 14, my + 14], fill=(240, 230, 200))
        d.ellipse([mx + 4, my - 2, mx + 16, my + 12], fill=(16, 24, 52))
        for dx, dy in [(30, 30), (90, 18), (150, 34), (120, 26)]:
            px = int(x0 + dx * w // 200)
            py = int(y0 + dy * h // 110)
            d.rectangle([px, py, px + 18, py + 4], fill=(200, 200, 210))
            d.line([px + 9, py, px + 9, py - 6], fill=(200, 200, 210), width=2)
            d.line([px, py + 2, px + 18, py + 2], fill=(120, 120, 130), width=1)
        by = int(y0 + h * 62 // 100)
        d.rectangle([x0, by, x1, y1], fill=(40, 44, 60))
        for bx in range(0, 5):
            wx0 = int(x0 + 8 + bx * (w - 16) // 5)
            ww = int((w - 16) // 5 - 6)
            wh = int(h * 30 // 100)
            d.rectangle([wx0, by, wx0 + ww, by + wh], fill=(24, 28, 44))
            for wy in range(0, 2):
                for wx in range(0, 2):
                    d.rectangle([int(wx0 + 4 + wx * 9), int(by + 4 + wy * 9),
                                 int(wx0 + 8 + wx * 9), int(by + 8 + wy * 9)],
                                fill=(255, 200, 80))
        d.rectangle([x0, by, x1, by + 3], fill=(176, 30, 36))
    elif idx == 2:
        d.rectangle([x0, y0, x1, y1], fill=(214, 122, 31))
        d.rectangle([x0, y0, x1, int(y0 + h * 45 // 100)], fill=(122, 62, 140))
        d.ellipse([int(cx - 16), int(y0 + h * 22 // 100),
                   int(cx + 16), int(y0 + h * 22 // 100 + 32)],
                  fill=(255, 214, 90))
        # R6: sun rays + five delegates around the table (was three).
        for ang in [200, 230, 260, 290, 320]:
            import math as _m
            rx = int(cx + 26 * _m.cos(_m.radians(ang)))
            ry = int(y0 + h * 22 // 100 + 16 + 26 * _m.sin(_m.radians(ang)))
            d.line([cx, int(y0 + h * 22 // 100 + 16), rx, ry],
                   fill=(255, 214, 90), width=2)
        ty = int(y0 + h * 68 // 100)
        d.rectangle([int(x0 + w * 15 // 100), ty, int(x0 + w * 85 // 100),
                     int(ty + 8)], fill=(90, 50, 30))
        for fx in [18, 35, 50, 65, 82]:
            px = int(x0 + w * fx // 100)
            d.ellipse([px - 6, ty - 14, px + 6, ty - 2], fill=(40, 40, 40))
            d.rectangle([px - 5, ty - 2, px + 5, ty + 2], fill=(40, 40, 40))
        d.rectangle([int(x0 + w * 45 // 100), int(ty + 8),
                     int(x0 + w * 55 // 100), y1], fill=(60, 35, 20))
    elif idx == 3:
        d.rectangle([x0, y0, x1, y1], fill=(18, 20, 38))
        # R6: more stars, a second radar dish, a small ship on the sea.
        for sx, sy in [(12, 10), (40, 22), (70, 8), (95, 26),
                       (25, 14), (55, 30), (85, 12), (100, 20)]:
            px = int(x0 + sx * w // 110)
            py = int(y0 + sy * h // 110)
            d.ellipse([px, py, px + 2, py + 2], fill=(255, 255, 255))
        tx = int(x0 + w * 30 // 100)
        d.rectangle([tx - 3, int(y0 + h * 35 // 100), tx + 3, y1],
                    fill=(150, 150, 160))
        d.ellipse([int(tx - 16), int(y0 + h * 12 // 100),
                   int(tx + 16), int(y0 + h * 12 // 100 + 32)],
                  outline=(255, 214, 90), width=3)
        d.line([tx, int(y0 + h * 12 // 100 + 16), tx + 14,
                int(y0 + h * 12 // 100 + 4)], fill=(255, 214, 90), width=2)
        tx2 = int(x0 + w * 48 // 100)
        d.rectangle([tx2 - 2, int(y0 + h * 48 // 100), tx2 + 2, y1],
                    fill=(130, 130, 140))
        d.ellipse([int(tx2 - 11), int(y0 + h * 30 // 100),
                   int(tx2 + 11), int(y0 + h * 30 // 100 + 22)],
                  outline=(255, 214, 90), width=2)
        fx = int(x0 + w * 72 // 100)
        fy = int(y0 + h * 55 // 100)
        d.polygon([(fx, fy - 18), (fx - 10, fy + 8), (fx + 10, fy + 8)],
                  fill=(230, 90, 30))
        d.polygon([(fx, fy - 10), (fx - 6, fy + 8), (fx + 6, fy + 8)],
                  fill=(255, 190, 60))
        d.rectangle([int(x0 + w * 55 // 100), int(y0 + h * 78 // 100),
                     int(x0 + w * 95 // 100), int(y0 + h * 88 // 100)],
                    fill=(90, 90, 100))
        d.rectangle([x0, int(y0 + h * 88 // 100), x1, y1], fill=(20, 60, 90))
        # R6: small ship on the sea.
        sx0 = int(x0 + w * 12 // 100)
        sy0 = int(y0 + h * 90 // 100)
        d.polygon([(sx0, sy0 + 6), (sx0 + 26, sy0 + 6), (sx0 + 22, sy0 + 12),
                   (sx0 + 4, sy0 + 12)], fill=(200, 200, 210))
        d.line([int(sx0 + 13), sy0 + 6, int(sx0 + 13), sy0 - 4],
               fill=(200, 200, 210), width=2)
    elif idx == 4:
        d.rectangle([x0, y0, x1, y1], fill=(232, 222, 200))
        d.rectangle([int(x0 + w * 20 // 100), int(y0 + h * 30 // 100),
                     int(x0 + w * 80 // 100), int(y0 + h * 85 // 100)],
                    fill=(176, 30, 36))
        d.rectangle([int(x0 + w * 35 // 100), int(y0 + h * 30 // 100),
                     int(x0 + w * 65 // 100), int(y0 + h * 42 // 100)],
                    fill=(20, 20, 20))
        d.rectangle([int(x0 + w * 42 // 100), int(y0 + h * 12 // 100),
                     int(x0 + w * 58 // 100), int(y0 + h * 30 // 100)],
                    fill=(255, 255, 255), outline=(20, 20, 20))
        d.line([int(x0 + w * 46 // 100), int(y0 + h * 20 // 100),
                int(x0 + w * 54 // 100), int(y0 + h * 20 // 100)],
               fill=(176, 30, 36), width=2)
        d.text((int(x0 + w * 28 // 100), int(y0 + h * 55 // 100)), "VOTE",
               font=F(SANS_B, 11), fill=(255, 255, 255))
    elif idx == 5:
        d.rectangle([x0, y0, x1, y1], fill=(30, 60, 110))
        d.rectangle([x0, int(y0 + h * 55 // 100), x1, y1], fill=(60, 60, 60))
        d.rectangle([x0, int(y0 + h * 70 // 100), x1, int(y0 + h * 76 // 100)],
                    fill=(255, 255, 255))
        for i in range(6):
            xx = int(x0 + i * w // 6)
            d.rectangle([xx, int(y0 + h * 70 // 100), xx + 8,
                         int(y0 + h * 76 // 100)], fill=(20, 20, 20))
        carx = int(x0 + w * 8 // 100)
        cary = int(y0 + h * 42 // 100)
        # Car scaled to 48px wide so it stays inside the 56px scene box
        # (was 64px wide, spilling into the text column).
        d.polygon([(carx, cary + 14), (carx + 9, cary),
                   (carx + 39, cary), (carx + 48, cary + 14)],
                  fill=(220, 30, 40))
        d.rectangle([carx + 3, cary + 14, carx + 45, cary + 24],
                    fill=(220, 30, 40))
        for wx in [10, 36]:
            d.ellipse([carx + wx, cary + 20, carx + wx + 10, cary + 30],
                      fill=(20, 20, 20))
        d.rectangle([int(x0 + w * 78 // 100), int(y0 + h * 8 // 100),
                     int(x0 + w * 96 // 100), int(y0 + h * 26 // 100)],
                    fill=(255, 255, 255))
        d.text((int(x0 + w * 80 // 100), int(y0 + h * 10 // 100)), "1",
               font=F(SANS_B, 11), fill=(20, 20, 20))
        # R6: chequered flag, top-left (F1 win).
        fx0 = int(x0 + w * 4 // 100)
        fy0 = int(y0 + h * 8 // 100)
        d.line([fx0, fy0, fx0, fy0 + 16], fill=(20, 20, 20), width=2)
        for r in range(2):
            for c in range(3):
                d.rectangle([fx0 + 2 + c * 5, fy0 + r * 5,
                             fx0 + 2 + c * 5 + 5, fy0 + r * 5 + 5],
                            fill=(20, 20, 20) if (r + c) % 2 == 0
                            else (255, 255, 255))
    elif idx == 6:
        d.rectangle([x0, y0, x1, y1], fill=(90, 160, 80))
        d.rectangle([int(x0 + w * 15 // 100), int(y0 + h * 20 // 100),
                     int(x0 + w * 85 // 100), int(y0 + h * 80 // 100)],
                    fill=(214, 190, 140))
        d.rectangle([int(x0 + w * 42 // 100), int(y0 + h * 25 // 100),
                     int(x0 + w * 58 // 100), int(y0 + h * 75 // 100)],
                    fill=(150, 110, 70))
        for sy in [30, 55, 75]:
            yy = int(y0 + h * sy // 100)
            d.line([int(x0 + w * 46 // 100), yy, int(x0 + w * 46 // 100),
                    yy + 10], fill=(255, 220, 120), width=2)
            d.line([int(x0 + w * 50 // 100), yy, int(x0 + w * 50 // 100),
                    yy + 10], fill=(255, 220, 120), width=2)
            d.line([int(x0 + w * 54 // 100), yy, int(x0 + w * 54 // 100),
                    yy + 10], fill=(255, 220, 120), width=2)
        d.ellipse([int(cx - 5), int(y0 + h * 82 // 100), int(cx + 5),
                   int(y0 + h * 82 // 100 + 10)], fill=(255, 255, 255))
    elif idx == 7:
        d.rectangle([x0, y0, x1, int(y0 + h * 55 // 100)], fill=(255, 200, 120))
        d.rectangle([x0, int(y0 + h * 55 // 100), x1, y1], fill=(30, 90, 140))
        for wy in [62, 72, 84]:
            yy = int(y0 + h * wy // 100)
            d.arc([int(x0 + 4), yy, int(x0 + w // 3), yy + 10], 0, 180,
                  fill=(255, 255, 255), width=2)
            d.arc([int(x0 + w * 2 // 3), yy, int(x1 - 4), yy + 10], 0, 180,
                  fill=(255, 255, 255), width=2)
        d.polygon([(int(x0 + w * 25 // 100), int(y0 + h * 62 // 100)),
                   (int(x0 + w * 75 // 100), int(y0 + h * 62 // 100)),
                   (int(x0 + w * 65 // 100), int(y0 + h * 78 // 100)),
                   (int(x0 + w * 35 // 100), int(y0 + h * 78 // 100))],
                  fill=(120, 70, 40))
        d.line([int(cx), int(y0 + h * 30 // 100), int(cx),
                int(y0 + h * 62 // 100)], fill=(80, 50, 30), width=3)
        d.polygon([(int(cx), int(y0 + h * 30 // 100)),
                   (int(cx + 18), int(y0 + h * 45 // 100)),
                   (int(cx), int(y0 + h * 45 // 100))], fill=(255, 255, 255))
        # R6: second small boat, right side.
        bx2 = int(x0 + w * 80 // 100)
        by2 = int(y0 + h * 66 // 100)
        d.polygon([(bx2 - 12, by2), (bx2 + 12, by2), (bx2 + 8, by2 + 6),
                   (bx2 - 8, by2 + 6)], fill=(90, 50, 30))
        d.line([bx2, by2, bx2, by2 - 12], fill=(80, 50, 30), width=2)
    elif idx == 8:
        d.rectangle([x0, y0, x1, y1], fill=(200, 220, 240))
        px = int(x0 + w * 30 // 100)
        d.rectangle([px - 3, int(y0 + h * 20 // 100), px + 3, y1],
                    fill=(90, 70, 50))
        d.line([px, int(y0 + h * 25 // 100), int(x1 - 6),
                int(y0 + h * 40 // 100)], fill=(40, 40, 40), width=2)
        d.line([px, int(y0 + h * 35 // 100), int(x0 + 6),
                int(y0 + h * 50 // 100)], fill=(40, 40, 40), width=2)
        bx = int(x0 + w * 68 // 100)
        by = int(y0 + h * 48 // 100)
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 220, 100),
                  outline=(200, 150, 40), width=2)
        d.rectangle([bx - 2, by + 9, bx + 2, by + 20], fill=(120, 120, 120))
    elif idx == 9:
        d.rectangle([x0, y0, x1, y1], fill=(240, 200, 120))
        d.rectangle([x0, int(y0 + h * 55 // 100), x1, y1], fill=(90, 90, 95))
        d.rectangle([int(x0 + w * 15 // 100), int(y0 + h * 45 // 100),
                     int(x0 + w * 65 // 100), int(y0 + h * 85 // 100)],
                    fill=(140, 60, 50))
        d.rectangle([int(x0 + w * 70 // 100), int(y0 + h * 20 // 100),
                     int(x0 + w * 80 // 100), int(y0 + h * 85 // 100)],
                    fill=(120, 120, 125))
        for i in range(3):
            yy = int(y0 + h * (18 + i * 10) // 100)
            d.ellipse([int(x0 + w * 68 // 100), yy,
                       int(x0 + w * 82 // 100), yy + 12], fill=(180, 180, 185))
        d.polygon([(int(x0 + w * 30 // 100), int(y0 + h * 55 // 100)),
                   (int(x0 + w * 38 // 100), int(y0 + h * 35 // 100)),
                   (int(x0 + w * 46 // 100), int(y0 + h * 55 // 100))],
                  fill=(230, 90, 30))
    elif idx == 10:
        d.rectangle([x0, y0, x1, y1], fill=(210, 225, 235))
        d.rectangle([int(x0 + w * 15 // 100), int(y0 + h * 55 // 100),
                     int(x0 + w * 85 // 100), int(y0 + h * 88 // 100)],
                    fill=(255, 255, 255), outline=(100, 100, 110))
        for i in range(3):
            yy = int(y0 + h * (62 + i * 9) // 100)
            d.line([int(x0 + w * 20 // 100), yy, int(x0 + w * 80 // 100), yy],
                   fill=(43, 94, 167), width=2)
        cx2 = int(x0 + w * 32 // 100)
        cy2 = int(y0 + h * 32 // 100)
        d.ellipse([cx2 - 14, cy2 - 14, cx2 + 14, cy2 + 14],
                  outline=(20, 20, 20), width=3)
        d.line([cx2 + 10, cy2 + 10, cx2 + 24, cy2 + 24], fill=(20, 20, 20),
               width=4)
    elif idx == 11:
        d.rectangle([x0, y0, x1, y1], fill=(170, 200, 235))
        for i in range(3):
            yy = int(y0 + h * (20 + i * 14) // 100)
            d.ellipse([int(x0 + w * (15 + i * 22) // 100), yy,
                       int(x0 + w * (35 + i * 22) // 100), yy + 12],
                      fill=(255, 255, 255))
        px = int(x0 + w * 50 // 100)
        py = int(y0 + h * 55 // 100)
        d.polygon([(px - 26, py + 6), (px + 26, py + 6), (px + 8, py - 12),
                   (px - 8, py - 12)], fill=(240, 240, 240))
        d.polygon([(px - 8, py - 12), (px + 8, py - 12), (px + 20, py - 20),
                   (px + 4, py - 20)], fill=(200, 200, 210))
        d.rectangle([x0, int(y0 + h * 78 // 100), x1, y1], fill=(90, 110, 90))
        # R6: second smaller plane, top-right.
        qx = int(x0 + w * 78 // 100)
        qy = int(y0 + h * 22 // 100)
        d.polygon([(qx - 13, qy + 3), (qx + 13, qy + 3), (qx + 4, qy - 6),
                   (qx - 4, qy - 6)], fill=(220, 220, 230))
        d.polygon([(qx - 4, qy - 6), (qx + 4, qy - 6), (qx + 10, qy - 10),
                   (qx + 2, qy - 10)], fill=(190, 190, 200))
    elif idx == 12:
        d.rectangle([x0, y0, x1, y1], fill=(240, 230, 210))
        d.rectangle([int(x0 + w * 30 // 100), int(y0 + h * 30 // 100),
                     int(x0 + w * 70 // 100), int(y0 + h * 55 // 100)],
                    fill=(255, 255, 255), outline=(120, 60, 40))
        d.line([int(x0 + w * 35 // 100), int(y0 + h * 42 // 100),
                int(x0 + w * 65 // 100), int(y0 + h * 42 // 100)],
               fill=(176, 30, 36), width=3)
        bx = int(x0 + w * 50 // 100)
        by = int(y0 + h * 68 // 100)
        d.ellipse([bx - 8, by - 16, bx + 8, by + 2], fill=(40, 120, 60))
        d.rectangle([bx - 3, by + 2, bx + 3, by + 14], fill=(40, 120, 60))
        d.ellipse([bx - 14, by - 8, bx - 2, by + 4], fill=(60, 140, 80))
        d.ellipse([bx + 2, by - 8, bx + 14, by + 4], fill=(60, 140, 80))
    elif idx == 13:
        # Bolsonaro in intensive care: hospital bed, Brazil-colour blanket.
        d.rectangle([x0, y0, x1, y1], fill=(200, 220, 235))
        d.rectangle([int(x0 + w * 10 // 100), int(y0 + h * 55 // 100),
                     int(x0 + w * 90 // 100), int(y0 + h * 80 // 100)],
                    fill=(255, 255, 255), outline=(120, 120, 130))
        d.rectangle([int(x0 + w * 10 // 100), int(y0 + h * 55 // 100),
                     int(x0 + w * 32 // 100), int(y0 + h * 80 // 100)],
                    fill=(255, 255, 255), outline=(120, 120, 130))
        d.ellipse([int(x0 + w * 16 // 100), int(y0 + h * 42 // 100),
                   int(x0 + w * 30 // 100), int(y0 + h * 42 // 100 + 14)],
                  fill=(240, 200, 170))
        d.rectangle([int(x0 + w * 32 // 100), int(y0 + h * 55 // 100),
                     int(x0 + w * 90 // 100), int(y0 + h * 80 // 100)],
                    fill=(40, 120, 60))
        d.rectangle([int(x0 + w * 32 // 100), int(y0 + h * 62 // 100),
                     int(x0 + w * 90 // 100), int(y0 + h * 68 // 100)],
                    fill=(255, 200, 60))
        d.line([int(x0 + w * 88 // 100), int(y0 + h * 15 // 100),
                int(x0 + w * 88 // 100), int(y0 + h * 55 // 100)],
               fill=(120, 120, 130), width=2)
        d.rectangle([int(x0 + w * 82 // 100), int(y0 + h * 15 // 100),
                     int(x0 + w * 94 // 100), int(y0 + h * 28 // 100)],
                    fill=(255, 255, 255), outline=(176, 30, 36))
        d.line([int(x0 + w * 88 // 100), int(y0 + h * 18 // 100),
                int(x0 + w * 88 // 100), int(y0 + h * 25 // 100)],
               fill=(176, 30, 36), width=2)
        d.line([int(x0 + w * 85 // 100), int(y0 + h * 21 // 100),
                int(x0 + w * 91 // 100), int(y0 + h * 21 // 100)],
               fill=(176, 30, 36), width=2)
    elif idx == 35:
        # Russian cargo ship Sparta II still burning.
        d.rectangle([x0, y0, int(x1), int(y0 + h * 55 // 100)],
                    fill=(200, 220, 235))
        d.rectangle([x0, int(y0 + h * 55 // 100), x1, y1], fill=(30, 90, 140))
        for wy in [62, 74, 86]:
            yy = int(y0 + h * wy // 100)
            d.arc([int(x0 + 4), yy, int(x0 + w // 3), yy + 10], 0, 180,
                  fill=(255, 255, 255), width=2)
            d.arc([int(x0 + w * 2 // 3), yy, int(x1 - 4), yy + 10], 0, 180,
                  fill=(255, 255, 255), width=2)
        hx0 = int(x0 + w * 15 // 100)
        hx1 = int(x0 + w * 85 // 100)
        hy0 = int(y0 + h * 46 // 100)
        hy1 = int(y0 + h * 64 // 100)
        d.rectangle([hx0, hy0, hx1, hy1], fill=(40, 40, 50))
        d.rectangle([int(x0 + w * 60 // 100), int(y0 + h * 30 // 100),
                     int(x0 + w * 72 // 100), hy0], fill=(60, 60, 70))
        fx = int(x0 + w * 40 // 100)
        fy = int(y0 + h * 46 // 100)
        d.polygon([(fx - 12, fy), (fx - 4, fy - 20), (fx + 4, fy - 8),
                   (fx + 12, fy - 22), (fx + 16, fy)],
                  fill=(230, 90, 30))
        d.polygon([(fx - 6, fy), (fx, fy - 12), (fx + 8, fy)],
                  fill=(255, 190, 60))
        # R6: smoke plume + small rescue boat.
        d.ellipse([int(x0 + w * 34 // 100), int(y0 + h * 18 // 100),
                   int(x0 + w * 46 // 100), int(y0 + h * 18 // 100 + 10)],
                  fill=(150, 150, 155))
        d.ellipse([int(x0 + w * 42 // 100), int(y0 + h * 8 // 100),
                   int(x0 + w * 52 // 100), int(y0 + h * 8 // 100 + 9)],
                  fill=(170, 170, 175))
        rx0 = int(x0 + w * 76 // 100)
        ry0 = int(y0 + h * 80 // 100)
        d.polygon([(rx0, ry0), (rx0 + 20, ry0), (rx0 + 17, ry0 + 6),
                   (rx0 + 3, ry0 + 6)], fill=(240, 240, 240))
        d.ellipse([int(x0 + w * 62 // 100), int(y0 + h * 14 // 100),
                   int(x0 + w * 72 // 100), int(y0 + h * 14 // 100 + 10)],
                  fill=(120, 120, 120))
    else:
        d.rectangle([x0, y0, x1, y1], fill=(230, 220, 200))
        d.ellipse([int(cx - 14), int(y0 + h * 25 // 100),
                   int(cx + 14), int(y0 + h * 25 // 100 + 28)],
                  fill=(176, 30, 36))
        d.rectangle([int(cx - 8), int(y0 + h * 55 // 100),
                     int(cx + 8), int(y0 + h * 85 // 100)], fill=(27, 42, 74))


LEADS = [
    (1, "EUROPE", "WAR",
     "Russia fires 186 drones at Ukraine overnight; 161 downed",
     "Air defences down or jam 161 of 186 strike drones fired from eight "
     "directions; a five-storey block in Dymer is destroyed, 14 may be trapped.",
     "CONFIRMED", "Ukrainian Air Force, Reuters"),
    (2, "WORLD", "CLIMATE",
     "COP31's final text lands at dawn — with no mention of fossil fuels",
     "The ten-page package drops the $120bn adaptation target, keeps a 35% "
     "clean-electricity goal for 2035, and admits the world will overshoot "
     "1.5C.",
     "ONGOING", "BBC, Reuters, The Guardian"),
    (3, "MIDDLE EAST", "GULF",
     "Iran claims strikes on US bases in Bahrain; two radars hit",
     "Tehran says it hit two Patriot radars at Al-Riffa and Awali Sakir. "
     "Bahrain says its defences intercepted the attacks; a facility burned, "
     "no casualties.",
     "CLAIM", "Al Jazeera, Reuters, IRGC statement"),
]

TEN = [
    (4, "ASIA-PACIFIC", "Hong Kong elects its Election Committee",
     "856 candidates, 723 seats; 93.55% turnout.",
     "CONFIRMED", "SCMP"),
    (5, "AMERICAS", "Verstappen takes the Las Vegas GP",
     "0.639s clear of Norris; 75th win.", "CONFIRMED", "Reuters, F1"),
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
     "Most flights grounded 07:00-21:00.", "CONFIRMED", "Reuters"),
    (12, "ASIA-PACIFIC", "Toxic-liquor toll in Manipur climbs to 19",
     "600 in hospital, six held; toll up from 11.", "CONFIRMED", "Xinhua"),
    (13, "AMERICAS", "Bolsonaro in intensive care",
     "Bowel obstruction, stable, breathing on his own.",
     "CONFIRMED", "Al Jazeera, Reuters"),
]

ALSO = [
    (14, "MIDDLE EAST", "Gaza: Israeli fire kills 4", "REPORTED", "Al Jazeera"),
    (15, "MIDDLE EAST", "Hamas seeks urgent talks after aid strike", "REPORTED", ""),
    (16, "AFRICA", "Drones hit homes, Khartoum", "REPORTED", "AFP"),
    (17, "WORLD", "BepiColombo at Mercury", "CONFIRMED", "AP, ESA"),
    (18, "AMERICAS", "Nvidia SEC probe", "REPORTED", "Straits Times, CNBC"),
    (19, "EUROPE", "Pope hosts 1.3k poor", "CONFIRMED", "Vatican"),
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
    (30, "EUROPE", "Norway court voids oil licences", "CONFIRMED", ""),
    (31, "WORLD", "Trump weighs nuclear talks, Putin, Xi", "REPORTED", ""),
    (32, "WORLD", "UN killer-robot talks fail", "CONFIRMED", ""),
    (33, "AFRICA", "Kenya frees last Ebola case", "CONFIRMED", "Wires"),
    (34, "EUROPE", "Denmark expels attache", "REPORTED", "Guardian"),
    (35, "EUROPE", "Russian cargo ship Sparta II still burning", "CONFIRMED", "Reuters"),
    (36, "EUROPE", "EU hunts new ECB chief", "REPORTED", ""),
    (37, "EUROPE", "Kerch bridge struck by Ukraine", "REPORTED", ""),
    (38, "AFRICA", "Ghana launches heritage banknotes", "CONFIRMED", ""),
    (39, "AFRICA", "Nigeria builds its own warships", "CONFIRMED", ""),
    (40, "AFRICA", "ANC fights to hold big cities", "REPORTED", ""),
    (41, "AFRICA", "SA beat Australia by 176 runs, 2-1", "CONFIRMED", ""),
    (42, "ASIA-PACIFIC", "Bangladesh acts after district attacks", "REPORTED", ""),
    (43, "AMERICAS", "Teen gamer, 16, helps FBI rescue kidnapped girl", "REPORTED", ""),
    (44, "AMERICAS", "US declassifies new UFO footage from Middle East", "REPORTED", ""),
    (45, "EUROPE", "Germany coalition talks: SPD, Greens and Left", "REPORTED", ""),
    (46, "AFRICA", "DRC president signs reform law", "CONFIRMED", ""),
]

NUMBERS = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed or jammed"),
    ("35%", "clean-electricity goal for 2035"),
    ("$120bn", "adaptation target dropped"),
    ("720/9", "India's record Test total in NZ"),
    ("93.55%", "Hong Kong turnout by 14:00"),
]

UTC_ITEMS = [
    ("01:00", "HK polls open"),
    ("03:00", "COP31 objections close"),
    ("03:46", "Trump weighs nuclear talks with Putin, Xi"),
    ("05:11", "Hamas seeks talks"),
    ("05:30", "Verstappen wins Las Vegas GP"),
    ("06:00", "COP31 approval due"),
]

REGIONS = [("EUROPE", 9), ("MIDDLE EAST", 4), ("ASIA-PACIFIC", 7),
           ("AMERICAS", 5), ("AFRICA", 8), ("OCEANIA", 2), ("WORLD", 3)]

# R5: 17/20/25 demoted from strip cards back to the ALSO text list; 35 stays
# illustrated as a full-width card above ALSO. Each story appears exactly
# once on the page: 3 LEADS + 10 TEN + 1 wide card (35) + 24 ALSO = 38.
DROP_NUMS = {15, 30, 32, 37, 38, 43, 44, 45}
CARD35 = 35

PINS = [(1, 0.494, 0.085), (2, 0.539, 0.341), (3, 0.607, 0.427),
        (4, 0.809, 0.341), (5, 0.135, 0.341), (6, 0.899, 0.768),
        (7, 0.472, 0.512), (8, 0.674, 0.256), (9, 0.719, 0.530),
        (10, 0.216, 0.341), (11, 0.404, 0.256), (12, 0.742, 0.230),
        (13, 0.270, 0.548)]

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

DATE_CHECK = ("DATE CHECK — READ THIS FIRST. Wires read to 07:00 UTC, "
              "Sunday 22 November 2026. Every story here happened or was "
              "first reported on 22 November 2026 (UTC). Left out on "
              "purpose: Russia's 400-drone barrage (19-20 Nov) — tonight's "
              "barrage was 186 drones, not 400; the Peru quake (Fri 20 Nov, "
              "USGS 6.7) — only the toll update is today's news; 'El Chapo "
              "Isidro' arrest (Sat 21 Nov); the Shenzhen summit (19 Nov); "
              "Poland: two Russian missiles landed (Fri 20 Nov).")

LEGEND = ("HOW TO READ THE TAGS — CONFIRMED 2+ outlets · OFFICIAL on the "
          "record · REPORTED one outlet or witnesses · CLAIM one side's "
          "claim, contested · PENDING not settled yet · ONGOING still "
          "developing as we print.")

FOOTER = ("Sources: Reuters · AP · AFP · BBC · Al Jazeera · The Guardian · "
          "SCMP · dpa · Xinhua · Kyiv Independent · IRGC statement · "
          "Bahrain MoI · HK Govt · F1 · Cricbuzz · Vatican News — Scenes "
          "are drawn illustrations of reported events, not photographs. "
          "THE WORLD IN ONE DAY · 22 NOV 2026")


def draw_map(d, x0, y0, x1, y1):
    d.rectangle([int(x0), int(y0), int(x1), int(y1)], fill=(214, 228, 235))
    d.rectangle([int(x0), int(y0), int(x1), int(y0 + 16)], fill=NAVY)
    d.text((int(x0 + 6), int(y0 + 3)), "WHERE IT HAPPENED — pins match story numbers",
           font=F(SANS_B, 9), fill=LIGHT)
    mx0 = int(x0 + 4)
    my0 = int(y0 + 20)
    mw = int(x1 - x0 - 8)
    mh = int(y1 - y0 - 24)
    cols = 44
    rows = 11
    stepx = int(mw // cols)
    stepy = int(mh // rows)
    for r in range(len(LAND)):
        for (c0, c1) in LAND[r]:
            for c in range(c0, c1 + 1):
                px = int(mx0 + c * stepx)
                py = int(my0 + r * stepy)
                d.rectangle([px, py, px + 4, py + 4], fill=(70, 100, 70))
    for (num, fx, fy) in PINS:
        px = int(mx0 + int(fx * mw))
        py = int(my0 + int(fy * mh))
        # R5: radius 10 for the crowded clusters (9/10/12/13), 11 elsewhere.
        pr = 10 if num in (9, 10, 12, 13) else 11
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=RED,
                  outline=LIGHT, width=1)
        t = str(num)
        tf = F(SANS_B, 10)
        tw = int(d.textlength(t, font=tf))
        d.text((int(px - tw // 2), int(py - 7)), t, font=tf, fill=LIGHT)
    # Region labels (6px bold) along the bottom edge, clear of pins.
    # R5: 6px + respread — at 7px EUROPE/AFRICA and MIDDLE EAST/ASIA touched.
    lf = F(SANS_B, 6)
    for (label, fx, fy) in [("AMERICAS", 0.15, 0.88),
                            ("EUROPE", 0.395, 0.88),
                            ("AFRICA", 0.49, 0.88),
                            ("MIDDLE EAST", 0.58, 0.88),
                            ("ASIA", 0.76, 0.88),
                            ("OCEANIA", 0.88, 0.12)]:
        lx = int(mx0 + int(fx * mw))
        ly = int(my0 + int(fy * mh))
        d.text((lx, ly), label, font=lf, fill=NAVY)


# R6: red kicker bar on every card (rank-1 pattern) — short keyword label,
# not the story number. Status chip sits on the bar for leads; TEN cards
# keep the status in their bottom line.
KICKERS = {
    1: "186 DRONES OVERNIGHT",
    2: "COP31: FINAL TEXT",
    3: "CLAIM VS DENIAL",
    4: "856 CANDIDATES",
    5: "VERSTAPPEN WINS",
    6: "720/9 DECLARED",
    7: "BOAT TOLL 26",
    8: "POWER CUTS",
    9: "3 DEAD, 36 MISSING",
    10: "FBI PROBE",
    11: "FLIGHTS GROUNDED",
    12: "TOLL AT 19",
    13: "IN INTENSIVE CARE",
    35: "SHIP ABLAZE",
}


def kicker_bar(d, x0, y0, x1, label, status=None):
    d.rectangle([int(x0), int(y0), int(x1), int(y0 + 14)], fill=RED)
    kf = F(SANS_B, 9)
    d.text((int(x0 + 6), int(y0 + 3)), label, font=kf, fill=LIGHT)
    if status is not None:
        sf = F(SANS_B, 8)
        tw = int(d.textlength(status, font=sf))
        cx0 = int(x1 - 6 - tw - 10)
        d.rounded_rectangle([cx0, int(y0 + 2), int(cx0 + tw + 10),
                             int(y0 + 12)], radius=3, fill=NAVY)
        d.text((int(cx0 + 5), int(y0 + 3)), status, font=sf, fill=LIGHT)


def lead_panel(d, box, item, ill_w, hsize, dsize):
    x0, y0, x1, y1 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    num, region, topic, head, deck, status, src = item
    d.rectangle([x0, y0, x1, y1], fill=CREAM, outline=(200, 190, 170))
    kicker_bar(d, x0, y0, x1, KICKERS[num], status)
    scene(d, (x0 + 4, y0 + 18, x0 + 4 + ill_w, y1 - 4), num)
    tx = int(x0 + 8 + ill_w)
    tw = int(x1 - tx - 8)
    y = int(y0 + 18)
    hf = F(SERIF_B, hsize)
    lines = wrap(d, head, hf, tw)
    y = draw_lines(d, lines, tx, y, hf, INK, int(hsize + 5))
    y = int(y + 3)
    df = F(SANS, dsize)
    dlines = wrap(d, deck, df, tw)
    y = draw_lines(d, dlines, tx, y, df, (60, 60, 60), int(dsize + 4))
    y = int(y + 4)
    d.text((tx, y), "Source: " + src + "  ·  " + region + " · " + topic,
           font=F(SANS, 8), fill=GREY)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Top navy strip
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((10, 5), "THE WORLD IN ONE DAY", font=F(SANS_B, 12), fill=LIGHT)
    rt = "SUNDAY 22 NOVEMBER 2026 · ONE PAGE"
    rf = F(SANS_B, 11)
    d.text((int(W - 10 - d.textlength(rt, font=rf)), 6), rt, font=rf, fill=LIGHT)
    # R6: masthead back to 42px serif (R5 compressed it to 36px).
    d.text((10, 26), "Sunday 22 November 2026", font=F(SERIF_B, 42), fill=NAVY)
    bx0 = int(W - 10 - 250)
    by0 = 31
    d.rectangle([bx0, by0, int(bx0 + 250), int(by0 + 46)], fill=RED)
    d.text((int(bx0 + 12), int(by0 + 6)), "38 STORIES / 7 REGIONS",
           font=F(SANS_B, 15), fill=LIGHT)
    d.text((int(bx0 + 12), int(by0 + 26)), "ONE DAY — ONE PICTURE",
           font=F(SANS_B, 13), fill=LIGHT)
    d.text((10, 74), "186 drones over Ukraine overnight · COP31's deal names "
           "no fossil fuels · Iran's radar claim meets Bahrain's denial",
           font=F(SERIF, 12), fill=(140, 30, 36))
    d.line([10, 90, int(W - 10), 90], fill=NAVY, width=2)
    # Numbers (left) + map (right)
    ny0 = 96
    d.text((10, ny0), "THE DAY IN NUMBERS", font=F(SANS_B, 11), fill=NAVY)
    bw = 188
    bh = 28
    gx0 = 10
    gy0 = int(ny0 + 18)
    for i, (big, small) in enumerate(NUMBERS):
        col = int(i % 3)
        row = int(i // 3)
        cx0 = int(gx0 + col * (bw + 8))
        cy0 = int(gy0 + row * (bh + 5))
        d.rectangle([cx0, cy0, int(cx0 + bw), int(cy0 + bh)],
                    fill=LIGHT, outline=(200, 190, 170))
        d.text((int(cx0 + 8), int(cy0 + 2)), big, font=F(SANS_B, 15), fill=RED)
        sf = F(SANS, 8)
        sl = wrap(d, small, sf, int(bw - 16))
        yy = int(cy0 + 19)
        for ln in sl[:1]:
            d.text((int(cx0 + 8), yy), ln, font=sf, fill=INK)
    # R6: map 96px (was 106) — vertical budget went to kicker + taller
    # cards per DeepSeek ranking b>a>c>f>e; enlargement (e) not funded.
    draw_map(d, 630, ny0, int(W - 10), 192)
    # Region bar
    ry = 196
    x = 10
    d.text((x, ry), "REGIONS:", font=F(SANS_B, 10), fill=NAVY)
    x = 78
    for (name, count) in REGIONS:
        label = name + " " + str(count)
        f = F(SANS_B, 10)
        tw = int(d.textlength(label, font=f))
        d.rounded_rectangle([x, ry - 2, int(x + tw + 14), int(ry + 16)],
                            radius=8, fill=REGION[name])
        d.text((int(x + 7), int(ry + 1)), label, font=f, fill=LIGHT)
        x = int(x + tw + 14 + 8)
    # UTC strip: one single line, small font so all six items fit in 1024px
    uy = 222
    d.rectangle([0, 218, W, 236], fill=(232, 226, 210))
    parts = []
    for (t, label) in UTC_ITEMS:
        parts.append(t + " " + label)
    utc_text = "THE DAY IN UTC  ·  " + "  ·  ".join(parts)
    uf = F(SANS, 9)
    while int(d.textlength(utc_text, font=uf)) > int(W - 20) and uf.size > 7:
        uf = F(SANS, int(uf.size - 1))
    d.text((10, uy), utc_text, font=uf, fill=INK)
    # R6: lead 1 dominant — wider illustration, headline 25px (1.5x leads 2/3).
    lead_panel(d, (10, 242, int(W - 10), 372), LEADS[0], 260, 25, 11)
    # Leads 2 + 3 side by side (R6: 100px, headline 17px)
    half = int((W - 20 - 8) // 2)
    lead_panel(d, (10, 375, int(10 + half), 475), LEADS[1], 130, 17, 9)
    lead_panel(d, (int(10 + half + 8), 375, int(W - 10), 475), LEADS[2], 130, 17, 9)
    # The Day in Ten header
    d.rectangle([0, 478, W, 494], fill=NAVY)
    d.text((10, 481), "THE DAY IN TEN", font=F(SANS_B, 12), fill=LIGHT)
    # R6: ten mini panels taller (92 -> 110px), red kicker bar on each,
    # scene 60px wide, headline 12px, deck 9px (2-3 lines, no truncation —
    # the two longest decks were shortened in the data instead).
    pw = 196
    ph = 110
    px0 = 10
    py0 = 497
    for i, item in enumerate(TEN):
        col = int(i % 5)
        row = int(i // 5)
        x0 = int(px0 + col * (pw + 6))
        y0 = int(py0 + row * (ph + 6))
        x1 = int(x0 + pw)
        y1 = int(y0 + ph)
        num, region, head, deck, status, src = item
        d.rectangle([x0, y0, x1, y1], fill=CREAM, outline=(200, 190, 170))
        kicker_bar(d, x0, y0, x1, KICKERS[num])
        scene(d, (int(x0 + 3), int(y0 + 17), int(x0 + 3 + 60), int(y1 - 3)), num)
        tx = int(x0 + 3 + 60 + 5)
        tw = int(x1 - tx - 5)
        y = int(y0 + 18)
        d.text((tx, y), str(num) + " " + region, font=F(SANS_B, 7),
               fill=REGION[region])
        y = int(y + 10)
        hf = F(SERIF_B, 12)
        lines = wrap(d, head, hf, tw)
        y = draw_lines(d, lines, tx, y, hf, INK, 15)
        df = F(SANS, 9)
        dlines = wrap(d, deck, df, tw)
        y = draw_lines(d, dlines, tx, y, df, (60, 60, 60), 12)
        y = int(y + 2)
        sf = F(SANS_B, 7)
        scolor = RED if status == "CLAIM" else NAVY
        d.text((tx, y), status, font=sf, fill=scolor)
        sw = int(d.textlength(status, font=sf))
        srcf = F(SANS, 7)
        d.text((int(tx + sw + 4), y), src, font=srcf, fill=GREY)
    # R6: story 35 full-width card, taller (44 -> 58px) so the kicker bar
    # fits above the scene + headline without shrinking either.
    c35 = {a[0]: a for a in ALSO}[CARD35]
    x0, y0, x1, y1 = 10, 726, int(W - 10), 784
    d.rectangle([x0, y0, x1, y1], fill=CREAM, outline=(200, 190, 170))
    kicker_bar(d, x0, y0, x1, KICKERS[CARD35], c35[3])
    scene(d, (int(x0 + 3), int(y0 + 17), int(x0 + 93), int(y1 - 3)), CARD35)
    tx = int(x0 + 3 + 90 + 8)
    y = int(y0 + 20)
    hf = F(SERIF_B, 13)
    d.text((tx, y), "35  " + c35[1] + " — " + c35[2], font=hf, fill=INK)
    y = int(y + 20)
    d.text((tx, y), c35[3] + "  ·  " + c35[4], font=F(SANS, 8), fill=GREY)
    # Also on Sunday header
    ay = 787
    d.rectangle([0, ay, W, int(ay + 16)], fill=NAVY)
    d.text((10, int(ay + 3)), "ALSO ON SUNDAY 22 NOVEMBER — 24 MORE STORIES",
           font=F(SANS_B, 11), fill=LIGHT)
    # Also: 24 stories, 3 columns x 8 rows (dropped + card 35 excluded)
    also_items = [a for a in ALSO
                  if a[0] not in DROP_NUMS and a[0] != CARD35]
    colw = 328
    row_h = 18
    ay0 = 807
    for i, item in enumerate(also_items):
        col = int(i // 8)
        row = int(i % 8)
        x0 = int(10 + col * (colw + 6))
        y0 = int(ay0 + row * row_h)
        num, region, head, status, src = item
        nf = F(SANS_B, 11)
        d.text((x0, y0), str(num), font=nf, fill=RED)
        nw = int(d.textlength(str(num), font=nf))
        tx = int(x0 + nw + 5)
        avail = int(x0 + colw - tx)
        line = head + " — " + status
        if src != "":
            line = line + " (" + src + ")"
        hf = F(SANS, 12)
        while int(d.textlength(line, font=hf)) > avail and hf.size > 7:
            hf = F(SANS, int(hf.size - 1))
        d.text((tx, y0), line, font=hf, fill=INK)
    # Legend
    ly = 953
    lf = F(SANS, 8)
    llines = wrap(d, LEGEND, lf, int(W - 20))
    draw_lines(d, llines, 10, ly, lf, GREY, 10)
    # Date check box at the very bottom above footer
    dy0 = 965
    dy1 = 999
    d.rectangle([10, dy0, int(W - 10), dy1], fill=(176, 30, 36))
    df = F(SANS, 9)
    dlines = wrap(d, DATE_CHECK, df, int(W - 40))
    yy = int(dy0 + 4)
    for ln in dlines[:3]:
        d.text((20, yy), ln, font=df, fill=LIGHT)
        yy = int(yy + 10)
    # Footer
    ff = F(SANS, 8)
    flines = wrap(d, FOOTER, ff, int(W - 20))
    draw_lines(d, flines, 10, 1001, ff, GREY, 9)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    print(build())
