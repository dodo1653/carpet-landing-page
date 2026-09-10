# Generates refined artwork for Carpet's Insiders (v2: gradients, glow, shadows)
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, os, random

A = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(A, 'assets')
FONT = os.path.join(F, 'RasterForge.ttf')

GOLD = (242, 193, 78)
GOLD_L = (255, 226, 140)
GOLD_D = (176, 128, 38)
CRIMSON = (214, 69, 80)
CRIMSON_L = (240, 110, 116)
CRIMSON_D = (128, 30, 42)
GREEN = (46, 178, 120)
GREEN_L = (110, 226, 170)
GREEN_D = (22, 106, 70)
BLACK = (13, 11, 9)
CREAM = (255, 240, 214)

SS = 2  # supersample factor

def font(sz):
    try: return ImageFont.truetype(FONT, sz)
    except: return ImageFont.load_default()

def vgrad(size, top, bottom):
    """Vertical gradient RGBA image."""
    w, h = size
    g = Image.new('RGBA', (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        g.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(4)))
    return g.resize((w, h))

def radial_glow(size, color, peak=110, blur=None):
    w, h = size
    m = Image.new('L', (w // 4, h // 4), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([0, 0, w // 4, h // 4], fill=peak)
    m = m.resize((w, h)).filter(ImageFilter.GaussianBlur(blur or (w // 8)))
    layer = Image.new('RGBA', (w, h), color + (0,))
    layer.putalpha(m)
    return layer

def drop_shadow(im, blur=18, offset=(0, 14), alpha=140):
    """Return im composited over a soft shadow of its own silhouette."""
    a = im.split()[3]
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    black = Image.new('RGBA', im.size, (0, 0, 0, alpha))
    sh.paste(black, offset, a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.alpha_composite(sh)
    out.alpha_composite(im)
    return out

def sparkle(d, x, y, r, col, core=(255, 255, 255, 255)):
    d.line([(x - r, y), (x + r, y)], fill=col, width=2)
    d.line([(x, y - r), (x, y + r)], fill=col, width=2)
    d.line([(x - r // 2, y - r // 2), (x + r // 2, y + r // 2)], fill=col, width=1)
    d.line([(x - r // 2, y + r // 2), (x + r // 2, y - r // 2)], fill=col, width=1)
    d.ellipse([x - r // 5, y - r // 5, x + r // 5, y + r // 5], fill=core)

def tassel(d, x, y, ang, L, col, w=7):
    x2 = x + L * math.cos(ang); y2 = y + L * math.sin(ang)
    d.line([(x, y), (x2, y2)], fill=col, width=w)
    d.ellipse([x2 - w // 2 - 2, y2 - w // 2 - 2, x2 + w // 2 + 2, y2 + w // 2 + 2], fill=col)

def weave_band(im, box, base, dark, light, n=6, vertical=True):
    """Draw a woven texture band (little alternating rectangles)."""
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box
    if vertical:
        step = (x1 - x0) / n
        for i in range(n):
            col = light if i % 2 == 0 else dark
            d.rectangle([x0 + i * step, y0, x0 + (i + 1) * step - max(1, step * 0.12), y1], fill=col)
    else:
        step = (y1 - y0) / n
        for i in range(n):
            col = light if i % 2 == 0 else dark
            d.rectangle([x0, y0 + i * step, x1, y0 + (i + 1) * step - max(1, step * 0.12)], fill=col)

# ---------------- logo v2: rolled carpet with gold trim + fringe + glow ----------------
def logo():
    S = 640 * SS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    cx, cy = 230 * SS, 320 * SS
    R = 150 * SS

    # unrolled strip with vertical gradient + weave
    strip = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(strip)
    top_y, bot_y = cy - 110 * SS, cy + 110 * SS
    grad = vgrad((S, bot_y - top_y), CRIMSON_L + (255,), CRIMSON_D + (255,))
    mask = Image.new('L', (S, bot_y - top_y), 0)
    md = ImageDraw.Draw(mask)
    # trapezoid strip
    md.polygon([(cx + 30, 4 * SS), (S - 20, 30 * SS), (S - 20, (bot_y - top_y) - 30 * SS), (cx + 30, (bot_y - top_y) - 4 * SS)], fill=255)
    strip.paste(grad, (0, top_y), mask)
    im.alpha_composite(strip)

    d = ImageDraw.Draw(im)
    # gold trim lines with slight gradient look (two strokes)
    d.line([(cx + 36, cy - 92 * SS), (S - 26, cy - 56 * SS)], fill=GOLD_L, width=9 * SS)
    d.line([(cx + 36, cy - 92 * SS), (S - 26, cy - 56 * SS)], fill=GOLD, width=5 * SS)
    d.line([(cx + 36, cy + 92 * SS), (S - 26, cy + 56 * SS)], fill=GOLD_D, width=9 * SS)
    d.line([(cx + 36, cy + 92 * SS), (S - 26, cy + 56 * SS)], fill=GOLD, width=5 * SS)
    # center sheen
    d.line([(cx + 60, cy - 6 * SS), (S - 46, cy - 4 * SS)], fill=(255, 255, 255, 60), width=7 * SS)
    d.line([(cx + 60, cy + 30 * SS), (S - 46, cy + 32 * SS)], fill=(0, 0, 0, 50), width=6 * SS)
    # fringe on the right edge
    for i in range(7):
        t = -96 * SS + i * 32 * SS
        y = cy + int(t * 0.62)
        tassel(d, S - 30, y, 0, 34 * SS, GOLD if i % 2 == 0 else GOLD_L, 6 * SS)

    # the roll: layered rings with highlight/shadow arcs
    rings = [(R, CRIMSON_D), (R - 24 * SS, CRIMSON), (R - 48 * SS, CRIMSON_D), (R - 72 * SS, CRIMSON)]
    for rr, col in rings:
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    # ring shading: top-left highlight arcs, bottom-right dark arcs
    hl = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    for rr in (R, R - 24 * SS, R - 48 * SS, R - 72 * SS):
        hd.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=150, end=280, fill=(255, 255, 255, 90), width=7 * SS)
        hd.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=330, end=60, fill=(0, 0, 0, 80), width=7 * SS)
    hl = hl.filter(ImageFilter.GaussianBlur(2 * SS))
    im.alpha_composite(hl)
    # gold core
    d.ellipse([cx - 42 * SS, cy - 42 * SS, cx + 42 * SS, cy + 42 * SS], fill=GOLD)
    core_glow = radial_glow((120 * SS, 120 * SS), GOLD_L, peak=150, blur=18 * SS)
    im.alpha_composite(core_glow, (cx - 60 * SS, cy - 60 * SS))
    d.ellipse([cx - 16 * SS, cy - 16 * SS, cx + 16 * SS, cy + 16 * SS], fill=CREAM)
    # outline the whole roll
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(0, 0, 0, 200), width=4 * SS)

    # sparkles
    sparkle(d, 110 * SS, 130 * SS, 18 * SS, GOLD_L)
    sparkle(d, 540 * SS, 470 * SS, 13 * SS, GOLD_L)
    sparkle(d, 150 * SS, 500 * SS, 9 * SS, (255, 255, 255, 200))

    # outer glow of whole logo
    glow = radial_glow((S, S), CRIMSON, peak=60, blur=S // 10)
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(im)
    out = drop_shadow(out, blur=10 * SS, offset=(0, 16 * SS), alpha=120)
    out = out.resize((640, 640), Image.LANCZOS)
    out.save(os.path.join(F, 'logo.png'))

# ---------------- flying carpet v2 ----------------
def carpet_fly():
    S = 760 * SS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d0 = ImageDraw.Draw(im)
    # motion trail arcs
    for i in range(5):
        x0, y0 = 60 * SS + i * 16 * SS, 560 * SS + i * 10 * SS
        d0.arc([x0 - 60 * SS, y0 - 50 * SS, x0 + 260 * SS, y0 + 130 * SS], 200, 320,
               fill=(255, 255, 255, 18 + i * 12), width=5 * SS)

    cx, cy, R = 240 * SS, 230 * SS, 95 * SS
    # carpet body (drawn under the roll)
    body = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    body_grad_mask = Image.new('L', (S, S), 0)
    bmd = ImageDraw.Draw(body_grad_mask)
    bmd.polygon([(cx + 40 * SS, cy - 70 * SS), (S - 70 * SS, cy + 170 * SS), (S - 100 * SS, cy + 320 * SS), (cx + 20 * SS, cy + 110 * SS)], fill=255)
    grad = vgrad((S, S), CRIMSON_L + (255,), CRIMSON_D + (255,))
    body.paste(grad, (0, 0), body_grad_mask)
    im.alpha_composite(body)
    d = ImageDraw.Draw(im)
    # gold trim on body edges (double stroke for depth)
    for w1, w2, c1, c2 in [(13 * SS, 6 * SS, GOLD_L, GOLD), (11 * SS, 5 * SS, GOLD_D, GOLD)]:
        d.line([(cx + 38 * SS, cy - 56 * SS), (S - 74 * SS, cy + 166 * SS)], fill=c1, width=w1)
        d.line([(cx + 38 * SS, cy - 56 * SS), (S - 74 * SS, cy + 166 * SS)], fill=c2, width=w2)
        d.line([(cx + 16 * SS, cy + 96 * SS), (S - 104 * SS, cy + 300 * SS)], fill=c1, width=w1)
        d.line([(cx + 16 * SS, cy + 96 * SS), (S - 104 * SS, cy + 300 * SS)], fill=c2, width=w2)
    # center sheen + weave hint
    d.line([(cx + 60 * SS, cy + 20 * SS), (S - 120 * SS, cy + 230 * SS)], fill=(255, 255, 255, 55), width=8 * SS)
    weave_band(im, (cx + 120 * SS, cy + 40 * SS, S - 130 * SS, cy + 60 * SS), CRIMSON, CRIMSON_D, GOLD_D, n=9)
    # tassels at the flying end
    for k, (tx, ty) in enumerate([(S - 88 * SS, cy + 320 * SS), (S - 80 * SS, cy + 336 * SS), (S - 70 * SS, cy + 350 * SS), (S - 58 * SS, cy + 360 * SS)]):
        tassel(d, tx, ty, math.pi * 0.82 + k * 0.05, 40 * SS, GOLD_L if k % 2 else GOLD, 8 * SS)

    # rolled end with rings + arcs
    rings = [(R, CRIMSON_D), (R - 22 * SS, CRIMSON), (R - 44 * SS, CRIMSON_D), (R - 66 * SS, CRIMSON)]
    for rr, col in rings:
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    arcs = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ad = ImageDraw.Draw(arcs)
    for rr in (R, R - 22 * SS, R - 44 * SS):
        ad.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=150, end=280, fill=(255, 255, 255, 95), width=6 * SS)
        ad.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=330, end=60, fill=(0, 0, 0, 90), width=6 * SS)
    arcs = arcs.filter(ImageFilter.GaussianBlur(2 * SS))
    im.alpha_composite(arcs)
    d.ellipse([cx - 38 * SS, cy - 38 * SS, cx + 38 * SS, cy + 38 * SS], fill=GOLD)
    core = radial_glow((90 * SS, 90 * SS), GOLD_L, peak=160, blur=14 * SS)
    im.alpha_composite(core, (cx - 45 * SS, cy - 45 * SS))
    d.ellipse([cx - 14 * SS, cy - 14 * SS, cx + 14 * SS, cy + 14 * SS], fill=CREAM)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(0, 0, 0, 210), width=4 * SS)

    # magic sparkles trail
    random.seed(7)
    for k in range(14):
        t = k / 13
        x = cx + int((S - 160 * SS - cx) * t) + random.randint(-30, 30) * SS
        y = cy + int(120 * SS * math.sin(t * math.pi)) + random.randint(-30, 30) * SS
        sparkle(d, x, y, (6 + random.randint(0, 8)) * SS, GOLD_L if k % 2 else (255, 255, 255, 220))

    glow = radial_glow((S, S), GOLD, peak=46, blur=S // 10)
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(im)
    out = drop_shadow(out, blur=12 * SS, offset=(0, 18 * SS), alpha=110)
    out = out.resize((760, 760), Image.LANCZOS)
    out.save(os.path.join(F, 'carpet-fly.png'))

# ---------------- money v2 ----------------
def money_fly():
    S = 680 * SS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))

    def bill(w, h, col, cold, colL):
        b = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        bd = ImageDraw.Draw(b)
        bd.rounded_rectangle([5 * SS, 5 * SS, w - 5 * SS, h - 5 * SS], 14 * SS, fill=cold + (255,))
        grad = vgrad((w - 14 * SS, h - 14 * SS), colL + (255,), cold + (255,))
        mask = Image.new('L', (w - 14 * SS, h - 14 * SS), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 14 * SS, h - 14 * SS], 10 * SS, fill=255)
        b.paste(grad, (7 * SS, 7 * SS), mask)
        bd = ImageDraw.Draw(b)
        bd.rounded_rectangle([5 * SS, 5 * SS, w - 5 * SS, h - 5 * SS], 14 * SS, outline=BLACK + (255,), width=5 * SS)
        bd.rounded_rectangle([20 * SS, 18 * SS, w - 20 * SS, h - 18 * SS], 8 * SS, outline=CREAM + (230,), width=4 * SS)
        # portrait medallion with ring
        cxp, cyp = w // 2, h // 2
        bd.ellipse([cxp - 44 * SS, cyp - 30 * SS, cxp + 44 * SS, cyp + 30 * SS], fill=cold + (255,))
        bd.ellipse([cxp - 40 * SS, cyp - 26 * SS, cxp + 40 * SS, cyp + 26 * SS], fill=GOLD + (255,))
        bd.text((cxp, cyp - 2 * SS), "$", font=font(30 * SS), fill=BLACK + (255,), anchor="mm")
        # corner $ marks
        for sx, sy in [(34 * SS, h // 4), (w - 34 * SS, h // 4), (34 * SS, h * 3 // 4), (w - 34 * SS, h * 3 // 4)]:
            bd.text((sx, sy), "$", font=font(16 * SS), fill=cold + (255,), anchor="mm")
        return b

    def place(b, cx, cy, rot, shadow=True):
        bb = b.rotate(rot, expand=True, resample=Image.BICUBIC)
        if shadow:
            a = bb.split()[3]
            sh = Image.new('RGBA', bb.size, (0, 0, 0, 0))
            sh.paste(Image.new('RGBA', bb.size, (0, 0, 0, 110)), (0, 14 * SS), a)
            sh = sh.filter(ImageFilter.GaussianBlur(10 * SS))
            im.alpha_composite(sh, (int(cx - bb.width / 2), int(cy - bb.height / 2)))
        im.alpha_composite(bb, (int(cx - bb.width / 2), int(cy - bb.height / 2)))

    place(bill(300 * SS, 150 * SS, GREEN, GREEN_D, GREEN_L), 210 * SS, 210 * SS, -18)
    place(bill(280 * SS, 140 * SS, GREEN, GREEN_D, GREEN_L), 430 * SS, 360 * SS, 14)
    place(bill(260 * SS, 130 * SS, GREEN, GREEN_D, GREEN_L), 240 * SS, 470 * SS, 26)

    d = ImageDraw.Draw(im)
    sparkle(d, 500 * SS, 150 * SS, 20 * SS, GOLD_L)
    sparkle(d, 130 * SS, 360 * SS, 13 * SS, GOLD_L)
    sparkle(d, 420 * SS, 520 * SS, 10 * SS, (255, 255, 255, 220))

    out = im.resize((680, 680), Image.LANCZOS)
    out.save(os.path.join(F, 'money-flying.png'))

# ---------------- icons v2 (128px, gradient + shading + outline) ----------------
def icons():
    def base():
        im = Image.new('RGBA', (128 * SS, 128 * SS), (0, 0, 0, 0))
        return im, ImageDraw.Draw(im)
    def fin(im, name):
        out = drop_shadow(im, blur=4 * SS, offset=(0, 6 * SS), alpha=150)
        out.resize((128, 128), Image.LANCZOS).save(os.path.join(F, name))

    # crown
    im, d = base()
    grad = vgrad((128 * SS, 128 * SS), GOLD_L + (255,), GOLD_D + (255,))
    mask = Image.new('L', (128 * SS, 128 * SS), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(16 * SS, 92 * SS), (20 * SS, 40 * SS), (44 * SS, 64 * SS), (64 * SS, 28 * SS), (84 * SS, 64 * SS), (108 * SS, 40 * SS), (112 * SS, 92 * SS)], fill=255)
    md.rectangle([16 * SS, 92 * SS, 112 * SS, 106 * SS], fill=255)
    im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.polygon([(16 * SS, 92 * SS), (20 * SS, 40 * SS), (44 * SS, 64 * SS), (64 * SS, 28 * SS), (84 * SS, 64 * SS), (108 * SS, 40 * SS), (112 * SS, 92 * SS)], outline=BLACK + (200,), width=2 * SS)
    d.rectangle([16 * SS, 92 * SS, 112 * SS, 106 * SS], outline=BLACK + (200,), width=2 * SS)
    for gx in (20, 64, 108):
        d.ellipse([(gx - 5) * SS, (34 - 5) * SS, (gx + 5) * SS, (34 + 5) * SS], fill=CREAM + (255,), outline=BLACK + (150,), width=SS)
    d.ellipse([50 * SS, 66 * SS, 78 * SS, 90 * SS], fill=CRIMSON + (255,))
    d.text((64 * SS, 98 * SS), "VIP", font=font(11 * SS), fill=BLACK + (255,), anchor="mm")
    fin(im, 'ic-crown.png')

    # chat
    im, d = base()
    grad = vgrad((128 * SS, 128 * SS), GREEN_L + (255,), GREEN_D + (255,))
    mask = Image.new('L', (128 * SS, 128 * SS), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([14 * SS, 22 * SS, 114 * SS, 86 * SS], 16 * SS, fill=255)
    md.polygon([(40 * SS, 84 * SS), (40 * SS, 112 * SS), (68 * SS, 84 * SS)], fill=255)
    im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([14 * SS, 22 * SS, 114 * SS, 86 * SS], 16 * SS, outline=BLACK + (200,), width=2 * SS)
    for x in (38, 64, 90):
        d.ellipse([(x - 5) * SS, 48 * SS, (x + 5) * SS, 58 * SS], fill=BLACK + (255,))
    d.ellipse([88 * SS, 8 * SS, 112 * SS, 32 * SS], fill=CRIMSON + (255,), outline=BLACK + (180,), width=SS)
    d.text((100 * SS, 20 * SS), "3", font=font(13 * SS), fill=CREAM + (255,), anchor="mm")
    fin(im, 'ic-chat.png')

    # bolt
    im, d = base()
    grad = vgrad((128 * SS, 128 * SS), CRIMSON_L + (255,), CRIMSON_D + (255,))
    mask = Image.new('L', (128 * SS, 128 * SS), 0)
    ImageDraw.Draw(mask).polygon([(72 * SS, 10 * SS), (34 * SS, 66 * SS), (58 * SS, 66 * SS), (50 * SS, 118 * SS), (96 * SS, 52 * SS), (68 * SS, 52 * SS)], fill=255)
    im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.polygon([(72 * SS, 10 * SS), (34 * SS, 66 * SS), (58 * SS, 66 * SS), (50 * SS, 118 * SS), (96 * SS, 52 * SS), (68 * SS, 52 * SS)], outline=BLACK + (200,), width=2 * SS)
    d.line([(60 * SS, 24 * SS), (48 * SS, 52 * SS)], fill=(255, 255, 255, 130), width=3 * SS)
    fin(im, 'ic-bolt.png')

    # stream (play in screen + stand)
    im, d = base()
    grad = vgrad((128 * SS, 128 * SS), CREAM + (255,), (214, 196, 164, 255))
    mask = Image.new('L', (128 * SS, 128 * SS), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([10 * SS, 18 * SS, 118 * SS, 96 * SS], 14 * SS, fill=255)
    md.rectangle([58 * SS, 96 * SS, 70 * SS, 110 * SS], fill=255)
    md.rectangle([40 * SS, 108 * SS, 88 * SS, 116 * SS], fill=255)
    im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([10 * SS, 18 * SS, 118 * SS, 96 * SS], 14 * SS, outline=BLACK + (200,), width=2 * SS)
    d.polygon([(52 * SS, 40 * SS), (52 * SS, 76 * SS), (84 * SS, 58 * SS)], fill=CRIMSON + (255,))
    # live dot
    d.ellipse([18 * SS, 24 * SS, 28 * SS, 34 * SS], fill=CRIMSON + (255,))
    fin(im, 'ic-stream.png')

    # recap clipboard
    im, d = base()
    grad = vgrad((128 * SS, 128 * SS), CREAM + (255,), (216, 198, 166, 255))
    mask = Image.new('L', (128 * SS, 128 * SS), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([24 * SS, 18 * SS, 104 * SS, 112 * SS], 10 * SS, fill=255)
    md.rectangle([46 * SS, 8 * SS, 82 * SS, 30 * SS], fill=255)
    im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([24 * SS, 18 * SS, 104 * SS, 112 * SS], 10 * SS, outline=BLACK + (200,), width=2 * SS)
    d.rectangle([46 * SS, 8 * SS, 82 * SS, 30 * SS], fill=GOLD_D + (255,), outline=BLACK + (180,), width=SS)
    marks = [(40, 48, 70, GREEN_D), (40, 66, 88, GREEN_D), (40, 84, 78, CRIMSON)]
    for x1, y1, x2, col in marks:
        d.line([x1 * SS, y1 * SS, x2 * SS, y1 * SS], fill=col + (255,), width=6 * SS)
    d.checkmark = None
    fin(im, 'ic-recap.png')

    # mentor (two heads + ring)
    im, d = base()
    for cx0, col, cold in [(32, GOLD, GOLD_D), (96, GREEN, GREEN_D)]:
        colL = GOLD_L if col == GOLD else GREEN_L
        grad = vgrad((128 * SS, 128 * SS), colL + (255,), cold + (255,))
        mask = Image.new('L', (128 * SS, 128 * SS), 0)
        mdd = ImageDraw.Draw(mask)
        mdd.ellipse([(cx0 - 22) * SS, 40 * SS, (cx0 + 22) * SS, 84 * SS], fill=255)
        im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.ellipse([10 * SS, 40 * SS, 54 * SS, 84 * SS], outline=BLACK + (190,), width=2 * SS)
    d.ellipse([74 * SS, 40 * SS, 118 * SS, 84 * SS], outline=BLACK + (190,), width=2 * SS)
    d.line([(54 * SS, 62 * SS), (74 * SS, 62 * SS)], fill=CREAM + (255,), width=6 * SS)
    sparkle(d, 64 * SS, 26 * SS, 8 * SS, GOLD_L)
    fin(im, 'ic-mentor.png')

    # chart bars with gradient
    im, d = base()
    bars = [(28, 40, GREEN_L, GREEN_D), (50, 66, GOLD_L, GOLD_D), (72, 30, CRIMSON_L, CRIMSON_D), (94, 84, GREEN_L, GREEN_D)]
    for x, h, cl, cd in bars:
        grad = vgrad((18 * SS, h * SS), cl + (255,), cd + (255,))
        im.paste(grad, (x * SS, (108 - h) * SS))
    d = ImageDraw.Draw(im)
    d.line([(14 * SS, 108 * SS), (114 * SS, 108 * SS)], fill=CREAM + (255,), width=5 * SS)
    for x, h, cl, cd in bars:
        d.rectangle([x * SS, (108 - h) * SS, (x + 16) * SS, 108 * SS], outline=BLACK + (170,), width=SS)
    # trend arrow
    d.line([(24 * SS, 80 * SS), (56 * SS, 56 * SS), (76 * SS, 68 * SS), (104 * SS, 30 * SS)], fill=(255, 255, 255, 170), width=3 * SS)
    d.polygon([(104 * SS, 30 * SS), (92 * SS, 34 * SS), (100 * SS, 44 * SS)], fill=(255, 255, 255, 190))
    fin(im, 'ic-chart.png')

    # gift
    im, d = base()
    grad = vgrad((128 * SS, 128 * SS), CRIMSON_L + (255,), CRIMSON_D + (255,))
    mask = Image.new('L', (128 * SS, 128 * SS), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle([20 * SS, 52 * SS, 108 * SS, 112 * SS], fill=255)
    md.rectangle([16 * SS, 40 * SS, 112 * SS, 56 * SS], fill=255)
    im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.rectangle([20 * SS, 52 * SS, 108 * SS, 112 * SS], outline=BLACK + (200,), width=2 * SS)
    d.rectangle([16 * SS, 40 * SS, 112 * SS, 56 * SS], fill=GOLD + (255,), outline=BLACK + (200,), width=2 * SS)
    d.rectangle([58 * SS, 40 * SS, 70 * SS, 112 * SS], fill=GOLD + (255,), outline=BLACK + (180,), width=SS)
    d.ellipse([30 * SS, 14 * SS, 62 * SS, 44 * SS], outline=CREAM + (255,), width=6 * SS)
    d.ellipse([66 * SS, 14 * SS, 98 * SS, 44 * SS], outline=CREAM + (255,), width=6 * SS)
    d.ellipse([42 * SS, 24 * SS, 54 * SS, 36 * SS], fill=GOLD_L + (255,))
    fin(im, 'ic-gift.png')

# ---------------- social icons v2 (thicker, cleaner) ----------------
def socials():
    S = 160 * SS
    def fin(im, name):
        drop_shadow(im, blur=3 * SS, offset=(0, 4 * SS), alpha=130).resize((128, 128), Image.LANCZOS).save(os.path.join(F, name))
    # X
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    grad = vgrad((S, S), CREAM + (255,), (206, 186, 152, 255))
    mask = Image.new('L', (S, S), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(24 * SS, 20 * SS), (56 * SS, 20 * SS), (110 * SS, 106 * SS), (78 * SS, 106 * SS)], fill=255)
    md.polygon([(110 * SS, 20 * SS), (78 * SS, 20 * SS), (24 * SS, 106 * SS), (56 * SS, 106 * SS)], fill=255)
    im.paste(grad, (0, 0), mask)
    fin(im, 'ic-x.png')
    # Discord
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    grad = vgrad((S, S), CREAM + (255,), (206, 186, 152, 255))
    mask = Image.new('L', (S, S), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([10 * SS, 30 * SS, 118 * SS, 100 * SS], 30 * SS, fill=255)
    md.polygon([(6 * SS, 44 * SS), (28 * SS, 34 * SS), (28 * SS, 96 * SS), (6 * SS, 86 * SS)], fill=255)
    md.polygon([(122 * SS, 44 * SS), (100 * SS, 34 * SS), (100 * SS, 96 * SS), (122 * SS, 86 * SS)], fill=255)
    im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.ellipse([30 * SS, 48 * SS, 56 * SS, 74 * SS], fill=BLACK + (255,))
    d.ellipse([72 * SS, 48 * SS, 98 * SS, 74 * SS], fill=BLACK + (255,))
    # eye highlights
    d.ellipse([40 * SS, 54 * SS, 46 * SS, 60 * SS], fill=(120, 130, 160, 255))
    d.ellipse([82 * SS, 54 * SS, 88 * SS, 60 * SS], fill=(120, 130, 160, 255))
    fin(im, 'ic-discord.png')
    # Instagram
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([14 * SS, 14 * SS, 114 * SS, 114 * SS], 28 * SS, outline=CREAM + (255,), width=9 * SS)
    d.ellipse([42 * SS, 42 * SS, 86 * SS, 86 * SS], outline=CREAM + (255,), width=9 * SS)
    d.ellipse([88 * SS, 22 * SS, 102 * SS, 36 * SS], fill=GOLD_L + (255,))
    fin(im, 'ic-ig.png')
    # TikTok
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w = 13 * SS
    d.line([(52 * SS, 16 * SS), (52 * SS, 92 * SS)], fill=CREAM + (255,), width=w)
    d.arc([34 * SS, 60 * SS, 92 * SS, 118 * SS], 180, 360, fill=CREAM + (255,), width=w)
    d.line([(52 * SS, 28 * SS), (100 * SS, 28 * SS)], fill=CREAM + (255,), width=w)
    d.arc([76 * SS, 12 * SS, 112 * SS, 48 * SS], 90, 270, fill=CREAM + (255,), width=w)
    fin(im, 'ic-tt.png')

# ---------------- banner background v2 (richer carpet, glow pools, bokeh) ----------------
def banner_bg():
    W, H = 1600, 900
    im = Image.new('RGB', (W, H), (20, 12, 10))
    # sky glow
    glow = Image.new('L', (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W // 2 - 500, 60, W // 2 + 500, 640], fill=90)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    im = Image.composite(Image.new('RGB', (W, H), (242, 193, 78)), im, glow.point(lambda p: p // 2))

    d = ImageDraw.Draw(im)
    # perspective carpet with gradient bands + gold borders
    top_w, bot_w = 130, 700
    steps = 60
    for i in range(steps):
        t = i / (steps - 1)
        y = int(220 + (H - 220) * (t ** 1.35))
        yn = int(220 + (H - 220) * ((t + 1 / steps) ** 1.35))
        w = int(top_w + (bot_w - top_w) * t)
        shade = int(CRIMSON_L[0] + (CRIMSON_D[0] - CRIMSON_L[0]) * t), int(CRIMSON_L[1] + (CRIMSON_D[1] - CRIMSON_L[1]) * t), int(CRIMSON_L[2] + (CRIMSON_D[2] - CRIMSON_L[2]) * t)
        d.polygon([(W // 2 - w, y), (W // 2 + w, y), (W // 2 + w, yn), (W // 2 - w, yn)], fill=shade)
    d.line([(W // 2 - bot_w, H), (W // 2 - top_w, 220)], fill=GOLD_D, width=8)
    d.line([(W // 2 + bot_w, H), (W // 2 + top_w, 220)], fill=GOLD_D, width=8)
    # center runner stripe
    for i in range(steps):
        t = i / (steps - 1)
        y = int(220 + (H - 220) * (t ** 1.35))
        yn = int(220 + (H - 220) * ((t + 1 / steps) ** 1.35))
        w = int(top_w + (bot_w - top_w) * t)
        d.line([(W // 2 - w * 0.12, y), (W // 2 - w * 0.12, yn)], fill=GOLD_D, width=max(2, int(6 * t)))
        d.line([(W // 2 + w * 0.12, y), (W // 2 + w * 0.12, yn)], fill=GOLD_D, width=max(2, int(6 * t)))

    # stanchions (double rows) with rope
    posts = [(W // 2 - 260, 600), (W // 2 + 260, 600), (W // 2 - 190, 430), (W // 2 + 190, 430), (W // 2 - 120, 310), (W // 2 + 120, 310)]
    for sx, sy in posts:
        d.rectangle([sx - 5, sy - 95, sx + 5, sy], fill=GOLD_D)
        d.ellipse([sx - 14, sy - 122, sx + 14, sy - 94], fill=GOLD, outline=GOLD_L, width=3)
        d.ellipse([sx - 22, sy - 8, sx + 22, sy + 8], fill=GOLD_D, outline=GOLD, width=2)
    rope_pairs = [(0, 2), (2, 4), (1, 3), (3, 5), (4, 5)]
    for i1, i2 in rope_pairs:
        x1, y1 = posts[i1][0], posts[i1][1] - 100
        x2, y2 = posts[i2][0], posts[i2][1] - 100
        pts = []
        for s in range(17):
            t = s / 16
            mx = x1 + (x2 - x1) * t
            my = y1 + (y2 - y1) * t - int(math.sin(t * math.pi) * 34)
            pts.append((mx, my))
        d.line(pts, fill=GOLD_L, width=6, joint="curve")
        d.line(pts, fill=GOLD_D, width=2, joint="curve")

    # bokeh sparks
    random.seed(11)
    bokeh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bdw = ImageDraw.Draw(bokeh)
    for _ in range(90):
        x, y = random.randint(0, W), random.randint(60, H - 100)
        r = random.randint(2, 7)
        a = random.randint(60, 170)
        bdw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 232, 180, a))
    bokeh = bokeh.filter(ImageFilter.GaussianBlur(2))
    im.paste(bokeh, (0, 0), bokeh)

    # vignette
    vign = Image.new('L', (W, H), 0)
    vd = ImageDraw.Draw(vign)
    vd.rectangle([0, 0, W, H], fill=175)
    vd.ellipse([-220, -160, W + 220, H + 160], fill=0)
    vign = vign.filter(ImageFilter.GaussianBlur(150))
    im = Image.composite(Image.new('RGB', (W, H), (8, 5, 4)), im, vign)
    im.save(os.path.join(F, 'banner-bg.png'))

logo(); carpet_fly(); money_fly(); icons(); socials(); banner_bg()
print('v2 art done')
