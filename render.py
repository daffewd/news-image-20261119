"""Render the 19 Nov 2026 front page (1024x1024), v2: lead visual panel
(flags), big market figure, larger type, page filled to the footer.
Deterministic: fixed fonts, fixed layout, no timestamps inside the image."""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 240, 214)
INK = (20, 20, 20)
RED = (178, 34, 34)
GREY = (90, 90, 90)
GREEN = (0, 128, 55)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def _wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_para(draw, x, y, width, text, fnt, leading, color=INK):
    for line in _wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, y, x0=40, x1=984, width=3):
    draw.line([(x0, y), (x1, y)], fill=INK, width=width)
    return y + width


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
y = 12

# top bar
f_top = font(SANS_B, 25)
d.text((40, y), "ONE PAGE  \u2022  THE WORLD", font=f_top, fill=INK)
right = "THURSDAY 19 NOVEMBER 2026"
d.text((984 - d.textlength(right, font=f_top), y), right, font=f_top, fill=INK)
y += 32
y = rule(d, y, width=4)

# masthead
f_mast = font(SERIF_B, 72)
mast = "THE WORLD TODAY"
d.text(((W - d.textlength(mast, font=f_mast)) / 2, y + 2), mast, font=f_mast, fill=INK)
y += 80
y = rule(d, y, width=4)

# subline
f_sub = font(SERIF_I, 26)
sub = "Thursday 19 November 2026 \u2014 the day's world news, in one picture"
d.text(((W - d.textlength(sub, font=f_sub)) / 2, y + 5), sub, font=f_sub, fill=GREY)
y += 36
y = rule(d, y, width=2)

# lead headline, one line (second half in red)
f_lead = font(SERIF_B, 50)
l1 = "THREE LEADERS MEET "
l2 = "IN SHENZHEN"
w1 = d.textlength(l1, font=f_lead)
w2 = d.textlength(l2, font=f_lead)
x_start = (W - w1 - w2) / 2
d.text((x_start, y + 6), l1, font=f_lead, fill=INK)
d.text((x_start + w1, y + 6), l2, font=f_lead, fill=RED)
y += 62
f_body = font(SERIF, 30)
y = draw_para(
    d, 40, y, 944,
    "Trump, Xi and Putin hold their first three-way talks on the sidelines of the "
    "APEC summit, issuing a joint declaration on nuclear risks and stable energy flows.",
    f_body, 36)
y += 6

# --- lead visual panel: three flags ---
panel_y = y
panel_h = 104
fw, fh = 272, 62
fxs = [60, 376, 692]
# USA flag
x0 = fxs[0]
d.rectangle([x0, panel_y, x0 + fw, panel_y + fh], outline=INK, width=2)
stripe_h = fh / 7
for i in range(7):
    if i % 2 == 0:
        d.rectangle([x0 + 2, panel_y + 2 + i * stripe_h, x0 + fw - 2,
                     panel_y + 2 + (i + 1) * stripe_h], fill=(190, 30, 45))
    else:
        d.rectangle([x0 + 2, panel_y + 2 + i * stripe_h, x0 + fw - 2,
                     panel_y + 2 + (i + 1) * stripe_h], fill=(255, 255, 255))
canton_w, canton_h = 118, stripe_h * 4
d.rectangle([x0 + 2, panel_y + 2, x0 + canton_w, panel_y + canton_h], fill=(40, 60, 140))
for r in range(4):
    for c in range(6):
        cx = x0 + 14 + c * 19
        cy = panel_y + 9 + r * 9
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))
# China flag
x0 = fxs[1]
d.rectangle([x0, panel_y, x0 + fw, panel_y + fh], fill=(222, 41, 49), outline=INK, width=2)
star(d, x0 + 36, panel_y + 22, 15, (255, 222, 0))
for sx, sy in [(66, 10), (74, 21), (74, 32), (66, 43)]:
    star(d, x0 + sx, panel_y + sy, 5, (255, 222, 0))
