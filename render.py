"""Render the 19 Nov 2026 front page (1024x1024) in the same style as the
18 Nov entry: cream paper, serif masthead, red kickers. Deterministic:
fixed fonts, fixed layout, no timestamps inside the image."""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 240, 214)
INK = (20, 20, 20)
RED = (178, 34, 34)
GREY = (90, 90, 90)

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


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
y = 20

# top bar
f_top = font(SANS_B, 25)
d.text((40, y), "ONE PAGE  \u2022  THE WORLD", font=f_top, fill=INK)
right = "THURSDAY 19 NOVEMBER 2026"
d.text((984 - d.textlength(right, font=f_top), y), right, font=f_top, fill=INK)
y += 36
y = rule(d, y, width=4)

# masthead
f_mast = font(SERIF_B, 92)
mast = "THE WORLD TODAY"
d.text(((W - d.textlength(mast, font=f_mast)) / 2, y + 4), mast, font=f_mast, fill=INK)
y += 100
y = rule(d, y, width=4)

# subline
f_sub = font(SERIF_I, 26)
sub = "Thursday 19 November 2026 \u2014 the day's world news, in one picture"
d.text(((W - d.textlength(sub, font=f_sub)) / 2, y + 6), sub, font=f_sub, fill=GREY)
y += 40
y = rule(d, y, width=2)

# lead headline, two lines
f_lead = font(SERIF_B, 58)
l1 = "THREE LEADERS MEET"
l2 = "IN SHENZHEN"
d.text(((W - d.textlength(l1, font=f_lead)) / 2, y + 8), l1, font=f_lead, fill=INK)
y += 66
d.text(((W - d.textlength(l2, font=f_lead)) / 2, y), l2, font=f_lead, fill=RED)
y += 70
f_body = font(SERIF, 28)
y = draw_para(
    d, 40, y, 944,
    "Trump, Xi and Putin hold their first three-way talks on the sidelines of the "
    "APEC summit, issuing a joint declaration on nuclear risks and stable energy flows.",
    f_body, 35)
y += 8
y = rule(d, y, width=2)

# two-column row: Markets / Tech
f_kick = font(SANS_B, 24)
f_head = font(SERIF_B, 32)
f_small = font(SERIF, 26)
col_w = 452
y0 = y + 12
x = 40
d.text((x, y0), "MARKETS", font=f_kick, fill=RED)
y1 = draw_para(d, x, y0 + 32, col_w, "Anthropic soars on debut", f_head, 38)
y1 = draw_para(
    d, x, y1 + 2, col_w,
    "Shares close at $97.17, up 17% on the $83 IPO price, after opening 34% higher "
    "at $111.50. About $81.3bn raised; valuation near $1.5 trillion.",
    f_small, 33)
d.line([(512, y0), (512, y1)], fill=GREY, width=2)
x = 532
d.text((x, y0), "TECH", font=f_kick, fill=RED)
y2 = draw_para(d, x, y0 + 32, col_w, "Gemini gets computer use", f_head, 38)
y2 = draw_para(
    d, x, y2 + 2, col_w,
    "Google adds computer use to its Gemini Mac app \u2014 it can sort files, fill in "
    "forms and run multi-step tasks. Gemini 4 Neon, a mid-tier reasoning model, also ships.",
    f_small, 33)
y = max(y1, y2) + 8
y = rule(d, y, width=2)

# three-column row
col_w3 = 296
y0 = y + 12
cols = [
    ("THE GULF", "Tankers ablaze off Hormuz",
     "Three oil tankers catch fire after hitting mines east of the Strait of Hormuz, Iran says."),
    ("JUSTICE", "World court: Myanmar guilty",
     "The world court rules Myanmar committed genocide against the Rohingya."),
    ("UKRAINE", "Bridge hit again",
     "Ukraine strikes the Crimean Bridge for a third time in a week; Russian strikes "
     "kill five and cut power."),
]
ys = []
for i, (kick, head, body) in enumerate(cols):
    x = 40 + i * 328
    d.text((x, y0), kick, font=f_kick, fill=RED)
    yy = draw_para(d, x, y0 + 32, col_w3, head, f_head, 38)
    yy = draw_para(d, x, yy + 2, col_w3, body, f_small, 33)
    ys.append(yy)
    if i < 2:
        d.line([(40 + (i + 1) * 328 - 16, y0), (40 + (i + 1) * 328 - 16, yy)], fill=GREY, width=2)
y = max(ys) + 8
y = rule(d, y, width=2)

# also strip
f_also = font(SERIF_B, 25)
y = draw_para(
    d, 40, y + 10, 944,
    "ALSO \u2022 DeepSeek closes $105bn funding \u2022 COP31 enters final talks "
    "\u2022 Muse Charm at ~$300",
    f_also, 30)
y += 8
y = rule(d, y, width=2)

# footer
f_foot = font(SERIF_I, 24)
foot = "All stories from Thursday 19 November 2026"
d.text(((W - d.textlength(foot, font=f_foot)) / 2, y + 6), foot, font=f_foot, fill=GREY)

print("final y:", y)
img.save("/home/hatch/workspace/makefun-entries/news-image-20261119/entry.png")
print("saved", img.size)
