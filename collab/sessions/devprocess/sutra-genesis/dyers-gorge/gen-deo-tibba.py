"""
Generative landscape: Deo Tibba at Dawn
Snow peaks catching first light while the valley below remains in shadow.
The moment before the gorge gets its four hours of sun.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7777)

fig, ax = plt.subplots(figsize=(20, 12))
width, height = 2000, 1200
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_aspect('equal')

# === Sky — pre-dawn transitioning to golden first light ===
for y in range(height):
    t = y / height
    if t > 0.7:
        # Upper sky — deep blue fading to lighter
        s = (t - 0.7) / 0.3
        colour = np.array([0.08, 0.10, 0.25]) * s + np.array([0.20, 0.22, 0.40]) * (1 - s)
    elif t > 0.4:
        # Mid sky — blue to pink transition
        s = (t - 0.4) / 0.3
        colour = np.array([0.20, 0.22, 0.40]) * s + np.array([0.65, 0.45, 0.50]) * (1 - s)
    else:
        # Horizon — golden-pink
        s = t / 0.4
        colour = np.array([0.65, 0.45, 0.50]) * s + np.array([0.85, 0.70, 0.50]) * (1 - s)
    ax.axhline(y=y, color=colour, linewidth=1.2)

# === Stars — a few in the deep blue upper sky ===
for _ in range(50):
    sx = np.random.uniform(0, width)
    sy = np.random.uniform(height * 0.75, height)
    star_size = np.random.uniform(0.5, 2.0)
    ax.plot(sx, sy, '.', color='white', markersize=star_size,
            alpha=np.random.uniform(0.3, 0.8))

# === Mountain profiles ===

def ridgeline(x, base, amplitude, frequencies, seed=0):
    np.random.seed(seed)
    y = np.full(len(x), float(base), dtype=np.float64)
    for f in frequencies:
        phase = np.random.uniform(0, 2 * np.pi)
        amp = amplitude / (f + 0.5)
        y += amp * np.sin(f * x / width * 2 * np.pi + phase)
    y += np.random.randn(len(x)) * amplitude * 0.02
    return y

x = np.arange(width)

# --- Deo Tibba massif — the dominant peak ---
# Deo Tibba is 6001m, centered in the frame

# Far background ranges — very pale, atmospheric
bg = ridgeline(x, 820, 100, [1.5, 3, 5, 8], seed=10)
ax.fill_between(x, 0, bg, color='#8888A0', alpha=0.4)

# Main Deo Tibba profile — prominent central peak
peak_center = width * 0.45
peak_base = ridgeline(x, 750, 80, [2, 4, 7], seed=20)
# Add the main summit
deo_tibba_peak = 350 * np.exp(-((x - peak_center) / 200) ** 2)
# Secondary shoulder
shoulder = 200 * np.exp(-((x - peak_center - 300) / 250) ** 2)
peak_profile = peak_base + deo_tibba_peak + shoulder

# The peak in shadow (dark rock/snow)
ax.fill_between(x, 0, peak_profile, color='#3A3A4A', alpha=0.95)

# === ALPENGLOW — first light on the summit ===
# Only the upper portions catch the dawn light
# The magic: warm golden-pink light on snow while everything below is dark

alpenglow_threshold = peak_profile.max() - 200
for xi in range(width):
    h = peak_profile[xi]
    if h > alpenglow_threshold:
        # How far above the shadow line
        exposure = (h - alpenglow_threshold) / (peak_profile.max() - alpenglow_threshold)
        # Golden-pink light, stronger on the eastern (right) face
        eastern_bias = np.clip((xi - peak_center) / 300, -0.3, 1.0) * 0.3 + 0.7

        glow_colour = np.array([0.95, 0.70, 0.50]) * exposure * eastern_bias
        glow_colour = np.clip(glow_colour, 0, 1)

        # Paint glow on the peak
        ax.plot([xi], [h], '.', color=tuple(glow_colour),
                markersize=3, alpha=exposure * 0.8)

        # Snow on the sunlit portions
        if exposure > 0.3:
            snow_col = np.array([1.0, 0.92, 0.85]) * exposure
            snow_col = np.clip(snow_col, 0, 1)
            ax.plot([xi], [h - 5], '.', color=tuple(snow_col),
                    markersize=2, alpha=exposure * 0.5)

# --- Second peak (Pin Parvati range) to the right ---
pin_center = width * 0.75
pin_base = ridgeline(x, 700, 70, [2.5, 5, 9], seed=30)
pin_peak = 250 * np.exp(-((x - pin_center) / 180) ** 2)
pin_profile = pin_base + pin_peak

ax.fill_between(x, 0, pin_profile, color='#2A2A3A', alpha=0.95)

# Alpenglow on Pin Parvati (less, it's further east)
pin_glow_threshold = pin_profile.max() - 120
for xi in range(width):
    h = pin_profile[xi]
    if h > pin_glow_threshold:
        exposure = (h - pin_glow_threshold) / (pin_profile.max() - pin_glow_threshold)
        glow = np.array([0.90, 0.65, 0.45]) * exposure * 0.6
        ax.plot([xi], [h], '.', color=tuple(np.clip(glow, 0, 1)),
                markersize=2, alpha=exposure * 0.6)

# --- Foreground ridges — dark, in complete shadow ---
fg1 = ridgeline(x, 400, 100, [2, 4, 6, 10], seed=40)
# Valley V-cut
valley_cut = 250 * np.exp(-((x - width * 0.5) / (width * 0.2)) ** 2)
fg1 -= valley_cut
ax.fill_between(x, 0, fg1, color='#1A1A22', alpha=0.97)

fg2 = ridgeline(x, 280, 80, [3, 5, 8], seed=50)
valley_cut2 = 200 * np.exp(-((x - width * 0.5) / (width * 0.15)) ** 2)
fg2 -= valley_cut2
ax.fill_between(x, 0, fg2, color='#121218', alpha=0.98)

# --- Valley floor — deepest shadow ---
ax.fill_between(x, 0, 120, color='#0A0A12', alpha=1.0)

# === Mist in the valley ===
for y_band in [100, 180, 260]:
    mist_x = np.arange(width)
    mist_density = 0.06 * np.exp(-((mist_x - width/2) / (width * 0.3)) ** 2)
    for xi in range(0, width, 3):
        if mist_density[xi] > 0.01:
            ax.plot(xi, y_band + np.random.uniform(-15, 15), '.',
                    color='#C0B8B0', markersize=np.random.uniform(1, 4),
                    alpha=mist_density[xi] * np.random.uniform(0.5, 1.0))

# === The river — barely visible, a gleam in the dark ===
river_x = width / 2
for ry in range(20, 120, 2):
    rx = river_x + 8 * np.sin(ry * 0.03) + np.random.uniform(-3, 3)
    gleam = np.random.uniform(0.0, 0.15)
    if gleam > 0.05:
        ax.plot(rx, ry, '.', color='#4A6A6A', markersize=1.5, alpha=gleam)

# === Framing ===
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.patch.set_facecolor('#0A0A12')
plt.tight_layout(pad=0)
plt.savefig('view-deo-tibba-dawn.png', dpi=150, bbox_inches='tight',
            pad_inches=0, facecolor='#0A0A12', edgecolor='none')
print('view-deo-tibba-dawn.png saved')
plt.close()
