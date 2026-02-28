"""
Generative landscape: The Treeline Transition
Birch forest giving way to alpine meadow — the altitude where lichen grows,
where Kamala Devi harvested Xanthoria from boulders.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)

fig, ax = plt.subplots(figsize=(20, 12))
width, height = 2000, 1200
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_aspect('equal')

# Sky — clear autumn day at altitude
for y in range(height):
    t = y / height
    sky_col = np.array([0.45, 0.55, 0.75]) * t + np.array([0.80, 0.82, 0.88]) * (1 - t)
    ax.axhline(y=y, color=sky_col, linewidth=1.2)

# Distant ridge — snow
ridge_x = np.arange(width)
ridge_y = 950 + 80 * np.sin(ridge_x / width * np.pi * 3) + 40 * np.sin(ridge_x / width * np.pi * 7)
ridge_y += np.random.randn(width) * 5
ax.fill_between(ridge_x, 0, ridge_y, color='#C8D0D8', alpha=0.6)
ax.fill_between(ridge_x, ridge_y - 25, ridge_y, color='#E8F0F5', alpha=0.5)

# Mid ridge — rock and alpine meadow
ridge2_y = 750 + 60 * np.sin(ridge_x / width * np.pi * 4.5 + 1) + 30 * np.sin(ridge_x / width * np.pi * 11 + 2)
ridge2_y += np.random.randn(width) * 4
ax.fill_between(ridge_x, 0, ridge2_y, color='#5A6855', alpha=0.85)

# === The treeline — the sharp boundary ===
# Below: birch trees (white bark, golden/bare branches in autumn)
# Above: alpine meadow with boulders

treeline_height = 500  # The boundary

# Alpine meadow (above treeline)
meadow_top = treeline_height + 200
meadow_y = meadow_top + 40 * np.sin(ridge_x / width * np.pi * 5) + 20 * np.random.randn(width)
ax.fill_between(ridge_x, 0, meadow_y, color='#7A8B5A', alpha=0.9)

# Scattered boulders above treeline — where the lichen grows
for _ in range(80):
    bx = np.random.uniform(100, width - 100)
    by = np.random.uniform(treeline_height + 20, treeline_height + 180)
    bw = np.random.uniform(8, 25)
    bh = np.random.uniform(6, 18)
    boulder_col = np.random.choice(['#708090', '#808888', '#606868', '#7A7A7A'])

    # Boulder shape — irregular rectangle
    pts = np.array([
        [bx - bw/2 + np.random.uniform(-3, 3), by],
        [bx - bw/3, by + bh + np.random.uniform(-2, 2)],
        [bx + bw/3, by + bh + np.random.uniform(-2, 2)],
        [bx + bw/2 + np.random.uniform(-3, 3), by],
    ])
    ax.fill(pts[:, 0], pts[:, 1], color=boulder_col, alpha=0.8)

    # Lichen patches — orange/yellow Xanthoria on the boulders
    if np.random.random() < 0.6:
        n_lichen = np.random.randint(1, 5)
        for _ in range(n_lichen):
            lx = bx + np.random.uniform(-bw/3, bw/3)
            ly = by + np.random.uniform(bh * 0.2, bh * 0.8)
            lr = np.random.uniform(1.5, 4)
            lichen_col = np.random.choice(['#DAA520', '#E8B960', '#C4921F', '#B8860B'])
            circle = plt.Circle((lx, ly), lr, color=lichen_col, alpha=np.random.uniform(0.5, 0.8))
            ax.add_patch(circle)

# Ground below treeline — brown leaf litter, earth
ax.fill_between(ridge_x, 0, treeline_height + 10, color='#8B7355', alpha=0.7)
ax.fill_between(ridge_x, 0, treeline_height - 20, color='#6B5335', alpha=0.8)

# === Birch trees ===
# Distinctive: white/silver peeling bark, golden autumn leaves (or bare branches)

def draw_birch_tree(ax, base_x, base_y, tree_height, lean=0):
    """Draw a stylized birch tree — white trunk, golden crown."""
    # Trunk — white with dark horizontal marks
    trunk_top_y = base_y + tree_height
    trunk_lean_x = base_x + lean * tree_height * 0.15

    # Main trunk
    n_segments = 20
    for i in range(n_segments):
        t = i / n_segments
        seg_x = base_x + (trunk_lean_x - base_x) * t + np.random.uniform(-1, 1)
        seg_y = base_y + tree_height * t
        seg_w = 3.5 * (1 - t * 0.6)  # Tapers

        # White bark
        bark_shade = np.random.uniform(0.85, 0.97)
        ax.plot([seg_x, seg_x], [seg_y, seg_y + tree_height / n_segments + 1],
                color=(bark_shade, bark_shade * 0.98, bark_shade * 0.95),
                linewidth=seg_w, solid_capstyle='round')

        # Horizontal bark marks (birch characteristic)
        if np.random.random() < 0.4:
            mark_w = seg_w * np.random.uniform(0.5, 1.2)
            ax.plot([seg_x - mark_w, seg_x + mark_w], [seg_y, seg_y],
                    color='#4A4A4A', linewidth=0.5, alpha=0.4)

    # Crown — golden autumn leaves (or sparse bare branches)
    crown_y = base_y + tree_height * 0.55
    crown_x = trunk_lean_x
    is_autumn = np.random.random() < 0.7  # Most trees in autumn gold

    if is_autumn:
        # Golden leaf cloud
        n_leaves = np.random.randint(40, 80)
        for _ in range(n_leaves):
            lx = crown_x + np.random.normal(0, tree_height * 0.15)
            ly = crown_y + np.random.uniform(0, tree_height * 0.45)
            ls = np.random.uniform(2, 6)
            leaf_col = np.random.choice([
                '#DAA520', '#E8C44A', '#C49210', '#F0D48A',
                '#8B6914', '#B8860B', '#D4A520', '#E8B040'
            ])
            ax.plot(lx, ly, '.', color=leaf_col,
                    markersize=ls, alpha=np.random.uniform(0.3, 0.7))
    else:
        # Bare branches
        n_branches = np.random.randint(4, 8)
        for _ in range(n_branches):
            br_angle = np.random.uniform(-0.8, 0.8)
            br_len = tree_height * np.random.uniform(0.15, 0.35)
            br_y_start = crown_y + np.random.uniform(0, tree_height * 0.3)
            br_x_end = crown_x + br_len * np.sin(br_angle)
            br_y_end = br_y_start + br_len * np.cos(br_angle) * 0.5
            ax.plot([crown_x, br_x_end], [br_y_start, br_y_end],
                    color='#5A4A3A', linewidth=0.8, alpha=0.6)


# Plant birch forest below treeline
n_trees = 120
for _ in range(n_trees):
    tx = np.random.uniform(50, width - 50)
    ty = np.random.uniform(80, treeline_height - 20)
    th = np.random.uniform(80, 180)
    lean = np.random.uniform(-1, 1)

    # Trees get sparser and smaller near treeline
    treeline_proximity = ty / treeline_height
    if np.random.random() > (1 - treeline_proximity * 0.5):
        th *= (1 - treeline_proximity * 0.4)

    draw_birch_tree(ax, tx, ty, th, lean)

# === A few scattered rhododendrons at the treeline boundary ===
for _ in range(15):
    rx = np.random.uniform(100, width - 100)
    ry = np.random.uniform(treeline_height - 40, treeline_height + 30)
    rh = np.random.uniform(30, 60)

    # Dark trunk
    ax.plot([rx, rx + np.random.uniform(-5, 5)], [ry, ry + rh],
            color='#4A3A2A', linewidth=2, alpha=0.7)

    # Dark evergreen leaves + possible red blooms
    for _ in range(25):
        lx = rx + np.random.normal(0, rh * 0.25)
        ly = ry + np.random.uniform(rh * 0.3, rh)
        ax.plot(lx, ly, '.', color='#2D4A2D',
                markersize=np.random.uniform(3, 7), alpha=0.6)

    # Spring blooms (red)
    if np.random.random() < 0.4:
        for _ in range(8):
            bx = rx + np.random.normal(0, rh * 0.2)
            by = ry + np.random.uniform(rh * 0.5, rh * 0.9)
            ax.plot(bx, by, '.', color='#C41E3A',
                    markersize=np.random.uniform(3, 6), alpha=0.5)

# === Foreground — a few close birch trunks, large ===
for i in range(4):
    tx = np.random.uniform(50, width - 50)
    ty = -20
    th = np.random.uniform(350, 500)
    draw_birch_tree(ax, tx, ty, th, lean=np.random.uniform(-0.5, 0.5))

# === Ground texture — scattered fallen leaves ===
for _ in range(300):
    lx = np.random.uniform(0, width)
    ly = np.random.uniform(0, treeline_height * 0.8)
    leaf_col = np.random.choice(['#DAA520', '#8B6914', '#C49210', '#B8860B', '#6B5335'])
    ax.plot(lx, ly, '.', color=leaf_col,
            markersize=np.random.uniform(1, 3), alpha=0.3)

# === Framing ===
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.patch.set_facecolor('#FEFCF5')
plt.tight_layout(pad=0)
plt.savefig('view-treeline.png', dpi=150, bbox_inches='tight',
            pad_inches=0, facecolor='#FEFCF5', edgecolor='none')
print('view-treeline.png saved')
plt.close()
