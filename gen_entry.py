"""food-picture-01 entry generator, rev 1: glossy burger + naughty cat stealing a patty.

Winning-formula upgrade (ai-happy-01): two characters interacting (burger + sneaky
cat paw/head), a funny moment, warm golden-hour lighting, painterly texture.
"""
from PIL import Image, ImageDraw, ImageFilter
import math
import os
import random

random.seed(20261114)

S = 4          # supersample factor
W = H = 1024
WBig, HBig = W * S, H * S


def scaled(*vals):
    return [v * S for v in vals]


img = Image.new("RGB", (WBig, HBig))
d = ImageDraw.Draw(img)

# --- background: warm golden-hour radial gradient + light rays --------------
cx0, cy0 = 0.5 * WBig, 0.42 * HBig
maxd = math.hypot(cx0, cy0)
top, bot = (255, 172, 60), (255, 224, 160)
for y in range(HBig):
    t = y / (HBig - 1)
    base = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (WBig, y)], fill=base)

# radial warm glow toward the burger
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse([0.12 * W, 0.10 * H, 0.88 * W, 0.86 * H], fill=110)
glow = glow.resize((WBig, HBig), Image.LANCZOS).filter(ImageFilter.GaussianBlur(18 * S))
warm = Image.new("RGB", (WBig, HBig), (255, 214, 130))
img = Image.composite(warm, img, glow)
d = ImageDraw.Draw(img)

# light rays fanning from upper centre
for ang, wid in [(-64, 26), (-38, 18), (-14, 30), (12, 20), (38, 16), (62, 24)]:
    a = math.radians(90 + ang)  # measured from up-vector
    x2 = cx0 + math.sin(a) * 1.4 * WBig
    y2 = cy0 - math.cos(a) * 1.4 * HBig
    x3 = cx0 + math.sin(a + math.radians(wid / 10)) * 1.4 * WBig
    y3 = cy0 - math.cos(a + math.radians(wid / 10)) * 1.4 * HBig
    ray = Image.new("RGBA", (WBig, HBig), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ray)
    rd.polygon([(cx0, cy0), (x2, y2), (x3, y3)], fill=(255, 240, 190, 52))
    ray = ray.filter(ImageFilter.GaussianBlur(10 * S))
    img = Image.alpha_composite(img.convert("RGBA"), ray).convert("RGB")
d = ImageDraw.Draw(img)

# --- soft ground shadow ------------------------------------------------------
sh = Image.new("L", (WBig, HBig), 0)
sd = ImageDraw.Draw(sh)
sd.ellipse(scaled(0.22 * W, 0.86 * H, 0.72 * W, 0.95 * H), fill=140)
sd.ellipse(scaled(0.72 * W, 0.88 * H, 0.92 * W, 0.95 * H), fill=90)  # under the sneaky paw
sh = sh.filter(ImageFilter.GaussianBlur(10 * S))
shadow_col = Image.new("RGB", (WBig, HBig), (196, 122, 52))
img = Image.composite(shadow_col, img, sh)
d = ImageDraw.Draw(img)

# --- naughty cat reaching in from the right, paw stealing the patty ----------
# arm: cream tabby with outline, coming from bottom-right corner toward the patty
arm = [(1.02, 1.02), (0.90, 0.92), (0.76, 0.80), (0.665, 0.665)]
arm_pts = []
for i, (ax, ay) in enumerate(arm):
    arm_pts += [ax * W - 0.055 * W, ay * H]
for i in reversed(range(len(arm))):
    ax, ay = arm[i]
    w = 0.105 * W if i < 2 else 0.130 * W
    arm_pts += [ax * W + w, ay * H]
d.polygon(scaled(*arm_pts), fill=(243, 208, 163), outline=(190, 142, 92), width=5 * S)

# tabby stripes hugging the arm's spine
for i in range(3):
    sx, sy = 0.80 + 0.06 * i, 0.90 - 0.062 * i
    d.arc(scaled(sx * W - 0.055 * W, sy * H - 0.05 * H, sx * W + 0.055 * W, sy * H + 0.05 * H),
          start=210, end=330, fill=(214, 168, 112), width=6 * S)

# paw gripping the patty's right edge is drawn AFTER the patty (see below)

