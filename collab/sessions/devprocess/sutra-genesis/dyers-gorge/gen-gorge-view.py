"""
Generative landscape: The Parvati Gorge
A view looking up-valley — deep V-cut, jade river, altitude-banded vegetation,
atmospheric haze. The valley that swallows light.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches

np.random.seed(2026)

# === Fractal noise (simple diamond-square-ish via spectral synthesis) ===

def fractal_noise_2d(shape, octaves=6, persistence=0.5, lacunarity=2.0):
    """Generate 2D fractal noise by summing octaves of random frequency components."""
    noise = np.zeros(shape)
    amplitude = 1.0
    frequency = 1.0
    for _ in range(octaves):
        # Generate smooth noise at this frequency
        small = (max(2, int(shape[0] / frequency)), max(2, int(shape[1] / frequency)))
        raw = np.random.randn(*small)
        # Upscale with cubic interpolation (using zoom-like approach)
        from scipy.ndimage import zoom
        scaled = zoom(raw, (shape[0] / small[0], shape[1] / small[1]), order=3)
        # Trim to exact shape
        scaled = scaled[:shape[0], :shape[1]]
        noise += amplitude * scaled
        amplitude *= persistence
        frequency *= lacunarity
    # Normalize to [0, 1]
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    return noise


# === Valley geometry ===

width, height = 2000, 1400
aspect = width / height

# Create the valley cross-section: a deep V centered in the image
# The "camera" looks up-valley, so x is lateral, y is vertical (elevation + perspective)

fig, ax = plt.subplots(figsize=(20, 14))
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_aspect('equal')

# Background sky gradient — dawn colours
sky_top = np.array([0.15, 0.18, 0.35])      # deep pre-dawn blue
sky_mid = np.array([0.55, 0.45, 0.50])      # pink-grey horizon
sky_bottom = np.array([0.75, 0.65, 0.55])   # warm haze at valley rim

for y in range(height):
    t = y / height
    if t > 0.6:
        # Upper sky
        s = (t - 0.6) / 0.4
        colour = sky_mid * (1 - s) + sky_top * s
    else:
        # Lower sky / haze
        s = t / 0.6
        colour = sky_bottom * (1 - s) + sky_mid * s
    ax.axhline(y=y, color=colour, linewidth=1.2, alpha=1.0)

# === Mountain ridgelines — multiple layers with atmospheric perspective ===

# The Parvati valley palette for altitude bands
altitude_colours = {
    'river':    '#2E6B5A',  # jade
    'gorge':    '#3D5C4E',  # dark gorge wall
    'deodar':   '#2D4A2D',  # deep forest
    'birch':    '#556B2F',  # lighter forest
    'meadow':   '#7A8B5A',  # alpine grass
    'rock':     '#708090',  # slate/scree
    'snow':     '#E0E8F0',  # snow
}

def generate_ridgeline(x, base_height, amplitude, roughness, seed=0):
    """Generate a ridgeline using summed sinusoids with noise."""
    np.random.seed(seed)
    y = np.full_like(x, base_height, dtype=float)
    # Major features
    for i in range(8):
        freq = (i + 1) * roughness
        phase = np.random.uniform(0, 2 * np.pi)
        amp = amplitude / (i + 1) ** 1.2
        y += amp * np.sin(freq * x / width * 2 * np.pi + phase)
    # Small noise
    y += np.random.randn(len(x)) * amplitude * 0.03
    return y

x = np.arange(width)

# --- Layer 0: Distant peaks (background) — snow-covered, pale, atmospheric ---
for layer in range(3):
    base = 1050 + layer * 80
    ridge = generate_ridgeline(x, base, 180 - layer * 30, 1.5 + layer * 0.3, seed=100 + layer)
    # Add a few prominent peaks
    for _ in range(2):
        peak_x = np.random.randint(200, width - 200)
        peak_h = np.random.uniform(100, 200)
        peak_w = np.random.uniform(150, 300)
        ridge += peak_h * np.exp(-((x - peak_x) / peak_w) ** 2)

    # Atmospheric fade — more distant = more washed out
    fade = 0.4 + layer * 0.15
    base_col = np.array([0.85, 0.88, 0.92])  # snow-white
    haze_col = np.array([0.60, 0.55, 0.58])  # atmospheric haze
    colour = base_col * (1 - fade) + haze_col * fade

    ax.fill_between(x, 0, ridge, color=colour, alpha=0.9 - layer * 0.1)
    # Snow highlight on peaks
    snow_line = ridge - 30
    ax.fill_between(x, snow_line, ridge, color='#E8EFF5', alpha=0.3)

# --- Layer 1: Mid-distance ridges — rock and alpine meadow ---
for layer in range(2):
    base = 850 + layer * 60
    ridge = generate_ridgeline(x, base, 150, 2.0 + layer * 0.5, seed=200 + layer)
    # Deeper V in the center for the valley
    valley_mask = np.exp(-((x - width / 2) / (width * 0.25)) ** 2) * 200
    ridge -= valley_mask

    fade = 0.2 + layer * 0.1
    rock_col = np.array([0.44, 0.50, 0.56])  # slate
    meadow_col = np.array([0.48, 0.55, 0.35])  # alpine green
    # Mix based on height
    for xi in range(0, width, 3):
        h = ridge[xi]
        if h > 900:
            c = rock_col
        else:
            c = meadow_col
        c_faded = c * (1 - fade) + np.array([0.55, 0.50, 0.52]) * fade

    # Just use a gradient fill
    ax.fill_between(x, 0, ridge,
                    color=tuple(rock_col * (1 - fade) + np.array([0.55, 0.50, 0.52]) * fade),
                    alpha=0.95)

# --- Layer 2: Near ridges — deodar forest, dark ---
for layer in range(2):
    base = 600 + layer * 80
    ridge = generate_ridgeline(x, base, 120, 2.5, seed=300 + layer)
    # Stronger V-cut
    valley_mask = np.exp(-((x - width / 2) / (width * 0.18)) ** 2) * 280
    ridge -= valley_mask

    # Dark forest colour with slight variation
    forest_base = np.array([0.18, 0.29, 0.18])
    variation = np.random.uniform(-0.03, 0.03, 3)
    colour = np.clip(forest_base + variation + layer * np.array([0.02, 0.03, 0.01]), 0, 1)

    ax.fill_between(x, 0, ridge, color=tuple(colour), alpha=0.95)

# --- Layer 3: Closest slopes — gorge walls ---
for side in ['left', 'right']:
    base = 450
    seed = 400 if side == 'left' else 410
    ridge = generate_ridgeline(x, base, 100, 3.0, seed=seed)

    if side == 'left':
        # Left wall rises steeply from center
        wall = 200 + 600 * (1 - np.clip((x - width * 0.15) / (width * 0.35), 0, 1))
        ridge = np.minimum(ridge, wall)
    else:
        # Right wall
        wall = 200 + 600 * np.clip((x - width * 0.5) / (width * 0.35), 0, 1)
        ridge = np.minimum(ridge, wall)

    colour = (0.15, 0.22, 0.15) if side == 'left' else (0.13, 0.20, 0.14)
    ax.fill_between(x, 0, ridge, color=colour, alpha=0.97)

# --- The river — jade green ribbon at the valley floor ---
river_center = width / 2
river_width_base = 25
river_y = np.linspace(0, 500, 300)

for i, ry in enumerate(river_y):
    # River narrows as it goes "into" the valley (higher y = further away)
    perspective = 1.0 - (ry / 500) * 0.7
    rw = river_width_base * perspective
    rx_center = river_center + 15 * np.sin(ry * 0.02)  # slight meander

    # Jade colour, lighter at edges (foam)
    jade = np.array([0.18, 0.42, 0.35])
    foam = np.array([0.55, 0.70, 0.62])
    # Atmospheric fade for distant water
    atm = ry / 500 * 0.3
    jade_faded = jade * (1 - atm) + np.array([0.45, 0.42, 0.40]) * atm

    rect = mpatches.Rectangle(
        (rx_center - rw / 2, ry),
        rw, 2.5,
        facecolor=tuple(jade_faded),
        edgecolor='none',
        alpha=0.85
    )
    ax.add_patch(rect)

    # Foam/rapids — white flecks
    if np.random.random() < 0.3:
        fx = rx_center + np.random.uniform(-rw * 0.3, rw * 0.3)
        ax.plot(fx, ry, '.', color='white', markersize=np.random.uniform(0.5, 2) * perspective,
                alpha=0.4 * perspective)

# --- Mist / atmospheric haze layers ---
for y_band in [150, 300, 450, 600]:
    mist_alpha = 0.08 * (1 - y_band / 800)
    ax.axhspan(y_band - 30, y_band + 30, color='#C8C0B8', alpha=mist_alpha)

# --- Subtle light rays from upper right (dawn) ---
for i in range(5):
    ray_x = width * 0.7 + i * 80
    ray_y_top = height
    ray_y_bottom = 600
    ray_width = 40 + i * 10
    ray = mpatches.Polygon(
        [(ray_x, ray_y_top), (ray_x - ray_width, ray_y_bottom),
         (ray_x + ray_width, ray_y_bottom)],
        closed=True, facecolor='#FFE8C0', alpha=0.03, edgecolor='none'
    )
    ax.add_patch(ray)

# === Framing ===
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.patch.set_facecolor('#1A1A2A')

plt.tight_layout(pad=0)
plt.savefig('view-gorge.png', dpi=150, bbox_inches='tight',
            pad_inches=0, facecolor='#1A1A2A', edgecolor='none')
print('view-gorge.png saved')
plt.close()
