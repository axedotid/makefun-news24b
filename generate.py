#!/usr/bin/env python3
"""Generate an original newspaper front page summing up world news of
Tuesday 24 November 2026, from real BBC RSS headlines of that day."""
import json
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER   = (244, 239, 228)
INK     = (28, 30, 36)
MUTED   = (90, 92, 100)
NAVY    = (16, 22, 38)
RULE    = (40, 42, 50)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF   = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS    = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TAG = {
    "AMERICAS": (178, 34, 34), "AFRICA": (200, 130, 26),
    "BRITAIN": (31, 78, 140), "POLITICS": (106, 61, 154),
    "BUSINESS": (31, 122, 77), "EDUCATION": (18, 124, 124),
    "EUROPE": (37, 99, 175), "ASIA": (176, 58, 96),
    "MIDDLE EAST": (150, 90, 20), "TECHNOLOGY": (70, 70, 180),
    "SCIENCE": (20, 120, 110), "WORLD": (60, 60, 70), "CULTURE": (150, 60, 120),
}

_meas = ImageDraw.Draw(Image.new("RGB", (10, 10)))
def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if _meas.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out

def draw_lines(d, x, y, lines, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

# ---- load & split ------------------------------------------------------
items = json.load(open("curated.json"))
lead = items[0]
rest = items[1:]

LM = 32
COL_GAP = 22
COL_W = (W - 2*LM - COL_GAP)//2

# masthead
MAST_H = 150
DATE_H = 38
LEAD_TOP_PAD = 16

# choose fonts that FIT the available height
avail_h = H - MAST_H - DATE_H - 40  # 40 = footer
# We'll pick card font size then check total column height fits between
# lead bottom and footer.
def build(card_fs, lead_fs, gap):
    card_font = F(SERIF_B, card_fs)
    card_lh = card_fs + 6
    lead_font = F(SERIF_B, lead_fs)
    lead_lh = lead_fs + 10
    tagf = F(SANS_B, 13)
    # lead height
    lead_lines = wrap(lead["title"], lead_font, W-2*LM)
    lead_block = 40 + len(lead_lines)*lead_lh + 8 + 3 + 16
    y0 = MAST_H + DATE_H + LEAD_TOP_PAD + lead_block
    def card_h(t):
        n = len(wrap(t, card_font, COL_W-22))
        return 30 + n*card_lh + 6
    cols = {0: y0, 1: y0}
    heights = {}
    for it in rest:
        h = card_h(it["title"])
        col = 0 if cols[0] <= cols[1] else 1
        cols[col] += h + gap
    return {
        "card_font": card_font, "card_lh": card_lh, "lead_font": lead_font,
        "lead_lh": lead_lh, "tagf": tagf, "lead_lines": lead_lines,
        "y0": y0, "maxbottom": max(cols.values()), "card_h": card_h,
    }

footer_top = H - 40
best = None
for cfs in range(26, 14, -1):
    r = build(cfs, 44 if cfs >= 20 else 40, 12)
    if r["maxbottom"] <= footer_top - 10:
        best = (cfs, r)
        break
if best is None:
    best = (15, build(15, 38, 8))
cfs, R = best

# ---- render ------------------------------------------------------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, W, MAST_H], fill=NAVY)
d.text((W/2, 22), "THE DAILY WORLD", font=F(SERIF_B, 58), fill=(246, 242, 232),
       anchor="ma")
d.text((W/2, 96), "INDEPENDENT  ·  GLOBAL  ·  SINCE 2026", font=F(SANS, 14),
       fill=(176, 184, 200), anchor="ma")
d.line([(0, MAST_H-16), (W, MAST_H-16)], fill=(120, 128, 150), width=2)
d.line([(0, MAST_H-10), (W, MAST_H-10)], fill=(70, 78, 96), width=1)

d.rectangle([0, MAST_H, W, MAST_H+DATE_H], fill=(228, 221, 206))
d.text((W/2, MAST_H+10),
       "TUESDAY, 24 NOVEMBER 2026   ·   WORLD EDITION   ·   No. 24,331",
       font=F(SANS_B, 15), fill=INK, anchor="ma")

y = MAST_H + DATE_H + LEAD_TOP_PAD
lead_tag = lead["region"]; tc = TAG.get(lead_tag, TAG["WORLD"])
tagf = R["tagf"]
tw = d.textlength(lead_tag, font=F(SANS_B, 15))
lead_tag_f = F(SANS_B, 15)
d.rounded_rectangle([LM, y, LM+tw+24, y+26], radius=5, fill=tc)
d.text((LM+12, y+5), lead_tag, font=lead_tag_f, fill=(255, 255, 255))
d.text((LM+tw+34, y+5), "TOP STORY", font=F(SANS_B, 15), fill=MUTED)
y += 40
y = draw_lines(d, LM, y, R["lead_lines"], R["lead_font"], INK, R["lead_lh"])
y += 8
d.line([(LM, y), (W-LM, y)], fill=RULE, width=3)
y += 16

cols = {0: y, 1: y}
card_font = R["card_font"]; card_lh = R["card_lh"]; gap = 12
left_x = LM; right_x = LM + COL_W + COL_GAP
for it in rest:
    region = it["region"]; title = it["title"]
    ch = R["card_h"](title)
    col = 0 if cols[0] <= cols[1] else 1
    cy = cols[col]
    x = left_x if col == 0 else right_x
    cc = TAG.get(region, TAG["WORLD"])
    d.rounded_rectangle([x, cy, x+COL_W, cy+ch], radius=8, fill=(252, 250, 244),
                        outline=(208, 202, 190), width=1)
    d.rounded_rectangle([x, cy, x+7, cy+ch], radius=3, fill=cc)
    twr = d.textlength(region, font=tagf)
    d.rounded_rectangle([x+15, cy+10, x+15+twr+16, cy+10+19], radius=4, fill=cc)
    d.text((x+15+8, cy+10+3), region, font=tagf, fill=(255, 255, 255))
    lines = wrap(title, card_font, COL_W-22)
    ty = cy + 34
    for ln in lines:
        d.text((x+15, ty), ln, font=card_font, fill=INK)
        ty += card_lh
    cols[col] = cy + ch + gap

# footer
d.rectangle([0, H-40, W, H], fill=NAVY)
d.text((W/2, H-28),
       "Headlines: BBC News RSS  ·  Compiled for make.fun  ·  Rights remain with original publishers",
       font=F(SANS, 12), fill=(190, 196, 210), anchor="ma")

img.save("entry.png", optimize=True)

print("card font size:", cfs)
print("lead lines:", len(R["lead_lines"]))
print("column bottoms:", cols, "footer_top:", footer_top)
print("total headlines used:", len(items))
print("lead:", lead["region"], "|", lead["title"])