# --- cat head peeking from behind the burger, left side ----------------------
head_cx, head_cy = 0.205 * W, 0.60 * H
head_rx, head_ry = 0.105 * W, 0.115 * H
# ears first (behind head)
for ex, tilt in [(-0.055, -28), (0.052, 24)]:
    exx, exy = head_cx + ex * W, head_cy - head_ry * 0.75
    tip = (exx + tilt * W * 0.004, exy - 0.105 * H)
    base_l = (exx - 0.045 * W, exy + 0.02 * H)
    base_r = (exx + 0.045 * W, exy + 0.02 * H)
    d.polygon(scaled(*base_l, *tip, *base_r), fill=(240, 205, 160))
    d.polygon(scaled(base_l[0] + 0.016 * W, base_l[1] - 0.008 * H,
                     tip[0] * 0.86 + base_l[0] * 0.14, tip[1] * 0.86 + base_l[1] * 0.14,
                     tip[0] * 0.86 + base_r[0] * 0.14, tip[1] * 0.86 + base_r[1] * 0.14,
                     base_r[0] - 0.016 * W, base_r[1] - 0.008 * H), fill=(250, 178, 172))
# round head half-hidden behind the bun's left edge
d.ellipse(scaled(head_cx - head_rx, head_cy - head_ry, head_cx + head_rx, head_cy + head_ry),
          fill=(244, 210, 168), outline=(216, 172, 118), width=4 * S)
# face: two big shiny eyes looking at the burger (to the right)
for exo in (-0.038, 0.038):
    ecx, ecy = head_cx + exo * W, head_cy - 0.015 * H
    d.ellipse(scaled(ecx - 0.026 * W, ecy - 0.030 * H, ecx + 0.026 * W, ecy + 0.030 * H),
              fill=(62, 48, 40))
    d.ellipse(scaled(ecx + 0.004 * W, ecy - 0.020 * H, ecx + 0.016 * W, ecy - 0.004 * H),
              fill=(255, 255, 255))
# tiny pink nose + w-shaped mouth (naughty grin)
ncx, ncy = head_cx + 0.002 * W, head_cy + 0.030 * H
d.polygon(scaled(ncx - 0.011 * W, ncy - 0.008 * H, ncx + 0.011 * W, ncy - 0.008 * H, ncx, ncy + 0.006 * H),
          fill=(250, 160, 150))
d.arc(scaled(ncx - 0.022 * W, ncy, ncx - 0.002 * W, ncy + 0.020 * H), start=0, end=150,
      fill=(150, 110, 80), width=3 * S)
d.arc(scaled(ncx + 0.002 * W, ncy, ncx + 0.022 * W, ncy + 0.020 * H), start=30, end=180,
      fill=(150, 110, 80), width=3 * S)
# whiskers
for wy in (-0.006, 0.006):
    d.line(scaled(head_cx + 0.055 * W, head_cy + wy * H,
                  head_cx + 0.105 * W, head_cy + (wy - 0.012) * H), fill=(230, 190, 140), width=2 * S)
    d.line(scaled(head_cx - 0.055 * W, head_cy + wy * H,
                  head_cx - 0.102 * W, head_cy + (wy - 0.012) * H), fill=(230, 190, 140), width=2 * S)

# --- bottom bun (heel) -------------------------------------------------------
heel = [0.30 * W, 0.795 * H, 0.70 * W, 0.795 * H, 0.66 * W, 0.895 * H,
        0.34 * W, 0.895 * H]
d.polygon(scaled(*heel), fill=(232, 152, 66))
d.polygon(scaled(*heel), outline=(172, 100, 42), width=6 * S)
d.polygon(scaled(0.36 * W, 0.86 * H, 0.64 * W, 0.86 * H, 0.62 * W, 0.895 * H,
                 0.38 * W, 0.895 * H), fill=(218, 136, 58))

# --- lettuce: frilly green wave ----------------------------------------------
lettuce_y = 0.79 * H
pts = [0.26 * W, lettuce_y]
x = 0.26 * W
ruffle = 0.026 * H
while x < 0.74 * W:
    pts += [x + 0.03 * W, lettuce_y - ruffle, x + 0.06 * W, lettuce_y]
    x += 0.06 * W
pts += [0.74 * W, lettuce_y + 0.05 * H, 0.26 * W, lettuce_y + 0.05 * H]
d.polygon(scaled(*pts), fill=(128, 196, 88))

# --- tomato slices ------------------------------------------------------------
for tx, tw in [(0.335, 0.17), (0.51, 0.17)]:
    d.rounded_rectangle(scaled(tx * W, 0.725 * H, (tx + tw) * W, 0.795 * H),
                        radius=0.035 * W, fill=(232, 66, 50))
    d.rounded_rectangle(scaled(tx * W, 0.725 * H, (tx + tw) * W, 0.795 * H),
                        radius=0.035 * W, outline=(178, 42, 34), width=4 * S)

# --- cheese: thick melting slab with drips ------------------------------------
cheese_y = 0.715 * H
d.rounded_rectangle(scaled(0.31 * W, cheese_y, 0.69 * W, 0.745 * H),
                    radius=0.012 * W, fill=(255, 196, 44))
