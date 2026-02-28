"""
Generative landscape: Monsoon Twilight
The iridescent, shifting light of the Parvati valley during monsoon —
when everything is wet and the colours become ambiguous.
The light for Chapter VI: The Colour That Has No Name.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(2025)

fig, ax = plt.subplots(figsize=(20, 12))
width, height = 2000, 1200
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_aspect('equal')

# === Sky — monsoon: heavy, layered, not dark but luminous-grey ===
# The key quality: light comes from everywhere and nowhere
# Colours shift between purple, green-grey, and a strange warm glow

for y in range(height):
    t = y / height
    # Monsoon sky is not a clean gradient — it has layers and breaks
    base = np.array([0.50, 0.48, 0.55])  # purple-grey
    if t > 0.8:
        # Upper: slightly darker
        colour = base * 0.85 + np.array([0.05, 0.03, 0.10]) * (t - 0.8) / 0.2
    elif t > 0.5:
        # Mid: a break where light leaks through — the monsoon glow
        glow = np.exp(-((t - 0.65) / 0.08) ** 2) * 0.15
        colour = base + np.array([glow * 1.5, glow * 0.8, glow * 0.3])
    elif t > 0.3:
        # Lower sky: greenish tinge (reflected from wet forest)
        s = (t - 0.3) / 0.2
        colour = base + np.array([-0.05, 0.05, -0.03]) * s
    else:
        # Near horizon: misty, warm
        colour = np.array([0.55, 0.52, 0.50]) * (t / 0.3) + np.array([0.62, 0.58, 0.55]) * (1 - t / 0.3)
    colour = np.clip(colour, 0, 1)
    ax.axhline(y=y, color=colour, linewidth=1.2)

# === Rain — diagonal streaks across the entire image ===
rain_angle = 0.15  # Slight diagonal (wind from the west)
for _ in range(800):
    rx = np.random.uniform(-200, width + 200)
    ry = np.random.uniform(0, height)
    rain_len = np.random.uniform(20, 60)
    rain_alpha = np.random.uniform(0.02, 0.08)
    ax.plot([rx, rx + rain_len * rain_angle],
            [ry, ry + rain_len],
            color='#B0B8C0', linewidth=0.3, alpha=rain_alpha)

# === Cloud layers — low, heavy, textured ===
def cloud_layer(ax, y_center, thickness, density, colour_base, alpha_base):
    for _ in range(int(density)):
        cx = np.random.uniform(-100, width + 100)
        cy = y_center + np.random.normal(0, thickness)
        cr = np.random.uniform(20, 80)
        c_alpha = alpha_base * np.random.uniform(0.3, 1.0)
        # Colour variation
        c_var = np.random.uniform(-0.03, 0.03, 3)
        colour = np.clip(np.array(colour_base) + c_var, 0, 1)
        circle = plt.Circle((cx, cy), cr, color=tuple(colour),
                           alpha=c_alpha, edgecolor='none')
        ax.add_patch(circle)

# High clouds
cloud_layer(ax, height * 0.85, 50, 200, [0.52, 0.50, 0.58], 0.15)
# Mid clouds (the luminous break)
cloud_layer(ax, height * 0.65, 40, 150, [0.60, 0.55, 0.52], 0.12)
# Low clouds / mist
cloud_layer(ax, height * 0.35, 60, 250, [0.58, 0.56, 0.55], 0.10)

# === Mountains — dark, wet, colours deepened by rain ===

def ridgeline(x, base, amplitude, frequencies, seed=0):
    np.random.seed(seed)
    y = np.full(len(x), float(base), dtype=np.float64)
    for f in frequencies:
        phase = np.random.uniform(0, 2 * np.pi)
        amp = amplitude / (f + 0.5)
        y += amp * np.sin(f * x / width * 2 * np.pi + phase)
    return y

x = np.arange(width)

# Far ridge — almost invisible in cloud
far = ridgeline(x, 700, 80, [2, 4, 7], seed=100)
ax.fill_between(x, 0, far, color='#484850', alpha=0.4)

# Mid ridge — forest, deepened by rain
mid = ridgeline(x, 550, 90, [2.5, 5, 8], seed=200)
# Wet forest is darker, more saturated
ax.fill_between(x, 0, mid, color='#1A3A1A', alpha=0.7)

# Add wet-rock gleam to the mid ridge
for xi in range(0, width, 5):
    h = mid[xi]
    if np.random.random() < 0.1:
        # Wet rock catch — a brief gleam
        gleam_col = np.random.choice(['#6A7A6A', '#7A8A80', '#5A6A5A'])
        ax.plot(xi, h - np.random.uniform(5, 30), '.',
                color=gleam_col, markersize=np.random.uniform(1, 3),
                alpha=np.random.uniform(0.1, 0.3))

# Near ridge — darkest
near = ridgeline(x, 350, 70, [3, 6, 10], seed=300)
valley_cut = 200 * np.exp(-((x - width * 0.45) / (width * 0.15)) ** 2)
near -= valley_cut
ax.fill_between(x, 0, near, color='#101A10', alpha=0.9)

# === The river — swollen, jade-brown, monsoon fury ===
river_center = width * 0.45
river_width = 60  # Wide — monsoon-swollen

for ry in range(10, 350, 2):
    perspective = max(0.3, 1 - ry / 400)
    rw = river_width * perspective
    rx = river_center + 20 * np.sin(ry * 0.015)

    # Monsoon river: jade mixed with brown (glacial silt + monsoon mud)
    if ry < 100:
        river_col = np.array([0.25, 0.35, 0.30])  # Close: jade-brown
    else:
        fade = ry / 350
        river_col = np.array([0.25, 0.35, 0.30]) * (1 - fade) + np.array([0.40, 0.38, 0.36]) * fade

    ax.plot([rx - rw/2, rx + rw/2], [ry, ry],
            color=tuple(river_col), linewidth=2.5 * perspective, alpha=0.7)

    # Turbulent surface — white flecks (rapids)
    if np.random.random() < 0.4 * perspective:
        fx = rx + np.random.uniform(-rw * 0.4, rw * 0.4)
        ax.plot(fx, ry, '.', color='white',
                markersize=np.random.uniform(0.5, 2.5) * perspective,
                alpha=0.3 * perspective)

# === Wet surfaces — everything gleams ===
# Scattered points of reflected light on every surface

for _ in range(500):
    gx = np.random.uniform(0, width)
    gy = np.random.uniform(0, height * 0.5)
    # Only on surfaces (below ridgelines)
    gleam_col = np.random.choice([
        '#7A8A7A',  # wet leaf
        '#8A9A8A',  # wet rock
        '#6A7A70',  # wet bark
        '#9AA0A0',  # water surface
    ])
    ax.plot(gx, gy, '.', color=gleam_col,
            markersize=np.random.uniform(0.5, 2),
            alpha=np.random.uniform(0.05, 0.15))

# === The luminous break — monsoon light leaking through clouds ===
# A band of warm, strange light in the mid-sky
# This is the light that makes everything iridescent
glow_y = height * 0.62
glow_band = 80
for _ in range(400):
    gx = np.random.uniform(width * 0.2, width * 0.8)
    gy = glow_y + np.random.normal(0, glow_band)
    # Warm glow colours — the light that doesn't belong
    _glow_options = [
        (0.75, 0.65, 0.50),  # golden
        (0.70, 0.60, 0.55),  # amber
        (0.65, 0.60, 0.58),  # warm grey
        (0.72, 0.62, 0.48),  # honey
    ]
    glow_col = _glow_options[np.random.randint(len(_glow_options))]
    ax.plot(gx, gy, '.', color=glow_col,
            markersize=np.random.uniform(3, 10),
            alpha=np.random.uniform(0.02, 0.08))

# === Foreground — close vegetation, wet, dark, dripping ===
for _ in range(60):
    # Fern fronds and leaves, close to camera
    fx = np.random.uniform(0, width)
    fy = np.random.uniform(0, 100)
    frond_len = np.random.uniform(20, 60)
    frond_angle = np.random.uniform(0.3, 1.2)
    n_leaflets = np.random.randint(5, 12)

    # Main stem
    stem_x = np.linspace(fx, fx + frond_len * np.cos(frond_angle), n_leaflets)
    stem_y = np.linspace(fy, fy + frond_len * np.sin(frond_angle), n_leaflets)
    ax.plot(stem_x, stem_y, color='#1A3A1A', linewidth=1.5, alpha=0.7)

    # Leaflets
    for sx, sy in zip(stem_x, stem_y):
        ll = np.random.uniform(5, 15)
        la = frond_angle + np.random.choice([-1, 1]) * np.random.uniform(0.5, 1.2)
        ax.plot([sx, sx + ll * np.cos(la)], [sy, sy + ll * np.sin(la)],
                color='#2A4A2A', linewidth=np.random.uniform(0.5, 1.5), alpha=0.5)

    # Water droplets on the frond
    for sx, sy in zip(stem_x[::2], stem_y[::2]):
        if np.random.random() < 0.5:
            ax.plot(sx, sy - 2, '.', color='#C0D0D0', markersize=1.5, alpha=0.4)

# === Framing ===
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.patch.set_facecolor('#2A2A30')
plt.tight_layout(pad=0)
plt.savefig('view-monsoon-twilight.png', dpi=150, bbox_inches='tight',
            pad_inches=0, facecolor='#2A2A30', edgecolor='none')
print('view-monsoon-twilight.png saved')
plt.close()
