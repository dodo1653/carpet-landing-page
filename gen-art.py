# Generates all artwork for Carpet's Insiders (red-carpet luxury theme)
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, os

A = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(A, 'assets')
os.makedirs(F, exist_ok=True)
FONT = os.path.join(F, 'RasterForge.ttf')

GOLD = (242, 193, 78)
GOLD_D = (196, 148, 44)
CRIMSON = (214, 69, 80)
CRIMSON_D = (150, 40, 52)
GREEN = (46, 201, 143)
GREEN_D = (24, 130, 92)
BLACK = (13, 11, 9)
CREAM = (255, 240, 214)

def font(sz):
    try: return ImageFont.truetype(FONT, sz)
    except: return ImageFont.load_default()

def sparkle(d, x, y, r, col):
    d.line([(x - r, y), (x + r, y)], fill=col, width=2)
    d.line([(x, y - r), (x, y + r)], fill=col, width=2)
    d.line([(x - r//2, y - r//2), (x + r//2, y + r//2)], fill=col, width=1)
    d.line([(x - r//2, y + r//2), (x + r//2, y - r//2)], fill=col, width=1)

# ---------------- logo: rolled red carpet with gold trim ----------------
def logo():
    S = 640
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 240, 320          # roll center
    R = 150
    # unrolled carpet: a red strip going right, slight perspective
    d.polygon([(cx + 20, cy - 110), (S - 30, cy - 70), (S - 30, cy + 70), (cx + 20, cy + 110)], fill=CRIMSON + (255,))
    # gold stripes along the carpet edges
    d.line([(cx + 30, cy - 96), (S - 36, cy - 60)], fill=GOLD + (255,), width=14)
    d.line([(cx + 30, cy + 96), (S - 36, cy + 60)], fill=GOLD + (255,), width=14)
    d.line([(cx + 40, cy), (S - 40, cy)], fill=(255, 255, 255, 40), width=6)
    # the roll: concentric circles
    for rr, col in [(R, CRIMSON_D), (R - 26, CRIMSON), (R - 52, CRIMSON_D), (R - 78, CRIMSON), (40, GOLD)]:
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col + (255,))
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=CREAM + (255,))
    # fringe
    for i in range(7):
        x = S - 44
        y = -80 + i * 27
        yy = cy + int(y * 0.62)
        d.line([(x, yy), (S - 8, yy)], fill=GOLD + (255,), width=6)
    # sparkles
    sparkle(d, 120, 130, 16, GOLD + (255,))
    sparkle(d, 520, 480, 12, GOLD + (255,))
    im.save(os.path.join(F, 'logo.png'))

# ---------------- hero floating art: flying golden carpet ----------------
def carpet_fly():
    S = 720
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # motion trail
    for i in range(4):
        x0, y0 = 80 + i * 18, 520 + i * 10
        d.arc([x0 - 60, y0 - 40, x0 + 220, y0 + 120], 200, 320, fill=(255, 255, 255, 26 + i * 14), width=5)
    # rolled end (top-left)
    cx, cy, R = 220, 220, 92
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=CRIMSON_D + (255,))
    d.ellipse([cx - R + 18, cy - R + 18, cx + R - 18, cy + R - 18], fill=CRIMSON + (255,))
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=GOLD + (255,))
    # carpet body flowing to bottom-right
    d.polygon([(cx + 60, cy - 60), (S - 60, cy + 190), (S - 90, cy + 320), (cx + 30, cy + 110)], fill=CRIMSON + (255,))
    d.line([(cx + 56, cy - 44), (S - 66, cy + 186)], fill=GOLD + (255,), width=12)
    d.line([(cx + 40, cy + 96), (S - 96, cy + 306)], fill=GOLD + (255,), width=12)
    # tassels
    for t in range(4):
        tx = S - 70 + t * 6
        ty = 330 + t * 4
        d.line([(tx, ty), (tx - 26, ty + 34)], fill=GOLD + (255,), width=7)
    for k in range(8, 26, 4):
        ang = k * 0.7
        x = cx + int(210 * math.cos(ang)); y = cy + int(150 * math.sin(ang))
        sparkle(d, x, y, 10 + (k % 3) * 5, GOLD + (230,))
    im.save(os.path.join(F, 'carpet-fly.png'))

# ---------------- hero floating art: flying money ----------------
def money_fly():
    S = 620
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    def bill(cx, cy, rot):
        b = Image.new('RGBA', (300, 150), (0, 0, 0, 0))
        bd = ImageDraw.Draw(b)
        bd.rounded_rectangle([6, 6, 294, 144], 14, fill=GREEN + (255,), outline=BLACK + (255,), width=6)
        bd.rounded_rectangle([24, 24, 276, 126], 8, outline=CREAM + (255,), width=5)
        bd.ellipse([110, 40, 190, 110], fill=GREEN_D + (255,))
        bd.ellipse([128, 55, 172, 95], fill=GOLD + (255,))
        bd.text((150, 20), "$", font=font(30), fill=BLACK + (255,), anchor="mm")
        b = b.rotate(rot, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(b, (int(cx - b.width / 2), int(cy - b.height / 2)))
    bill(200, 200, -18)
    bill(400, 330, 12)
    bill(240, 430, 24)
    sparkle(d, 480, 140, 18, GOLD + (235,))
    sparkle(d, 120, 330, 12, GOLD + (200,))
    im.save(os.path.join(F, 'money-flying.png'))

# ---------------- PnL placeholder cards ----------------
def pnl_cards():
    rows = [("+312%", "early ca → 40x"), ("+187%", "vip play · thesis called"), ("+94%", "stream call"), ("+245%", "project recap follow"), ("+121%", "vip-only launch"), ("+406%", "student narrative")]
    for i, (pct, tag) in enumerate(rows, 1):
        W, H = 760, 460
        im = Image.new('RGB', (W, H), (18, 15, 12))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W - 1, H - 1], outline=(60, 50, 34), width=3)
        d.rectangle([0, 0, W, 64], fill=(26, 21, 16))
        d.text((24, 32), "CARPET'S INSIDERS — MEMBER PNL", font=font(24), fill=GOLD, anchor="lm")
        d.text((W - 24, 32), "LIVE", font=font(20), fill=GREEN, anchor="rm")
        # fake equity curve
        pts = []
        random.seed(i * 77)
        y = H - 110
        for x in range(60, W - 60, 28):
            y -= random.randint(-8, 26)
            y = max(120, min(H - 90, y))
            pts.append((x, y))
        d.line(pts, fill=GREEN, width=6, joint="curve")
        for p in pts[::4]:
            d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], fill=CREAM)
        d.text((60, 100), pct, font=font(72), fill=GREEN)
        d.text((60, 196), tag, font=font(26), fill=(200, 180, 140))
        d.rounded_rectangle([60, H - 84, 470, H - 36], 8, fill=(30, 24, 18))
        d.text((76, H - 60), "FULL PNL WALL DROPS SOON", font=font(20), fill=GOLD_D, anchor="lm")
        im.save(os.path.join(F, f'pnl{i}.png'))

