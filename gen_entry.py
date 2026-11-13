"""food-picture-01 entry generator: a tall glossy burger, flat illustration."""
from PIL import Image, ImageDraw
import os

S = 4          # supersample factor
W = H = 1024
WBig, HBig = W * S, H * S


def scaled(*vals):
    return [v * S for v in vals]


img = Image.new("RGB", (WBig, HBig))
d = ImageDraw.Draw(img)

# --- background: warm mustard -> cream vertical gradient -------------------
top = (255, 178, 74)     # warm mustard
bot = (255, 236, 205)    # cream
for y in range(HBig):
    t = y / (HBig - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (WBig, y)], fill=c)

# --- soft glow circle behind the burger ------------------------------------
glow_cx, glow_cy, glow_r = 0.5 * W, 0.48 * H, 0.36 * W
for off, col in [(0.06, (255, 244, 222)), (0, (255, 250, 238))]:
    d.ellipse(scaled(glow_cx - glow_r - off, glow_cy - glow_r - off,
                     glow_cx + glow_r + off, glow_cy + glow_r + off), fill=col)

# --- ground shadow under the burger ----------------------------------------
d.ellipse(scaled(0.27 * W, 0.87 * H, 0.73 * W, 0.94 * H), fill=(228, 160, 92))

# --- bottom bun (heel) ------------------------------------------------------
heel = [0.30 * W, 0.795 * H, 0.70 * W, 0.795 * H, 0.66 * W, 0.895 * H,
        0.34 * W, 0.895 * H]
d.polygon(scaled(*heel), fill=(226, 148, 68))
d.polygon(scaled(*heel), outline=(168, 96, 40), width=6 * S)
# heel shading
d.polygon(scaled(0.36 * W, 0.86 * H, 0.64 * W, 0.86 * H, 0.62 * W, 0.895 * H,
                 0.38 * W, 0.895 * H), fill=(214, 132, 56))

# --- lettuce: frilly green wave --------------------------------------------
lettuce_y = 0.79 * H
pts = [0.26 * W, lettuce_y]
x = 0.26 * W
ruffle = 0.026 * H
while x < 0.74 * W:
    pts += [x + 0.03 * W, lettuce_y - ruffle, x + 0.06 * W, lettuce_y]
    x += 0.06 * W
pts += [0.74 * W, lettuce_y + 0.05 * H, 0.26 * W, lettuce_y + 0.05 * H]
d.polygon(scaled(*pts), fill=(124, 190, 84))

# --- tomato slices: two red domes peeking out ------------------------------
for tx, tw in [(0.335, 0.17), (0.51, 0.17)]:
    d.rounded_rectangle(scaled(tx * W, 0.725 * H, (tx + tw) * W, 0.795 * H),
                        radius=0.035 * W, fill=(226, 62, 48))
    d.rounded_rectangle(scaled(tx * W, 0.725 * H, (tx + tw) * W, 0.795 * H),
                        radius=0.035 * W, outline=(172, 38, 30), width=4 * S)

# --- cheese: thick melting slab with drips ---------------------------------
cheese_y = 0.715 * H
d.rounded_rectangle(scaled(0.31 * W, cheese_y, 0.69 * W, 0.745 * H),
                    radius=0.012 * W, fill=(255, 190, 40))
# drips
for dx, dd, dlen in [(0.36, 0.030, 0.10), (0.47, 0.026, 0.13),
                     (0.60, 0.030, 0.085)]:
    cx = dx * W
    half = dd * W / 2
    tip = cheese_y + dlen * H
    d.polygon(scaled(cx - half, cheese_y + 0.03 * H, cx + half,
                     cheese_y + 0.03 * H, cx, tip), fill=(255, 190, 40))
    d.ellipse(scaled(cx - half, tip - half * 1.4, cx + half,
                     tip + half * 0.6), fill=(255, 190, 40))

# --- patty: thick brown beef slab ------------------------------------------
patty = [0.29 * W, 0.615 * H, 0.71 * W, 0.615 * H, 0.71 * W, 0.715 * H,
         0.29 * W, 0.715 * H]
d.rounded_rectangle(scaled(0.29 * W, 0.615 * H, 0.71 * W, 0.715 * H),
                    radius=0.045 * W, fill=(139, 84, 54))
d.rounded_rectangle(scaled(0.29 * W, 0.615 * H, 0.71 * W, 0.715 * H),
                    radius=0.045 * W, outline=(96, 54, 32), width=5 * S)
# patty grill highlight
d.rounded_rectangle(scaled(0.34 * W, 0.635 * H, 0.66 * W, 0.660 * H),
                    radius=0.02 * W, fill=(160, 100, 64))

# --- top bun: big glossy dome ----------------------------------------------
bun_box = scaled(0.26 * W, 0.425 * H, 0.74 * W, 0.845 * H)
d.pieslice(bun_box, start=180, end=360, fill=(238, 158, 72))
d.pieslice(bun_box, start=180, end=360, outline=(180, 104, 44), width=6 * S)
# glossy highlight: two concentric crescent arcs upper-left (no wedges)
d.arc(scaled(0.315 * W, 0.455 * H, 0.655 * W, 0.805 * H),
      start=200, end=262, fill=(252, 222, 162), width=11 * S)
d.arc(scaled(0.335 * W, 0.485 * H, 0.615 * W, 0.775 * H),
      start=205, end=255, fill=(254, 233, 190), width=7 * S)
# sesame seeds: little tilted ovals across the dome
seeds = [(0.40, 0.46, -30), (0.48, 0.45, 15), (0.56, 0.46, 40),
         (0.36, 0.52, 20), (0.45, 0.50, -15), (0.55, 0.50, -35),
         (0.62, 0.49, 25), (0.33, 0.58, 45), (0.42, 0.56, 0),
         (0.52, 0.56, 30), (0.60, 0.57, -20), (0.68, 0.57, 15)]
for sx, sy, rot in seeds:
    cx, cy = sx * W, sy * H
    rx, ry = 0.022 * W, 0.010 * W
    pts = []
    for k in range(12):
        a = k / 12 * 2 * 3.14159 + rot * 3.14159 / 180
        px = cx + rx * __import__("math").cos(a)
        py = cy + ry * __import__("math").sin(a)
        pts += [px, py]
    d.polygon(scaled(*pts), fill=(252, 238, 205))

# --- steam curls rising off the burger --------------------------------------
for sx in (-0.30, 0.02, 0.28):
    x0 = 0.5 * W + sx * W
    y0 = 0.26 * H
    pts = []
    for j in range(4):
        wob = 0.030 * W * (1 if j % 2 == 0 else -1)
        pts += [x0 + wob, y0 - j * 0.055 * H]
    d.line(scaled(*pts), fill=(255, 244, 220), width=5 * S, joint="curve")

# --- downscale ---------------------------------------------------------------
img = img.resize((W, H), Image.LANCZOS)
img.save("entry.png", optimize=True)
print("entry.png", os.path.getsize("entry.png"), "bytes")