# Russia flag
x0 = fxs[2]
d.rectangle([x0, panel_y, x0 + fw, panel_y + fh], outline=INK, width=2)
band = fh / 3
d.rectangle([x0 + 2, panel_y + 2, x0 + fw - 2, panel_y + band], fill=(255, 255, 255))
d.rectangle([x0 + 2, panel_y + band, x0 + fw - 2, panel_y + 2 * band], fill=(30, 80, 180))
d.rectangle([x0 + 2, panel_y + 2 * band, x0 + fw - 2, panel_y + fh - 2], fill=(210, 35, 45))
# captions
f_cap = font(SANS_B, 21)
for fx, cap in zip(fxs, ["UNITED STATES", "CHINA", "RUSSIA"]):
    d.text((fx + (fw - d.textlength(cap, font=f_cap)) / 2, panel_y + fh + 7),
           cap, font=f_cap, fill=INK)
y = panel_y + panel_h + 4
y = rule(d, y, width=2)

# two-column row: Markets / Tech
f_kick = font(SANS_B, 26)
f_head = font(SERIF_B, 34)
f_small = font(SERIF, 28)
col_w = 452
y0 = y + 10
x = 40
d.text((x, y0), "MARKETS", font=f_kick, fill=RED)
y1 = draw_para(d, x, y0 + 32, col_w, "Anthropic soars on debut", f_head, 38)
# big figure block: +17% with close/open lines beside it
f_big = font(SANS_B, 58)
d.text((x, y1 + 2), "+17%", font=f_big, fill=GREEN)
f_line = font(SERIF, 25)
d.text((x + 205, y1 + 6), "close $97.17", font=f_line, fill=INK)
d.text((x + 205, y1 + 36), "opened +34% at $111.50", font=f_line, fill=INK)
# small bar pair under the figure (17 vs 34, proportional)
bar_y = y1 + 68
d.rectangle([x, bar_y, x + 110, bar_y + 10], fill=GREEN)
d.rectangle([x, bar_y + 14, x + 220, bar_y + 24], fill=GREEN)
y1 = bar_y + 28
y1 = draw_para(
    d, x, y1, col_w,
    "About $81.3bn raised; valuation near $1.5 trillion.",
    f_small, 32)
d.line([(512, y0), (512, y1)], fill=GREY, width=2)
x = 532
d.text((x, y0), "TECH", font=f_kick, fill=RED)
y2 = draw_para(d, x, y0 + 32, col_w, "Gemini gets computer use", f_head, 38)
y2 = draw_para(
    d, x, y2 + 2, col_w,
    "Google adds computer use to its Gemini Mac app \u2014 sorting files, filling "
    "forms, running multi-step tasks. Mid-tier model Gemini 4 Neon also ships.",
    f_small, 32)
y = max(y1, y2) + 6
y = rule(d, y, width=2)

# three-column row
f_small3 = font(SERIF, 27)
col_w3 = 300
y0 = y + 10
cols = [
    ("THE GULF", "Tankers ablaze off Hormuz",
     "Three oil tankers catch fire on mines east of the Strait of Hormuz, Iran says."),
    ("JUSTICE", "World court: Myanmar guilty",
     "World court rules Myanmar committed genocide against the Rohingya."),
    ("UKRAINE", "Bridge hit again",
     "Ukraine strikes the Crimean Bridge a third time in a week; Russian strikes "
     "kill five, cut power."),
]
ys = []
for i, (kick, head, body) in enumerate(cols):
    x = 40 + i * 322
    d.text((x, y0), kick, font=f_kick, fill=RED)
    yy = draw_para(d, x, y0 + 32, col_w3, head, f_head, 36)
    yy = draw_para(d, x, yy + 2, col_w3, body, f_small3, 30)
    ys.append(yy)
    if i < 2:
        d.line([(40 + (i + 1) * 322 - 11, y0), (40 + (i + 1) * 322 - 11, yy)], fill=GREY, width=2)
y = max(ys) + 6
y = rule(d, y, width=2)

# also strip
f_also = font(SERIF_B, 23)
y = draw_para(
    d, 40, y + 8, 944,
    "ALSO \u2022 DeepSeek closes $105bn funding \u2022 COP31 enters final talks "
    "\u2022 Muse Charm at ~$300",
    f_also, 30)
y += 6
y = rule(d, y, width=2)

# footer
f_foot = font(SERIF_I, 24)
foot = "All stories from Thursday 19 November 2026"
d.text(((W - d.textlength(foot, font=f_foot)) / 2, y + 6), foot, font=f_foot, fill=GREY)

print("final y:", y)
img.save("/home/hatch/workspace/makefun-entries/news-image-20261119/entry.png")
print("saved", img.size)
