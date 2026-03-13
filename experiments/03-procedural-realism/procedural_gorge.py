# /// script
# requires-python = ">=3.12"
# dependencies = ["Pillow>=10.0", "numpy>=1.26", "opensimplex>=0.4", "scipy>=1.12"]
# ///
"""
Experiment 03 — Procedural Realism, v2
Gorge-dawn panel with SRTM-driven geometry.

v2 changes over v1:
  - 2D DEM patch for lateral wall structure (gullies, spurs)
  - Corrected sun direction (ENE wall shaded, WSW wall lit at dawn)
  - River follows gorge bottom contour
  - Sharper distant peaks with better snow
  - Foreground terrace with rocky texture
  - DEM-derived slope/aspect for lighting
"""

from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from opensimplex import OpenSimplex
from scipy.ndimage import zoom, gaussian_filter

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

W, H = 768, 512

# ── Noise generators ─────────────────────────────────────────────────

noise_rock = OpenSimplex(seed=137)
noise_detail = OpenSimplex(seed=271)
noise_sky = OpenSimplex(seed=404)


def fbm_array(noise_gen, xs, ys, octaves=6, lacunarity=2.0, gain=0.5):
    """Vectorised FBM."""
    value = np.zeros_like(xs, dtype=np.float64)
    amplitude = 1.0
    frequency = 1.0
    for _ in range(octaves):
        layer = np.vectorize(noise_gen.noise2)(xs * frequency, ys * frequency)
        value += amplitude * layer
        amplitude *= gain
        frequency *= lacunarity
    return value


# ── Colour palette ───────────────────────────────────────────────────

SKY_ZENITH = np.array([0.40, 0.55, 0.80])    # deep blue overhead
SKY_HORIZON = np.array([0.88, 0.80, 0.68])   # warm haze at horizon
ROCK_LIT = np.array([0.82, 0.55, 0.28])      # golden-hour lit face
ROCK_WARM = np.array([0.60, 0.40, 0.22])     # warm mid-tone
ROCK_SHADOW = np.array([0.12, 0.11, 0.10])   # deep gorge shadow
ROCK_COOL = np.array([0.25, 0.23, 0.22])     # cool shadow with ambient
SNOW = np.array([0.96, 0.94, 0.96])
SNOW_SHADOW = np.array([0.70, 0.75, 0.85])   # blue-ish shadowed snow
RIVER = np.array([0.60, 0.75, 0.80])         # glacial blue
RIVER_DEEP = np.array([0.30, 0.42, 0.48])
ROCK_FG = np.array([0.35, 0.28, 0.22])       # foreground terrace


# ── Utility ──────────────────────────────────────────────────────────

def lerp_c(a, b, t):
    """Colour lerp: a, b are (3,), t is (H, W) → (H, W, 3)."""
    t3 = t[:, :, None] if t.ndim == 2 else t
    return a * (1 - t3) + b * t3


def smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0 + 1e-10), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ── Load DEM data ───────────────────────────────────────────────────

def load_data():
    npz_path = Path(__file__).parent / "output" / "transects.npz"
    if not npz_path.exists():
        raise FileNotFoundError(f"Run fetch_dem.py first → {npz_path}")
    data = np.load(npz_path)
    return data["d_ene"], data["e_ene"], data["dem_patch"]


def compute_slope_aspect(dem):
    """
    Compute slope and aspect from a DEM array.
    Returns slope (0..1, 0=flat, 1=vertical) and
    aspect as (dx, dy) gradient components.
    """
    # Gradient in x and y (Sobel-like)
    dy, dx = np.gradient(dem)
    slope = np.sqrt(dx**2 + dy**2)
    slope = slope / (slope.max() + 1e-10)  # normalise
    return slope, dx, dy


# ── Rendering ────────────────────────────────────────────────────────