import random

# ---------------- feature icons ----------------
def icons():
    def base():
        im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
        return im, ImageDraw.Draw(im)
    def save(im, name):
        im.save(os.path.join(F, name))
    # crown — early CAs
    im, d = base()
    d.polygon([(16, 92), (20, 40), (44, 64), (64, 28), (84, 64), (108, 40), (112, 92)], fill=GOLD + (255,))
    d.rectangle([16, 92, 112, 106], fill=GOLD_D + (255,))
    d.ellipse([56, 18, 72, 34], fill=CREAM + (255,))
    save(im, 'ic-crown.png')
    # chat — vip chat
    im, d = base()
    d.rounded_rectangle([14, 22, 114, 86], 16, fill=GREEN + (255,))
    d.polygon([(40, 84), (40, 112), (68, 84)], fill=GREEN + (255,))
    for x in (36, 58, 80):
        d.ellipse([x - 5, 48, x + 5, 58], fill=BLACK + (255,))
    save(im, 'ic-chat.png')
    # bolt — first calls
    im, d = base()
    d.polygon([(72, 10), (34, 66), (58, 66), (50, 118), (96, 52), (68, 52)], fill=CRIMSON + (255,), outline=CREAM + (255,))
    save(im, 'ic-bolt.png')
    # play — streams
    im, d = base()
    d.rounded_rectangle([10, 22, 118, 106], 18, fill=CREAM + (255,))
    d.polygon([(52, 44), (52, 84), (88, 64)], fill=CRIMSON + (255,))
    save(im, 'ic-stream.png')
    # clipboard — recaps
    im, d = base()
    d.rounded_rectangle([24, 18, 104, 112], 10, fill=CREAM + (255,))
    d.rectangle([46, 8, 82, 30], fill=GOLD_D + (255,))
    for y in (48, 66, 84):
        d.line([(40, y), (88, y)], fill=GREEN_D + (255,), width=8)
    save(im, 'ic-recap.png')
    # 1-on-1 — mentorship
    im, d = base()
    d.ellipse([10, 40, 54, 84], fill=GOLD + (255,))
    d.ellipse([74, 40, 118, 84], fill=GREEN + (255,))
    d.line([(54, 62), (74, 62)], fill=CREAM + (255,), width=6)
    save(im, 'ic-mentor.png')
    # chart — analysis
    im, d = base()
    d.line([(14, 108), (114, 108)], fill=CREAM + (255,), width=6)
    for i, (x, h) in enumerate([(28, 40), (50, 66), (72, 30), (94, 84)]):
        col = [GREEN, GOLD, CRIMSON, GREEN][i]
        d.rectangle([x, 108 - h, x + 16, 108], fill=col + (255,))
    save(im, 'ic-chart.png')
    # gift — giveaways
    im, d = base()
    d.rectangle([20, 52, 108, 112], fill=CRIMSON + (255,))
    d.rectangle([16, 40, 112, 56], fill=GOLD + (255,))
    d.rectangle([58, 40, 70, 112], fill=GOLD + (255,))
    d.ellipse([34, 16, 62, 44], outline=CREAM + (255,), width=7)
    d.ellipse([66, 16, 94, 44], outline=CREAM + (255,), width=7)
    save(im, 'ic-gift.png')