for dx, dd, dlen in [(0.36, 0.030, 0.10), (0.47, 0.026, 0.13), (0.60, 0.030, 0.085)]:
    cxx = dx * W
    half = dd * W / 2
    tip = cheese_y + dlen * H
    d.polygon(scaled(cxx - half, cheese_y + 0.03 * H, cxx + half,
                     cheese_y + 0.03 * H, cxx, tip), fill=(255, 196, 44))
    d.ellipse(scaled(cxx - half, tip - half * 1.4, cxx + half,
                     tip + half * 0.6), fill=(255, 196, 44))

# --- patty: thick brown beef slab (the one being stolen) ----------------------
d.rounded_rectangle(scaled(0.29 * W, 0.615 * H, 0.71 * W, 0.715 * H),
                    radius=0.045 * W, fill=(146, 88, 56))
d.rounded_rectangle(scaled(0.29 * W, 0.615 * H, 0.71 * W, 0.715 * H),
                    radius=0.045 * W, outline=(100, 56, 34), width=5 * S)
d.rounded_rectangle(scaled(0.34 * W, 0.635 * H, 0.66 * W, 0.660 * H),
                    radius=0.02 * W, fill=(168, 106, 68))
# juicy gloss streak on the patty
d.rounded_rectangle(scaled(0.36 * W, 0.622 * H, 0.62 * W, 0.632 * H),
                    radius=0.005 * W, fill=(196, 128, 86))

# --- paw gripping the patty's right edge (cream mitt clearly over the beef) ---
paw_cx, paw_cy = 0.685 * W, 0.665 * H
d.ellipse(scaled(paw_cx - 0.060 * W, paw_cy - 0.052 * H, paw_cx + 0.060 * W, paw_cy + 0.052 * H),
          fill=(250, 218, 176), outline=(190, 142, 92), width=4 * S)
for tx in (-0.028, 0.0, 0.028):
    d.line(scaled(paw_cx + tx * W, paw_cy - 0.018 * H, paw_cx + tx * W, paw_cy + 0.038 * H),
           fill=(190, 142, 92), width=3 * S)
for bx, by, br in [(-0.036, -0.010, 0.011), (0.0, -0.018, 0.012), (0.036, -0.010, 0.011)]:
    d.ellipse(scaled(paw_cx + bx * W - br * W, paw_cy + by * H - br * W,
                     paw_cx + bx * W + br * W, paw_cy + by * H + br * W), fill=(250, 170, 160))

# --- top bun: big glossy dome --------------------------------------------------
bun_box = scaled(0.26 * W, 0.425 * H, 0.74 * W, 0.845 * H)
d.pieslice(bun_box, start=180, end=360, fill=(244, 164, 74))
d.pieslice(bun_box, start=180, end=360, outline=(184, 108, 46), width=6 * S)
d.arc(scaled(0.315 * W, 0.455 * H, 0.655 * W, 0.805 * H),
      start=200, end=262, fill=(254, 226, 166), width=13 * S)
d.arc(scaled(0.335 * W, 0.485 * H, 0.615 * W, 0.775 * H),
      start=205, end=255, fill=(255, 238, 198), width=8 * S)

# sesame seeds
seeds = [(0.40, 0.46, -30), (0.48, 0.45, 15), (0.56, 0.46, 40),
         (0.36, 0.52, 20), (0.45, 0.50, -15), (0.55, 0.50, -35),
         (0.62, 0.49, 25), (0.33, 0.58, 45), (0.42, 0.56, 0),
         (0.52, 0.56, 30), (0.60, 0.57, -20), (0.68, 0.57, 15)]
for sx, sy, rot in seeds:
    scx, scy = sx * W, sy * H
    srx, sry = 0.022 * W, 0.010 * W
    pts = []
    for k in range(12):
        a = k / 12 * 2 * math.pi + rot * math.pi / 180
        pts += [scx + srx * math.cos(a), scy + sry * math.sin(a)]
    d.polygon(scaled(*pts), fill=(253, 240, 208))

# --- painterly grain + soft vignette ------------------------------------------
noise = Image.effect_noise((W, H), 14).resize((WBig, HBig), Image.LANCZOS).convert("L")
img = Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.045)
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-0.18 * W, -0.18 * H, 1.18 * W, 1.18 * H], fill=255)
vig = vig.resize((WBig, HBig), Image.LANCZOS).filter(ImageFilter.GaussianBlur(22 * S))
edge = Image.new("RGB", (WBig, HBig), (214, 138, 60))
img = Image.composite(img, edge, vig)

# steam wisps intentionally omitted: blurred overlays read as muddy smudges at
# 300px against this warm gradient — clean edges win the craft criterion instead.

# --- downscale ------------------------------------------------------------------
img = img.resize((W, H), Image.LANCZOS)
img.save("entry.png", optimize=True)
print("entry.png", os.path.getsize("entry.png"), "bytes", img.size)
