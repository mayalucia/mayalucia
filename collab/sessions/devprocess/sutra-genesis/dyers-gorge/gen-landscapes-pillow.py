"""
Generative landscapes for The Dyer's Gorge
Pixel-level rendering using Pillow — proper compositing, atmospheric perspective.

Generates four views:
1. view-gorge.png      — The valley that swallows light (deep V-cut, jade river)
2. view-treeline.png   — Birch forest and alpine boulders with lichen
3. view-deo-tibba.png  — Dawn alpenglow on snow peaks, valley in shadow
4. view-monsoon.png    — Monsoon twilight, iridescent shifting light
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import sys

# === Shared utilities ===

def lerp(a, b, t):
    """Linear interpolation between colours/values."""
    return a * (1 - t) + b * t

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def rgb(r, g, b):
    return (clamp(r * 255), clamp(g * 255), clamp(b * 255))

def ridge(x, width, base, amplitude, n_harmonics=8, seed=0):
    """Generate a ridgeline with fractal detail."""
    rng = np.random.RandomState(seed)
    y = np.full_like(x, base, dtype=np.float64)
    for i in range(n_harmonics):
        freq = (i + 1) * 1.5
        phase = rng.uniform(0, 2 * np.pi)
        amp = amplitude / (i + 1) ** 1.3
        y += amp * np.sin(freq * x / width * 2 * np.pi + phase)
    return y

def add_peaks(y, x, width, n_peaks=3, max_height=200, seed=0):
    """Add gaussian peaks to a ridgeline."""
    rng = np.random.RandomState(seed)
    for _ in range(n_peaks):
        cx = rng.uniform(width * 0.1, width * 0.9)
        h = rng.uniform(max_height * 0.4, max_height)
        w = rng.uniform(width * 0.05, width * 0.15)
        y = y + h * np.exp(-((x - cx) / w) ** 2)
    return y

def valley_cut(y, x, width, depth, center=0.5, spread=0.2):
    """Carve a V-shaped valley into a ridgeline."""
    cx = width * center
    return y - depth * np.exp(-((x - cx) / (width * spread)) ** 2)

def atmospheric_fog(colour, sky_colour, depth, fog_density=1.0):
    """Blend a colour toward sky colour based on depth (0=near, 1=far)."""
    t = 1 - np.exp(-depth * fog_density)
    return lerp(np.array(colour), np.array(sky_colour), t)


# ============================================================
# VIEW 1: The Gorge — looking up-valley at dawn
# ============================================================

def render_gorge(filename='view-gorge.png'):
    print(f"  Rendering {filename}...")
    W, H = 2400, 1600
    img = Image.new('RGB', (W, H))
    pixels = np.zeros((H, W, 3), dtype=np.uint8)

    # Sky gradient
    sky_top = np.array([0.12, 0.14, 0.30])
    sky_mid = np.array([0.50, 0.40, 0.48])
    sky_horizon = np.array([0.75, 0.62, 0.50])
    fog_colour = np.array([0.60, 0.55, 0.52])

    for y in range(H):
        t = 1.0 - y / H  # 0 at bottom, 1 at top
        if t > 0.6:
            c = lerp(sky_mid, sky_top, (t - 0.6) / 0.4)
        else:
            c = lerp(sky_horizon, sky_mid, t / 0.6)
        pixels[y, :] = rgb(*c)

    x = np.arange(W, dtype=np.float64)

    # Mountain layers — back to front, each more opaque and darker
    layers = [
        # (base_y, amplitude, n_peaks, peak_h, valley_depth, valley_spread, colour_rgb, fog_depth, seed)
        (380, 100, 4, 250, 0, 0, np.array([0.82, 0.85, 0.90]), 0.8, 10),   # Distant snow peaks
        (420, 80, 3, 180, 0, 0, np.array([0.70, 0.72, 0.78]), 0.65, 20),    # Far range
        (480, 70, 2, 120, 100, 0.25, np.array([0.50, 0.55, 0.52]), 0.45, 30),  # Mid — rock/meadow
        (540, 60, 1, 80, 150, 0.20, np.array([0.30, 0.42, 0.30]), 0.30, 40),   # Forest ridge
        (600, 50, 0, 0, 200, 0.18, np.array([0.18, 0.30, 0.18]), 0.15, 50),    # Near forest
        (680, 40, 0, 0, 280, 0.15, np.array([0.12, 0.22, 0.13]), 0.05, 60),    # Gorge walls
    ]

    for base_y, amp, n_pk, pk_h, v_depth, v_spread, base_col, fog_d, seed in layers:
        r = ridge(x, W, base_y, amp, seed=seed)
        if n_pk > 0:
            r = add_peaks(r, x, W, n_pk, pk_h, seed=seed + 1000)
        if v_depth > 0:
            r = valley_cut(r, x, W, v_depth, 0.48, v_spread)

        # Apply atmospheric fog
        col = atmospheric_fog(base_col, fog_colour, fog_d)

        # Paint: everything below the ridgeline gets this colour
        col_rgb = rgb(*col)
        for xi in range(W):
            ridge_y = H - int(r[xi])  # Convert to screen coords (y=0 at top)
            ridge_y = max(0, min(H - 1, ridge_y))
            pixels[ridge_y:, xi] = col_rgb

        # Add snow to distant peaks (first two layers)
        if fog_d > 0.5:
            snow_col = rgb(*atmospheric_fog(np.array([0.95, 0.95, 0.98]), fog_colour, fog_d * 0.8))
            for xi in range(W):
                ry = H - int(r[xi])
                snow_depth = 15 + int(10 * np.sin(xi * 0.01))
                for sy in range(ry, min(ry + snow_depth, H)):
                    pixels[sy, xi] = snow_col

    # River — jade ribbon at valley floor
    river_col_near = np.array([0.18, 0.42, 0.35])
    river_col_far = np.array([0.35, 0.45, 0.42])
    river_cx = W * 0.48
    for y in range(H - 1, H - 400, -1):
        t = (H - y) / 400  # 0 at bottom, 1 at distance
        rw = 30 * (1 - t * 0.7)
        col = lerp(river_col_near, river_col_far, t)
        col = atmospheric_fog(col, fog_colour, t * 0.3)
        col_rgb = rgb(*col)
        cx = int(river_cx + 12 * np.sin(y * 0.015))
        for xi in range(max(0, cx - int(rw)), min(W, cx + int(rw))):
            # Only paint if pixel is dark enough (on the valley floor)
            existing = pixels[y, xi]
            if existing[1] < 100:  # Green channel — dark means valley floor
                pixels[y, xi] = col_rgb

    # Foam/rapids
    rng = np.random.RandomState(77)
    for _ in range(200):
        fy = rng.randint(H - 350, H - 10)
        t = (H - fy) / 400
        rw = 30 * (1 - t * 0.7)
        fx = int(river_cx + 12 * np.sin(fy * 0.015) + rng.uniform(-rw * 0.4, rw * 0.4))
        if 0 <= fx < W:
            foam = rgb(0.7, 0.8, 0.75)
            pixels[fy, fx] = foam

    # Mist layers
    mist_img = Image.fromarray(pixels)
    mist_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    mist_draw = ImageDraw.Draw(mist_overlay)
    rng = np.random.RandomState(88)
    for y_band in [H - 150, H - 250, H - 350]:
        for _ in range(300):
            mx = rng.randint(0, W)
            my = y_band + rng.randint(-20, 20)
            mr = rng.randint(30, 100)
            alpha = rng.randint(3, 12)
            mist_draw.ellipse([mx - mr, my - mr, mx + mr, my + mr],
                            fill=(200, 195, 188, alpha))

    mist_img.paste(Image.alpha_composite(
        mist_img.convert('RGBA'), mist_overlay).convert('RGB'))

    mist_img.save(filename, quality=95)
    print(f"  {filename} saved ({W}x{H})")


# ============================================================
# VIEW 2: Treeline — birch forest, boulders, lichen
# ============================================================

def render_treeline(filename='view-treeline.png'):
    print(f"  Rendering {filename}...")
    W, H = 2400, 1400
    pixels = np.zeros((H, W, 3), dtype=np.uint8)

    # Sky — clear autumn day at altitude
    for y in range(H):
        t = 1.0 - y / H
        c = lerp(np.array([0.78, 0.80, 0.86]), np.array([0.35, 0.48, 0.70]), t)
        pixels[y, :] = rgb(*c)

    x = np.arange(W, dtype=np.float64)

    # --- Distant snowy ridge (back) ---
    # These need to be HIGH (large ridge values) so they appear above the treeline
    r = ridge(x, W, 850, 100, seed=11)
    r = add_peaks(r, x, W, 4, 250, seed=111)
    fog_sky = np.array([0.68, 0.70, 0.78])
    snow_base = atmospheric_fog(np.array([0.82, 0.84, 0.90]), fog_sky, 0.5)
    for xi in range(W):
        ry = H - int(r[xi])
        if ry < H:
            # Snow cap (top 25 px)
            snow_rgb = rgb(*atmospheric_fog(np.array([0.94, 0.95, 0.98]), fog_sky, 0.35))
            for y in range(max(0, ry), min(ry + 25, H)):
                pixels[y, xi] = snow_rgb
            # Body — pale rock
            body_rgb = rgb(*snow_base)
            for y in range(min(ry + 25, H), H):
                pixels[y, xi] = body_rgb

    # --- Mid ridge — rock/scree with sparse grass ---
    r2 = ridge(x, W, 720, 70, seed=22)
    r2 = add_peaks(r2, x, W, 2, 120, seed=222)
    mid_col = atmospheric_fog(np.array([0.42, 0.48, 0.40]), fog_sky, 0.25)
    mid_rgb = rgb(*mid_col)
    for xi in range(W):
        ry = H - int(r2[xi])
        for y in range(max(0, ry), H):
            pixels[y, xi] = mid_rgb

    # --- Alpine meadow slope (the treeline zone) ---
    # Gentle slope rather than flat band — lower than mountains
    meadow_ridge = ridge(x, W, 580, 30, seed=33)
    treeline_ridge = ridge(x, W, 650, 25, seed=34)
    meadow_col = np.array([0.45, 0.53, 0.32])
    ground_col = np.array([0.50, 0.40, 0.30])

    for xi in range(W):
        meadow_y = H - int(meadow_ridge[xi])
        tree_y = H - int(treeline_ridge[xi])
        # Meadow zone
        for y in range(max(0, meadow_y), min(tree_y, H)):
            t = (y - meadow_y) / max(1, tree_y - meadow_y)
            c = lerp(meadow_col, ground_col, t)
            pixels[y, xi] = rgb(*c)
        # Below treeline — earthy ground
        for y in range(max(0, tree_y), H):
            # Slight colour variation
            t = (y - tree_y) / max(1, H - tree_y)
            c = lerp(ground_col, np.array([0.42, 0.34, 0.26]), t)
            pixels[y, xi] = rgb(*c)

    # Boulders with lichen (in the alpine meadow zone)
    img = Image.fromarray(pixels)
    draw = ImageDraw.Draw(img)

    rng = np.random.RandomState(33)
    for _ in range(80):
        bx = rng.randint(50, W - 50)
        # Place boulders in the meadow zone
        meadow_y = H - int(meadow_ridge[min(bx, W - 1)])
        tree_y = H - int(treeline_ridge[min(bx, W - 1)])
        by = rng.randint(meadow_y + 5, max(meadow_y + 10, tree_y - 5))
        bw = rng.randint(12, 40)
        bh = rng.randint(8, 28)
        grey = rng.uniform(0.38, 0.58)
        boulder_col = rgb(grey, grey + 0.01, grey + 0.03)
        draw.ellipse([bx - bw, by - bh // 2, bx + bw, by + bh // 2], fill=boulder_col)
        # Shadow underneath
        draw.ellipse([bx - bw + 2, by + bh // 4, bx + bw + 3, by + bh // 2 + 4],
                     fill=rgb(grey * 0.6, grey * 0.6, grey * 0.6))

        # Lichen — orange/gold patches on the boulder face
        if rng.random() < 0.65:
            for _ in range(rng.randint(1, 7)):
                lx = bx + rng.randint(-bw // 2, bw // 2)
                ly = by + rng.randint(-bh // 3, bh // 4)
                lr = rng.randint(2, 6)
                lichen_colours = [(218, 165, 32), (232, 185, 96), (196, 146, 31),
                                  (184, 134, 11), (210, 170, 40)]
                lc = lichen_colours[rng.randint(len(lichen_colours))]
                draw.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=lc)

    # Birch trees — improved: vertical trunk lines, crown as cloud of dots
    def draw_birch(draw, bx, by, height, rng, faded=False):
        trunk_top = by - height
        trunk_width_base = max(2, int(height / 40))
        lean = rng.uniform(-0.08, 0.08) * height

        # Trunk — vertical white line with taper
        for seg_y in range(by, max(0, trunk_top), -1):
            t = (by - seg_y) / height
            tx = bx + int(lean * t)
            tw = max(1, int(trunk_width_base * (1 - t * 0.6)))
            bark_v = rng.randint(210, 245) if not faded else rng.randint(180, 210)
            draw.line([(tx - tw, seg_y), (tx + tw, seg_y)],
                     fill=(bark_v, bark_v - 2, bark_v - 5), width=1)
            # Horizontal bark marks (birch characteristic)
            if rng.random() < 0.15:
                mark_w = tw + rng.randint(1, 4)
                draw.line([(tx - mark_w, seg_y), (tx + mark_w, seg_y)],
                         fill=(65, 60, 55), width=1)

        # Crown — concentrated at the top, narrower than before
        crown_center_x = bx + int(lean * 0.7)
        crown_top = trunk_top - int(height * 0.05)
        crown_bottom = by - int(height * 0.45)
        crown_width = int(height * 0.15)

        n_leaves = rng.randint(20, 55) if not faded else rng.randint(10, 25)
        for _ in range(n_leaves):
            # Leaves clustered around the trunk top
            ly = rng.randint(crown_top, crown_bottom)
            crown_t = (ly - crown_top) / max(1, crown_bottom - crown_top)
            spread = int(crown_width * (0.5 + 0.5 * np.sin(crown_t * np.pi)))
            lx = crown_center_x + rng.randint(-spread, spread + 1)
            ls = rng.randint(2, 5) if not faded else rng.randint(1, 3)
            if faded:
                golds = [(188, 155, 72), (195, 170, 90), (175, 140, 60)]
            else:
                golds = [(218, 165, 32), (232, 196, 74), (196, 146, 16),
                         (240, 212, 138), (184, 134, 11), (210, 180, 60)]
            gc = golds[rng.randint(len(golds))]
            draw.ellipse([lx - ls, ly - ls, lx + ls, ly + ls], fill=gc)

    rng2 = np.random.RandomState(44)

    # Far background trees (small, faded) — placed just below meadow line
    for _ in range(50):
        tx = rng2.randint(30, W - 30)
        local_tree_y = H - int(treeline_ridge[min(tx, W - 1)])
        ty = rng2.randint(local_tree_y - 30, local_tree_y + 50)
        th = rng2.randint(40, 90)
        draw_birch(draw, tx, ty, th, rng2, faded=True)

    # Mid-ground trees
    for _ in range(70):
        tx = rng2.randint(30, W - 30)
        local_tree_y = H - int(treeline_ridge[min(tx, W - 1)])
        ty = rng2.randint(local_tree_y + 20, local_tree_y + 180)
        th = rng2.randint(80, 170)
        draw_birch(draw, tx, ty, th, rng2, faded=False)

    # Foreground trees (large, detailed)
    for _ in range(15):
        tx = rng2.randint(30, W - 30)
        ty = rng2.randint(H - 300, H - 80)
        th = rng2.randint(200, 400)
        draw_birch(draw, tx, ty, th, rng2, faded=False)

    # Rhododendrons at the treeline boundary
    for _ in range(15):
        rx = rng2.randint(100, W - 100)
        local_tree_y = H - int(treeline_ridge[min(rx, W - 1)])
        ry = rng2.randint(local_tree_y - 15, local_tree_y + 25)
        rh = rng2.randint(35, 70)
        # Gnarled trunk
        draw.line([(rx, ry), (rx + rng2.randint(-8, 8), ry - rh)],
                 fill=(55, 38, 22), width=3)
        # Dense dark leaves
        for _ in range(35):
            lx = rx + rng2.randint(-rh // 3, rh // 3)
            ly = ry - rng2.randint(rh // 3, rh)
            ls = rng2.randint(3, 6)
            draw.ellipse([lx - ls, ly - ls // 2, lx + ls, ly + ls // 2],
                        fill=(30, 60, 30))
        # Red blooms (spring — a few scattered)
        if rng2.random() < 0.4:
            for _ in range(rng2.randint(3, 8)):
                bx2 = rx + rng2.randint(-rh // 4, rh // 4)
                by2 = ry - rng2.randint(rh // 2, rh * 3 // 4)
                draw.ellipse([bx2 - 4, by2 - 3, bx2 + 4, by2 + 3], fill=(196, 30, 58))

    # Scattered fallen leaves on the ground
    for _ in range(800):
        lx = rng2.randint(0, W)
        local_tree_y = H - int(treeline_ridge[min(lx, W - 1)])
        ly = rng2.randint(local_tree_y, H)
        lc_options = [(180, 140, 30), (160, 120, 20), (200, 160, 50),
                      (140, 100, 40), (170, 130, 40)]
        lc = lc_options[rng2.randint(len(lc_options))]
        ls = rng2.randint(1, 3)
        draw.ellipse([lx - ls, ly, lx + ls, ly + 1], fill=lc)

    img.save(filename, quality=95)
    print(f"  {filename} saved ({W}x{H})")


# ============================================================
# VIEW 3: Deo Tibba Dawn — alpenglow
# ============================================================

def render_deo_tibba(filename='view-deo-tibba-dawn.png'):
    print(f"  Rendering {filename}...")
    W, H = 2400, 1400
    pixels = np.zeros((H, W, 3), dtype=np.uint8)

    # Sky — pre-dawn: deep blue top, warm golden-pink at horizon
    # The key: the horizon band should be wide and warm enough to silhouette the peaks
    for y in range(H):
        t = 1.0 - y / H
        if t > 0.65:
            c = lerp(np.array([0.15, 0.15, 0.35]), np.array([0.06, 0.06, 0.20]), (t - 0.65) / 0.35)
        elif t > 0.40:
            c = lerp(np.array([0.50, 0.35, 0.45]), np.array([0.15, 0.15, 0.35]), (t - 0.40) / 0.25)
        elif t > 0.20:
            # Wider warm band — the dawn glow
            c = lerp(np.array([0.80, 0.60, 0.40]), np.array([0.50, 0.35, 0.45]), (t - 0.20) / 0.20)
        else:
            # Near horizon — golden, bright
            c = lerp(np.array([0.88, 0.72, 0.45]), np.array([0.80, 0.60, 0.40]), t / 0.20)
        pixels[y, :] = rgb(*c)

    # Stars — only in the deep blue zone
    rng = np.random.RandomState(7)
    for _ in range(100):
        sx = rng.randint(0, W)
        sy = rng.randint(0, int(H * 0.35))
        brightness = rng.uniform(0.4, 1.0)
        sz = rng.randint(0, 2)
        for dx in range(-sz, sz + 1):
            for dy in range(-sz, sz + 1):
                if 0 <= sx + dx < W and 0 <= sy + dy < H:
                    fade = 1 - (abs(dx) + abs(dy)) / max(1, 2 * sz)
                    v = brightness * fade
                    pixels[sy + dy, sx + dx] = rgb(v, v, v * 0.95)

    x = np.arange(W, dtype=np.float64)

    # Background range — silhouette against the dawn, blue-grey
    bg = ridge(x, W, 520, 80, seed=10)
    bg = add_peaks(bg, x, W, 4, 140, seed=110)
    bg_col = np.array([0.22, 0.20, 0.28])
    for xi in range(W):
        ry = H - int(bg[xi])
        for y in range(max(0, ry), H):
            pixels[y, xi] = rgb(*bg_col)

    # Deo Tibba massif — the dominant peak
    dt = ridge(x, W, 600, 50, seed=20)
    # Main summit — large, asymmetric
    dt = dt + 350 * np.exp(-((x - W * 0.42) / 180) ** 2)
    # East shoulder — broader, lower
    dt = dt + 200 * np.exp(-((x - W * 0.56) / 260) ** 2)
    # West buttress
    dt = dt + 120 * np.exp(-((x - W * 0.30) / 200) ** 2)

    # The body: dark rock in shadow, but NOT pure black —
    # slight blue cast from pre-dawn sky reflection
    dt_shadow = np.array([0.08, 0.08, 0.14])
    dt_mid = np.array([0.12, 0.12, 0.18])
    for xi in range(W):
        h = dt[xi]
        ry = H - int(h)
        for y in range(max(0, ry), H):
            # Gradient: slightly lighter near the top, darker at base
            vert_t = (y - ry) / max(1, H - ry)
            col = lerp(dt_mid, dt_shadow, vert_t)
            pixels[y, xi] = rgb(*col)

    # ALPENGLOW — the centrepiece
    # Wider glow zone, stronger light, snow integrated
    peak_max = dt.max()
    glow_threshold = peak_max - 150  # Wider glow band

    for xi in range(W):
        h = dt[xi]
        if h > glow_threshold:
            ry = H - int(h)
            exposure = (h - glow_threshold) / (peak_max - glow_threshold)
            # Eastern bias — light from the right
            east = np.clip((xi - W * 0.35) / (W * 0.25), -0.1, 1.0) * 0.35 + 0.65
            intensity = exposure ** 0.7 * east  # Softer falloff with power curve

            # Warm alpenglow: deep gold at base, rose-pink at tip
            glow = lerp(np.array([0.92, 0.62, 0.35]), np.array([0.98, 0.82, 0.65]), exposure)
            glow = glow * intensity

            # Paint glow band — wider, with snow integrated
            glow_depth = int(45 * exposure)
            for dy in range(glow_depth):
                py = ry + dy
                if 0 <= py < H:
                    fade = 1 - (dy / glow_depth) ** 0.8
                    # Snow patches: brighter streaks in the glow zone
                    snow_boost = 0.0
                    if rng.random() < 0.15 * exposure:
                        snow_boost = 0.15
                    final = lerp(dt_mid, glow + snow_boost, fade)
                    final = np.clip(final, 0, 1)
                    pixels[py, xi] = rgb(*final)

    # Pin Parvati range — second peak to the right, slightly lighter than fg
    pp = ridge(x, W, 560, 50, seed=30)
    pp = pp + 220 * np.exp(-((x - W * 0.78) / 180) ** 2)
    pp = pp + 100 * np.exp(-((x - W * 0.85) / 150) ** 2)
    pp_col = np.array([0.07, 0.07, 0.11])
    for xi in range(W):
        ry = H - int(pp[xi])
        for y in range(max(0, ry), H):
            existing = pixels[y, xi]
            # Only overwrite if darker or same
            if existing[0] <= 35 and existing[2] <= 50:
                pixels[y, xi] = rgb(*pp_col)

    # Faint glow on Pin Parvati
    pp_max = pp.max()
    pp_glow_t = pp_max - 80
    for xi in range(W):
        h = pp[xi]
        if h > pp_glow_t:
            ry = H - int(h)
            exposure = (h - pp_glow_t) / (pp_max - pp_glow_t) * 0.5
            glow = np.array([0.75, 0.50, 0.30]) * exposure
            depth = int(20 * exposure)
            for dy in range(depth):
                py = ry + dy
                if 0 <= py < H:
                    fade = 1 - dy / max(1, depth)
                    final = lerp(pp_col, glow, fade)
                    pixels[py, xi] = rgb(*final)

    # Foreground ridges — deep shadow, dark forest tones
    fg = ridge(x, W, 800, 60, seed=40)
    fg = valley_cut(fg, x, W, 320, 0.48, 0.18)
    fg_col = np.array([0.03, 0.04, 0.05])
    for xi in range(W):
        ry = H - int(fg[xi])
        for y in range(max(0, ry), H):
            pixels[y, xi] = rgb(*fg_col)

    # Valley floor
    for y in range(H - 160, H):
        pixels[y, :] = rgb(0.02, 0.02, 0.03)

    # Mist in the valley — use RGBA overlay for soft blending
    img = Image.fromarray(pixels)
    mist_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    mist_draw = ImageDraw.Draw(mist_overlay)
    rng3 = np.random.RandomState(55)
    for _ in range(600):
        mx = rng3.randint(W * 2 // 10, W * 8 // 10)
        my = rng3.randint(H - 220, H - 40)
        mr = rng3.randint(40, 120)
        alpha = rng3.randint(4, 16)
        mist_draw.ellipse([mx - mr, my - mr // 3, mx + mr, my + mr // 3],
                         fill=(180, 175, 165, alpha))

    final_img = Image.alpha_composite(img.convert('RGBA'), mist_overlay).convert('RGB')
    final_img.save(filename, quality=95)
    print(f"  {filename} saved ({W}x{H})")


# ============================================================
# VIEW 4: Monsoon Twilight — iridescent, shifting
# ============================================================

def render_monsoon(filename='view-monsoon.png'):
    print(f"  Rendering {filename}...")
    W, H = 2400, 1400
    pixels = np.zeros((H, W, 3), dtype=np.uint8)

    rng = np.random.RandomState(2025)

    # Sky — monsoon: heavy, luminous grey-purple with a warm break
    for y in range(H):
        t = 1.0 - y / H
        # Base: purple-grey
        base = np.array([0.48, 0.45, 0.54])
        # Warm break at mid-sky (the monsoon light leaking through)
        glow = 0.12 * np.exp(-((t - 0.55) / 0.06) ** 2)
        # Green reflection from wet forest at lower sky
        green_tinge = 0.04 * np.clip(1 - t / 0.35, 0, 1)
        c = base + np.array([glow * 1.5, glow * 0.7 + green_tinge, glow * 0.2 - green_tinge * 0.5])
        c = np.clip(c, 0, 1)
        # Add slight noise for cloud texture
        noise = rng.uniform(-0.015, 0.015, 3)
        c = np.clip(c + noise, 0, 1)
        pixels[y, :] = rgb(*c)

    x = np.arange(W, dtype=np.float64)

    # Rain streaks — across entire image
    rain_img = Image.fromarray(pixels).convert('RGBA')
    rain_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rain_draw = ImageDraw.Draw(rain_overlay)
    for _ in range(600):
        rx = rng.randint(-50, W + 50)
        ry = rng.randint(0, H)
        rl = rng.randint(15, 50)
        alpha = rng.randint(5, 20)
        rain_draw.line([(rx, ry), (rx + int(rl * 0.15), ry + rl)],
                      fill=(180, 185, 195, alpha), width=1)
    rain_img = Image.alpha_composite(rain_img, rain_overlay)
    pixels = np.array(rain_img.convert('RGB'))

    # Cloud masses — low, heavy
    cloud_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cloud_draw = ImageDraw.Draw(cloud_overlay)
    for _ in range(400):
        cx = rng.randint(-100, W + 100)
        cy = rng.randint(int(H * 0.15), int(H * 0.55))
        cr = rng.randint(40, 120)
        grey = rng.randint(110, 145)
        alpha = rng.randint(8, 25)
        cloud_draw.ellipse([cx - cr, cy - cr // 2, cx + cr, cy + cr // 2],
                          fill=(grey, grey - 3, grey + 5, alpha))

    cloud_base = Image.fromarray(pixels).convert('RGBA')
    cloud_base = Image.alpha_composite(cloud_base, cloud_overlay)
    pixels = np.array(cloud_base.convert('RGB'))

    # Mountains — dark, wet, rain-deepened colours
    # Use explicit hand-picked colours for clear atmospheric separation.
    # Monsoon in the Parvati: far things are purple-grey, near things are deep green.

    # Mountains: the trick is that near ridges have DEEP valley cuts so far ridges
    # show through the gap. Each nearer ridge is taller at edges but deeply cut in center.

    # Far ridge — highest peaks, ghostly, barely visible
    far = ridge(x, W, 550, 80, seed=100)
    far = add_peaks(far, x, W, 4, 150, seed=1100)
    far_rgb = rgb(0.46, 0.44, 0.50)
    for xi in range(W):
        ry = H - int(far[xi])
        for y in range(max(0, ry), H):
            pixels[y, xi] = far_rgb

    # Mid-far ridge — grey-green, with moderate valley cut
    midfar = ridge(x, W, 580, 60, seed=150)
    midfar = add_peaks(midfar, x, W, 2, 80, seed=1150)
    midfar = valley_cut(midfar, x, W, 200, 0.45, 0.20)
    midfar_rgb = rgb(0.32, 0.36, 0.33)
    for xi in range(W):
        ry = H - int(midfar[xi])
        for y in range(max(0, ry), H):
            pixels[y, xi] = midfar_rgb

    # Mid ridge — dark green, deeper valley cut
    mid = ridge(x, W, 620, 60, seed=200)
    mid = valley_cut(mid, x, W, 300, 0.45, 0.18)
    mid_rgb = rgb(0.18, 0.28, 0.18)
    for xi in range(W):
        ry = H - int(mid[xi])
        for y in range(max(0, ry), H):
            pixels[y, xi] = mid_rgb

    # Wet rock gleams on mid ridge
    for xi in range(0, W, 3):
        ry = H - int(mid[xi])
        if rng.random() < 0.10:
            gleam_y = ry + rng.randint(3, 50)
            if gleam_y < H:
                v = rng.uniform(0.32, 0.48)
                pixels[gleam_y, xi] = rgb(v, v + 0.05, v + 0.03)
                if xi + 1 < W:
                    pixels[gleam_y, xi + 1] = rgb(v * 0.9, v * 0.9 + 0.04, v * 0.9 + 0.02)

    # Near ridge — deepest valley cut, very dark
    near = ridge(x, W, 680, 40, seed=300)
    near = valley_cut(near, x, W, 380, 0.45, 0.14)
    near_rgb = rgb(0.06, 0.14, 0.06)
    for xi in range(W):
        ry = H - int(near[xi])
        for y in range(max(0, ry), H):
            pixels[y, xi] = near_rgb

    # Swollen river — jade-brown
    river_cx = W * 0.45
    rw_base = 50
    for y in range(H - 1, H - 350, -1):
        t = (H - y) / 350
        rw = rw_base * (1 - t * 0.6)
        col = lerp(np.array([0.20, 0.32, 0.28]), np.array([0.35, 0.35, 0.33]), t)
        col = atmospheric_fog(col, np.array([0.50, 0.48, 0.52]), t * 0.2)
        col_rgb = rgb(*col)
        cx = int(river_cx + 15 * np.sin(y * 0.012))
        for xi in range(max(0, cx - int(rw)), min(W, cx + int(rw))):
            existing = pixels[y, xi]
            if existing[1] < 60:
                pixels[y, xi] = col_rgb

    # Turbulence / foam
    for _ in range(300):
        fy = rng.randint(H - 300, H - 20)
        t = (H - fy) / 350
        rw = rw_base * (1 - t * 0.6)
        fx = int(river_cx + 15 * np.sin(fy * 0.012) + rng.uniform(-rw * 0.4, rw * 0.4))
        if 0 <= fx < W and 0 <= fy < H:
            pixels[fy, fx] = rgb(0.65, 0.70, 0.68)

    # Foreground ferns — wet, dark, dripping
    fern_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fern_draw = ImageDraw.Draw(fern_overlay)
    for _ in range(40):
        fx = rng.randint(0, W)
        fy = rng.randint(H - 120, H - 10)
        frond_len = rng.randint(30, 80)
        angle = rng.uniform(0.3, 1.0)
        n_leaflets = rng.randint(6, 14)
        # Main stem
        sx2 = fx + int(frond_len * np.cos(angle))
        sy2 = fy - int(frond_len * np.sin(angle))
        fern_draw.line([(fx, fy), (sx2, sy2)], fill=(20, 50, 20, 180), width=2)
        # Leaflets
        for i in range(n_leaflets):
            t = i / n_leaflets
            lx = int(fx + (sx2 - fx) * t)
            ly = int(fy + (sy2 - fy) * t)
            ll = rng.randint(8, 20)
            la = angle + rng.choice([-1, 1]) * rng.uniform(0.5, 1.2)
            lx2 = lx + int(ll * np.cos(la))
            ly2 = ly - int(ll * np.sin(la))
            fern_draw.line([(lx, ly), (lx2, ly2)], fill=(25, 55, 25, 140), width=1)
        # Water drops
        for i in range(0, n_leaflets, 2):
            t = i / n_leaflets
            dx = int(fx + (sx2 - fx) * t)
            dy = int(fy + (sy2 - fy) * t) + 3
            fern_draw.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=(190, 210, 210, 100))

    final = Image.alpha_composite(Image.fromarray(pixels).convert('RGBA'), fern_overlay)
    final.convert('RGB').save(filename, quality=95)
    print(f"  {filename} saved ({W}x{H})")


# === Main ===
if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if which in ('all', 'gorge'):
        render_gorge()
    if which in ('all', 'treeline'):
        render_treeline()
    if which in ('all', 'deo-tibba'):
        render_deo_tibba()
    if which in ('all', 'monsoon'):
        render_monsoon()
    print("Done.")