# ---------------- social icons (footer) ----------------
def socials():
    # X
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(20, 18), (52, 18), (108, 110), (76, 110)], fill=CREAM + (255,))
    d.polygon([(108, 18), (76, 18), (20, 110), (52, 110)], fill=CREAM + (255,))
    im.save(os.path.join(F, 'ic-x.png'))
    # Discord (simplified controller face)
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 30, 118, 100], 30, fill=CREAM + (255,))
    d.ellipse([30, 50, 56, 76], fill=BLACK + (255,))
    d.ellipse([72, 50, 98, 76], fill=BLACK + (255,))
    d.polygon([(6, 44), (26, 36), (26, 96), (6, 88)], fill=CREAM + (255,))
    d.polygon([(122, 44), (102, 36), (102, 96), (122, 88)], fill=CREAM + (255,))
    im.save(os.path.join(F, 'ic-discord.png'))
    # Instagram
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([14, 14, 114, 114], 26, outline=CREAM + (255,), width=9)
    d.ellipse([42, 42, 86, 86], outline=CREAM + (255,), width=9)
    d.ellipse([90, 24, 102, 36], fill=CREAM + (255,))
    im.save(os.path.join(F, 'ic-ig.png'))
    # TikTok
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line([(52, 16), (52, 96)], fill=CREAM + (255,), width=13)
    d.arc([36, 62, 92, 118], 180, 360, fill=CREAM + (255,), width=13)
    d.line([(52, 30), (100, 30)], fill=CREAM + (255,), width=13)
    d.arc([76, 14, 112, 50], 90, 270, fill=CREAM + (255,), width=13)
    im.save(os.path.join(F, 'ic-tt.png'))

# ---------------- banner background (insiders block) ----------------
def banner_bg():
    W, H = 1600, 900
    im = Image.new('RGB', (W, H), (24, 14, 12))
    d = ImageDraw.Draw(im)
    # perspective carpet
    d.polygon([(W//2 - 700, H), (W//2 + 700, H), (W//2 + 130, 200), (W//2 - 130, 200)], fill=(96, 24, 30))
    for i, f in enumerate([1.0, 0.82, 0.62, 0.4]):
        w = int(640 * f)
        d.line([(W//2 - w, H - i * 4), (W//2 + w, H - i * 4)], fill=(214, 69, 80, 90), width=max(2, int(8 * f)))
    d.line([(W//2 - 640, H - 10), (W//2 - 122, 220)], fill=GOLD_D, width=10)
    d.line([(W//2 + 640, H - 10), (W//2 + 122, 220)], fill=GOLD_D, width=10)
    # stanchions with rope
    for sx, sy in [(W//2 - 240, 560), (W//2 + 240, 560), (W//2 - 180, 420), (W//2 + 180, 420)]:
        d.line([(sx, sy), (sx, sy - 90)], fill=GOLD, width=9)
        d.ellipse([sx - 14, sy - 118, sx + 14, sy - 90], fill=GOLD)
        d.ellipse([sx - 20, sy - 8, sx + 20, sy + 8], fill=GOLD_D)
    for (x1, y1), (x2, y2) in [((W//2 - 240, 476), (W//2 - 180, 340)), ((W//2 - 180, 340), (W//2 + 180, 340)), ((W//2 + 180, 340), (W//2 + 240, 476))]:
        steps = 16
        pts = []
        for s in range(steps + 1):
            t = s / steps
            mx = x1 + (x2 - x1) * t
            my = y1 + (y2 - y1) * t - int(math.sin(t * math.pi) * 36)
            pts.append((mx, my))
        d.line(pts, fill=GOLD, width=6, joint="curve")
    # glow + vignette
    glow = Image.new('L', (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W//2 - 420, 120, W//2 + 420, 620], fill=60)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    gold_layer = Image.new('RGB', (W, H), GOLD)
    im = Image.composite(gold_layer, im, glow.point(lambda p: p // 3))
    vign = Image.new('L', (W, H), 0)
    vd = ImageDraw.Draw(vign)
    vd.rectangle([0, 0, W, H], fill=170)
    vd.ellipse([-200, -150, W + 200, H + 150], fill=0)
    vign = vign.filter(ImageFilter.GaussianBlur(150))
    im = Image.composite(Image.new('RGB', (W, H), (8, 5, 4)), im, vign)
    random.seed(9)
    d = ImageDraw.Draw(im)
    for _ in range(70):
        x, y = random.randint(0, W), random.randint(0, H)
        r = random.randint(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 235, 190))
    im.save(os.path.join(F, 'banner-bg.png'))

logo(); carpet_fly(); money_fly(); pnl_cards(); icons(); socials(); banner_bg()
print('art done:', sorted(os.listdir(F)))