def render(img, distances_km, elevations_m, dem_patch):
    """Render the gorge scene."""

    xn = np.linspace(0, 1, W)
    yn = np.linspace(0, 1, H)
    XN, YN = np.meshgrid(xn, yn)

    # ── Prepare terrain profile ──────────────────────────────────────
    river_idx = np.argmin(elevations_m)
    river_elev = elevations_m[river_idx]
    river_km = distances_km[river_idx]

    # Crop to ±5km around river
    mask = np.abs(distances_km - river_km) < 5.0
    d_crop = distances_km[mask]
    e_crop = elevations_m[mask]

    # Normalise to image coords
    x_prof = (d_crop - d_crop[0]) / (d_crop[-1] - d_crop[0])
    e_min, e_max = river_elev, e_crop.max()
    y_top, y_river = 0.06, 0.78
    y_prof = y_river - (e_crop - e_min) / (e_max - e_min + 1e-10) * (y_river - y_top)

    # Interpolate to every pixel column
    terrain_y = np.interp(xn, x_prof, y_prof)
    TERRAIN = terrain_y[None, :]

    # River center in image x
    river_x_local = np.argmin(np.abs(d_crop - river_km))
    river_x_norm = x_prof[river_x_local]

    # ── Prepare 2D DEM for wall texture ──────────────────────────────
    # Resize DEM patch to image resolution
    dem_resized = zoom(dem_patch, (H / dem_patch.shape[0], W / dem_patch.shape[1]),
                       order=1)
    # Normalise elevation for texture use
    dem_norm = (dem_resized - dem_resized.min()) / (dem_resized.max() - dem_resized.min() + 1e-10)
    slope, dx, dy = compute_slope_aspect(dem_resized)
    slope_smooth = gaussian_filter(slope, sigma=2)

    # ── 1. Sky ───────────────────────────────────────────────────────
    print("  sky...", end="", flush=True)
    sky_t = smoothstep(0.0, 0.55, YN)
    sky = lerp_c(SKY_ZENITH, SKY_HORIZON, sky_t)

    # Dawn glow on the right side (east)
    dawn_glow = smoothstep(0.4, 1.0, XN) * smoothstep(0.5, 0.2, YN) * 0.12
    sky += np.stack([dawn_glow * 1.2, dawn_glow * 0.6, dawn_glow * 0.1], axis=-1)

    sky_noise = fbm_array(noise_sky, XN * 4, YN * 4, octaves=3) * 0.02
    sky += sky_noise[:, :, None]
    img[:] = np.clip(sky, 0, 1)
    print(" ✓")

    # ── 2. Distant peaks ─────────────────────────────────────────────
    print("  peaks...", end="", flush=True)
    # Use the N–S transect idea: real peaks are behind us (toward Nanga Parbat)
    # Generate a convincing ridgeline from noise, placed above the gorge
    peak_xs = np.linspace(0, 1, W)
    peak_base = 0.08
    # Multiple ridge layers for depth
    for layer_i, (scale, height, alpha, color_t) in enumerate([
        (3.0, 0.12, 0.5, 0.7),   # far ridge — faded
        (4.5, 0.08, 0.7, 0.4),   # mid ridge
    ]):
        ridge_y = np.zeros(W)
        for x in range(W):
            n = noise_rock.noise2(x / W * scale, layer_i * 10.0)
            n2 = noise_detail.noise2(x / W * scale * 3, layer_i * 10.0 + 5) * 0.3
            ridge_y[x] = peak_base + (n + n2) * height

        for x in range(W):
            ridge_top = int(ridge_y[x] * H)
            terrain_top = int(TERRAIN[0, x] * H)
            if ridge_top >= terrain_top:
                continue
            for y in range(max(ridge_top, 0), terrain_top):
                yt = (y - ridge_top) / max(terrain_top - ridge_top, 1)
                # Atmospheric fade
                col = ROCK_WARM * (1 - color_t) + SKY_HORIZON * color_t
                # Snow on upper parts
                snow_t = smoothstep(0.3, 0.0, yt)
                col = col * (1 - snow_t) + SNOW_SHADOW * snow_t
                # Slight texture
                n = noise_rock.noise2(x / W * 10, y / H * 10) * 0.03
                img[y, x] = np.clip(col + n, 0, 1)
    print(" ✓")

    # ── 3. Gorge walls ───────────────────────────────────────────────
    print("  walls...", end="", flush=True)

    is_wall = (YN >= TERRAIN) & (YN <= y_river + 0.03)

    # Depth within wall: 0 = ridgeline, 1 = river
    wall_depth = np.where(
        is_wall,
        (YN - TERRAIN) / np.maximum(y_river - TERRAIN + 0.01, 0.01),
        0.0
    )
    wall_depth = np.clip(wall_depth, 0, 1)

    # Shadow: deeper = darker, steepened by a power curve
    shadow = smoothstep(0.0, 0.65, wall_depth) ** 0.8

    # ── Sun direction (dawn from ENE = upper-right in image) ─────
    # The transect runs ENE (left) → WSW (right).
    # At dawn, the sun is low in the ENE sky, so it illuminates
    # the WSW-facing wall (right side of gorge, which IS the left
    # side of the image because the steep ENE wall is on the left).
    #
    # Actually: the steep wall is ENE (left in image). It FACES WSW.
    # So the steep left wall faces TOWARD the afternoon sun, not the dawn sun.
    # At dawn, the sun is behind the steep wall, so:
    #   - steep left wall (ENE, faces WSW): SHADED at dawn
    #   - gentle right wall (WSW, faces ENE): LIT at dawn ✓
    #
    # sun_facing: 0 = shaded, 1 = fully lit
    # Left of river → shaded (sun is behind this wall)
    # Right of river → lit (faces the dawn sun)
    sun_facing = smoothstep(river_x_norm - 0.15, river_x_norm + 0.25, XN)
    # Upper wall catches more light (less occluded by opposite wall)
    sun_facing *= smoothstep(0.5, 0.0, wall_depth) * 0.7 + 0.3

    # ── DEM-derived texture ──────────────────────────────────────
    # The slope field from the 2D DEM gives real gullies and spurs
    # Use it to modulate rock brightness
    dem_texture = slope_smooth * 0.3  # slope → brightness variation
    # Gradient direction for anisotropic shading
    # dx > 0 means terrain rises to the right → right-facing slope → catches dawn light
    sun_from_dem = np.clip(dx / (np.abs(dx).max() + 1e-10), -1, 1)
    sun_from_dem = (sun_from_dem + 1) * 0.5  # 0..1

    # ── Compose rock colour ──────────────────────────────────────
    # Base: shadow gradient
    rock = lerp_c(ROCK_LIT, ROCK_SHADOW, shadow)

    # Modulate by sun-facing (coarse, from gorge geometry)
    sun_mod = lerp_c(ROCK_COOL, ROCK_LIT, sun_facing)
    rock = rock * 0.4 + sun_mod * 0.6

    # Modulate by DEM slope (fine, from 2D patch)
    dem_bright = lerp_c(ROCK_SHADOW, ROCK_WARM, sun_from_dem * 0.5 + 0.25)
    rock = rock * 0.7 + dem_bright * 0.3

    # DEM elevation contours as subtle banding
    contour = np.sin(dem_norm * 80) * 0.02
    rock += contour[:, :, None]

    # FBM texture on top (fine-scale roughness not in the 90m DEM)
    fine_texture = fbm_array(noise_rock, XN * 3, YN * 30, octaves=4) * 0.06
    fine_texture += fbm_array(noise_detail, XN * 15, YN * 15, octaves=3) * 0.04
    rock += fine_texture[:, :, None]

    rock = np.clip(rock, 0, 1)

    # Composite walls over sky
    wall_mask = is_wall[:, :, None].astype(np.float64)
    img[:] = img * (1 - wall_mask) + rock * wall_mask
    print(" ✓")

    # ── 4. River ─────────────────────────────────────────────────────
    print("  river...", end="", flush=True)

    # River follows the lowest point of each column ± a band
    river_top_y = y_river - 0.005
    river_bot_y = y_river + 0.04
    river_band = (YN >= river_top_y) & (YN <= river_bot_y)

    # Width varies with gorge width
    gorge_width = y_river - terrain_y  # wider gorge → wider river
    gorge_width_norm = gorge_width / (gorge_width.max() + 1e-10)
    # Narrow the river where gorge is narrow
    river_width_mask = np.abs(XN - river_x_norm) < (gorge_width_norm[None, :] * 0.08 + 0.02)
    river_band = river_band & river_width_mask

    river_t = np.where(
        river_band,
        smoothstep(river_top_y, river_bot_y, YN),
        0.0
    )

    river_col = lerp_c(RIVER, RIVER_DEEP, river_t)
    # Flow texture
    flow = fbm_array(noise_detail, XN * 8 + 0.5, YN * 1.5, octaves=3) * 0.05
    river_col += flow[:, :, None]
    # Specular highlights on the water
    spec = fbm_array(noise_sky, XN * 20, YN * 4, octaves=2)
    spec = np.clip(spec, 0, 1) ** 4 * 0.15  # sharp highlights
    river_col += spec[:, :, None]
    river_col = np.clip(river_col, 0, 1)

    river_mask = river_band[:, :, None].astype(np.float64)
    img[:] = img * (1 - river_mask) + river_col * river_mask
    print(" ✓")

    # ── 5. Foreground terrace ────────────────────────────────────────
    print("  foreground...", end="", flush=True)

    fg_start = y_river + 0.04
    fg_mask = YN > fg_start

    # Rocky terrace with boulders
    fg_depth = np.clip((YN - fg_start) / (1.0 - fg_start), 0, 1)
    fg_base = lerp_c(ROCK_COOL, ROCK_FG, fg_depth)

    # Boulder texture from DEM (reuse the slope field)
    boulder = fbm_array(noise_rock, XN * 8, YN * 8, octaves=5)
    boulder_highlight = np.clip(boulder, 0, 1) ** 2 * 0.12
    fg_base += boulder_highlight[:, :, None]

    # Sparse vegetation hints (green-ish patches in lower foreground)
    veg = fbm_array(noise_detail, XN * 5, YN * 5, octaves=3)
    veg_mask = (veg > 0.2) & (fg_depth > 0.4)
    veg_col = np.array([0.22, 0.30, 0.15])
    fg_base[veg_mask] = fg_base[veg_mask] * 0.6 + veg_col * 0.4

    fg_base = np.clip(fg_base, 0, 1)

    fg_mask_3 = fg_mask[:, :, None].astype(np.float64)
    img[:] = img * (1 - fg_mask_3) + fg_base * fg_mask_3
    print(" ✓")

    return img


# ── Main ─────────────────────────────────────────────────────────────

def main():
    print("Loading SRTM data...")
    distances, elevations, dem_patch = load_data()
    print(f"  Transect: {len(distances)} points")
    print(f"  DEM patch: {dem_patch.shape}")

    print("Rendering procedural gorge v2...")
    img = np.zeros((H, W, 3), dtype=np.float64)
    render(img, distances, elevations, dem_patch)

    # Convert and save
    img_u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    result = Image.fromarray(img_u8)
    result = result.filter(ImageFilter.GaussianBlur(radius=0.5))

    out_path = OUT / "gorge-dawn-procedural-v2.png"
    result.save(out_path)
    print(f"\n  → {out_path}")

    # Side-by-side with reference
    ref_path = Path(__file__).parent / "references" / "gorge-dawn-seed271.png"
    if ref_path.exists():
        ref = Image.open(ref_path).resize((W, H))
        # Also load v1 for three-way comparison
        v1_path = OUT / "gorge-dawn-procedural-v1.png"
        if v1_path.exists():
            v1 = Image.open(v1_path)
            comp = Image.new("RGB", (W * 3 + 8, H), (40, 40, 40))
            comp.paste(ref, (0, 0))
            comp.paste(v1, (W + 4, 0))
            comp.paste(result, (W * 2 + 8, 0))
            comp_path = OUT / "comparison-v1-v2.png"
            comp.save(comp_path)
            print(f"  → {comp_path} (ref | v1 | v2)")
        else:
            comp = Image.new("RGB", (W * 2 + 4, H), (40, 40, 40))
            comp.paste(ref, (0, 0))
            comp.paste(result, (W + 4, 0))
            comp_path = OUT / "comparison-v2.png"
            comp.save(comp_path)
            print(f"  → {comp_path} (ref | v2)")


if __name__ == "__main__":
    main()
