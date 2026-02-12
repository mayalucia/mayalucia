"""Blender 5.x: import Kullu valleys mesh with biodiversity annotations.

Combines:
  - Vertex colors encoding 8 biome zones (800–6600 m)
  - Labeled empties at landmarks (towns, peaks, passes, valleys, protected areas)
  - Biome zone markers
  - Key species markers
  - 3D text for highest peak
  - Sun light from NW

Usage: blender --python parbati/kullu/kullu_blender.py

Coordinate system matches kullu_mesh.py:
  Origin = center of Kullu extent (32.05°N, 77.40°E)
  X = east (meters), Y = north (meters), Z = elevation (meters)
"""
import bpy
import bmesh
import math
from mathutils import Vector

# ── Coordinate conversion ─────────────────────────────────────────────

CENTER_LAT = (31.40 + 32.70) / 2   # 32.05
CENTER_LON = (76.80 + 78.00) / 2   # 77.40
DEG_LAT_M = 111320.0
DEG_LON_M = 111320.0 * math.cos(math.radians(32.05))


def latlon_to_xy(lat, lon):
    """Convert lat/lon to local mesh coordinates (meters)."""
    x = (lon - CENTER_LON) * DEG_LON_M
    y = (lat - CENTER_LAT) * DEG_LAT_M
    return x, y


def find_surface_z(terrain_obj, x, y):
    """Raycast downward to find terrain elevation at (x, y)."""
    origin = Vector((x, y, 10000))
    direction = Vector((0, 0, -1))
    inv = terrain_obj.matrix_world.inverted()
    local_origin = inv @ origin
    local_dir = (inv @ (origin + direction) - local_origin).normalized()
    result, loc, normal, index = terrain_obj.ray_cast(local_origin, local_dir)
    if result:
        world_loc = terrain_obj.matrix_world @ loc
        return world_loc.z
    return None


# ── Landmarks ─────────────────────────────────────────────────────────
# (name, lat, lon, known_elev_or_None, type)

LANDMARKS = [
    # Towns along the Beas
    ('Aut',                     31.530, 77.060, None,  'town'),
    ('Bhuntar',                 31.876, 77.160, None,  'town'),
    ('Kullu',                   31.958, 77.109, None,  'town'),
    ('Naggar',                  32.112, 77.169, None,  'town'),
    ('Manali',                  32.240, 77.189, None,  'town'),
    ('Keylong',                 32.572, 77.031, None,  'town'),
    # Parvati Valley towns
    ('Kasol',                   32.010, 77.315, None,  'town'),
    ('Manikaran',               32.030, 77.348, None,  'town'),
    ('Kheerganga',              32.038, 77.493, None,  'town'),
    # Peaks
    ('Parvati Parbat\n6632 m', 32.091, 77.735, 6632,  'summit'),
    ('Hanuman Tibba\n5932 m',  32.273, 77.132, 5932,  'summit'),
    ('Deo Tibba\n6001 m',      32.349, 77.196, 6001,  'summit'),
    ('Indrasan\n6221 m',       32.310, 77.130, 6221,  'summit'),
    # Passes
    ('Rohtang Pass',            32.372, 77.248, 3978,  'pass'),
    ('Pin Parvati Pass',        32.070, 77.820, 5300,  'pass'),
    ('Hamta Pass',              32.307, 77.212, 4268,  'pass'),
    ('Jalori Pass',             31.527, 77.370, 3120,  'pass'),
    ('Chandrakhani',            31.979, 77.183, 3660,  'pass'),
    # Valleys
    ('Parvati Valley',          31.900, 77.200, None,  'valley'),
    ('Tirthan Valley',          31.630, 77.450, None,  'valley'),
    ('Sainj Valley',            31.720, 77.300, None,  'valley'),
    ('Solang Valley',           32.310, 77.160, None,  'valley'),
    # Protected areas
    ('GHNP',                    31.750, 77.500, None,  'protected'),
    ('Khirganga NP',            32.050, 77.600, None,  'protected'),
    # Cardinal directions
    ('N', 32.68, 77.40, None, 'cardinal'),
    ('S', 31.42, 77.40, None, 'cardinal'),
    ('E', 32.05, 77.98, None, 'cardinal'),
    ('W', 32.05, 76.82, None, 'cardinal'),
]

# Biome zone labels (placed at representative locations)
BIOME_MARKERS = [
    ('Subtropical\n(Chir Pine)',        31.600, 77.100, 1400, 'biome'),
    ('Deodar Zone',                     31.850, 77.300, 2200, 'biome'),
    ('Fir-Spruce Zone',                 31.800, 77.420, 2900, 'biome'),
    ('Birch Treeline',                  31.900, 77.500, 3400, 'biome'),
    ('Alpine Meadow',                   32.000, 77.600, 4000, 'biome'),
    ('Nival Zone',                      32.050, 77.730, 5200, 'biome'),
]

# Key species markers (approximate range locations)
SPECIES_MARKERS = [
    ('Snow Leopard\nrange',               32.100, 77.750, 4500, 'fauna'),
    ('W. Tragopan\n(6.5/km\u00b2 GHNP)',  31.800, 77.450, 2800, 'fauna'),
    ('Brown Bear\nrange',                 32.000, 77.550, 3800, 'fauna'),
    ('Musk Deer\nhabitat',                31.850, 77.400, 3000, 'fauna'),
    ('Himalayan Monal',                   31.900, 77.480, 3200, 'fauna'),
    ('Golden Mahseer\n(lower Beas)',      31.600, 77.100, 1200, 'fauna'),
]

# Colors for annotation types
TYPE_COLORS = {
    'summit':    (1.0, 0.2, 0.2),    # red
    'pass':      (1.0, 0.8, 0.1),    # gold
    'town':      (1.0, 1.0, 1.0),    # white
    'valley':    (0.3, 0.8, 0.4),    # green
    'river':     (0.3, 0.6, 1.0),    # blue
    'protected': (0.1, 0.9, 0.5),    # bright green
    'cardinal':  (0.8, 0.8, 0.8),    # light gray
    'biome':     (0.9, 0.8, 0.3),    # warm yellow
    'fauna':     (1.0, 0.5, 0.8),    # pink
}

# Full elevation color ramp: 800 m (Aut) to 6600 m (summit snows)
ELEV_COLORS = [
    ( 500, 0.55, 0.45, 0.30),   # river gorge, warm brown
    ( 800, 0.60, 0.55, 0.35),   # subtropical base
    (1000, 0.65, 0.60, 0.38),   # dry subtropical
    (1400, 0.45, 0.55, 0.25),   # chir pine, olive green
    (1800, 0.30, 0.50, 0.18),   # deodar zone, deep green
    (2200, 0.20, 0.45, 0.15),   # dense temperate, dark green
    (2700, 0.18, 0.38, 0.18),   # fir zone, darker green
    (3200, 0.35, 0.45, 0.25),   # subalpine, medium green
    (3600, 0.50, 0.55, 0.30),   # treeline transition
    (4000, 0.55, 0.50, 0.35),   # alpine meadow, tawny
    (4500, 0.65, 0.60, 0.50),   # high alpine, light brown rock
    (5000, 0.75, 0.72, 0.68),   # scree, grey
    (5400, 0.85, 0.85, 0.88),   # snow edge
    (5800, 0.92, 0.94, 0.96),   # snow
    (6600, 1.00, 1.00, 1.00),   # summit snow
]


def elev_to_color(z):
    """Interpolate color from elevation ramp."""
    if z <= ELEV_COLORS[0][0]:
        return ELEV_COLORS[0][1:]
    if z >= ELEV_COLORS[-1][0]:
        return ELEV_COLORS[-1][1:]
    for i in range(len(ELEV_COLORS) - 1):
        z0, r0, g0, b0 = ELEV_COLORS[i]
        z1, r1, g1, b1 = ELEV_COLORS[i + 1]
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return (r0 + t * (r1 - r0),
                    g0 + t * (g1 - g0),
                    b0 + t * (b1 - b0))
    return (1, 1, 1)


# ── Scene setup ───────────────────────────────────────────────────────

# Clear default objects
for name in ["Cube", "Light", "Camera"]:
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

# Import the bare OBJ
bpy.ops.wm.obj_import(
    filepath="/home/muchu/Darshan/research/develop/agentic/mayalucia/parbati/kullu/data/meshes/kullu.obj"
)

# Find the terrain mesh
terrain = None
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        terrain = obj
        break

if terrain is None:
    raise RuntimeError("No mesh found after import")

bpy.context.view_layer.update()

# ── 1. Vertex colors (biome-encoding elevation bands) ────────────────

print("Painting elevation bands...")
mesh = terrain.data

if "ElevationColor" not in mesh.color_attributes:
    mesh.color_attributes.new(name="ElevationColor", type='BYTE_COLOR', domain='CORNER')

color_layer = mesh.color_attributes["ElevationColor"]

for poly in mesh.polygons:
    for loop_idx in poly.loop_indices:
        vert_idx = mesh.loops[loop_idx].vertex_index
        z = mesh.vertices[vert_idx].co.z
        r, g, b = elev_to_color(z)
        color_layer.data[loop_idx].color = (r, g, b, 1.0)

# Create material using vertex colors
mat_elev = bpy.data.materials.new(name="BiomeElevation")
mat_elev.use_nodes = True
nodes = mat_elev.node_tree.nodes
links = mat_elev.node_tree.links
nodes.clear()

attr_node = nodes.new('ShaderNodeAttribute')
attr_node.attribute_name = "ElevationColor"
attr_node.location = (-300, 0)

bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Roughness'].default_value = 0.9
bsdf.inputs['Specular IOR Level'].default_value = 0.1

output = nodes.new('ShaderNodeOutputMaterial')
output.location = (300, 0)

links.new(attr_node.outputs['Color'], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Replace any existing material
if terrain.data.materials:
    terrain.data.materials[0] = mat_elev
else:
    terrain.data.materials.append(mat_elev)

# ── 2. Labeled empties at landmarks ──────────────────────────────────

print("Placing landmarks...")

if "Annotations" not in bpy.data.collections:
    anno_col = bpy.data.collections.new("Annotations")
    bpy.context.scene.collection.children.link(anno_col)
else:
    anno_col = bpy.data.collections["Annotations"]

def place_markers(markers, offset_z=200):
    """Place labeled empties from a marker list."""
    for entry in markers:
        name, lat, lon, known_elev, ltype = entry
        x, y = latlon_to_xy(lat, lon)
        z = find_surface_z(terrain, x, y)
        if z is None:
            z = known_elev if known_elev else 3000
        elif known_elev and known_elev > z:
            z = known_elev

        display_name = name.replace('\n', ' ')
        empty = bpy.data.objects.new(display_name, None)
        empty.location = (x, y, z + offset_z)

        if ltype == 'summit':
            empty.empty_display_type = 'PLAIN_AXES'
            empty.empty_display_size = 200
        elif ltype == 'cardinal':
            empty.empty_display_type = 'SPHERE'
            empty.empty_display_size = 400
        elif ltype == 'protected':
            empty.empty_display_type = 'CIRCLE'
            empty.empty_display_size = 300
        elif ltype == 'fauna':
            empty.empty_display_type = 'CONE'
            empty.empty_display_size = 200
        elif ltype == 'biome':
            empty.empty_display_type = 'CUBE'
            empty.empty_display_size = 200
        else:
            empty.empty_display_type = 'SPHERE'
            empty.empty_display_size = 150

        empty.show_name = True
        anno_col.objects.link(empty)

place_markers(LANDMARKS)
place_markers(BIOME_MARKERS, offset_z=300)
place_markers(SPECIES_MARKERS, offset_z=350)

# ── 3. 3D text for highest peak ──────────────────────────────────────

print("Adding summit text...")
sx, sy = latlon_to_xy(32.091, 77.735)
sz = find_surface_z(terrain, sx, sy)
if sz is None:
    sz = 6570

# Summit marker pole
curve_data = bpy.data.curves.new('SummitPole', type='CURVE')
curve_data.dimensions = '3D'
spline = curve_data.splines.new('POLY')
spline.points.add(1)
spline.points[0].co = (0, 0, 0, 1)
spline.points[1].co = (0, 0, 800, 1)
curve_data.bevel_depth = 20
pole = bpy.data.objects.new('SummitPole', curve_data)
pole.location = (sx, sy, sz)
anno_col.objects.link(pole)

# Summit text
font_data = bpy.data.curves.new('SummitText', type='FONT')
font_data.body = "PARVATI PARBAT\n6632 m"
font_data.size = 200
font_data.align_x = 'CENTER'
font_data.extrude = 12
text_obj = bpy.data.objects.new('SummitLabel', font_data)
text_obj.location = (sx, sy, sz + 850)
text_obj.rotation_euler = (math.radians(90), 0, 0)
anno_col.objects.link(text_obj)

mat_text = bpy.data.materials.new(name="SummitTextMat")
mat_text.diffuse_color = (1.0, 0.2, 0.1, 1.0)
text_obj.data.materials.append(mat_text)

# ── 4. Sun light from NW ────────────────────────────────────────────

sun_data = bpy.data.lights.new(name="MountainSun", type='SUN')
sun_data.energy = 3.0
sun_data.color = (1.0, 0.95, 0.9)
sun_obj = bpy.data.objects.new("MountainSun", sun_data)
sun_obj.rotation_euler = (math.radians(45), math.radians(-15), math.radians(-45))
bpy.context.scene.collection.objects.link(sun_obj)

# ── Viewport setup ──────────────────────────────────────────────────

terrain.select_set(True)
bpy.context.view_layer.objects.active = terrain

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.clip_end = 300000
                space.shading.type = 'MATERIAL'
                space.overlay.show_extras = True
                space.overlay.show_text = True
        for region in area.regions:
            if region.type == 'WINDOW':
                with bpy.context.temp_override(area=area, region=region):
                    bpy.ops.view3d.view_selected()
                break
        break

print("Done. Annotations in 'Annotations' collection.")
print("Biome zones encoded in vertex colors (BiomeElevation material).")
print(f"Mesh: {len(mesh.vertices):,} vertices, {len(mesh.polygons):,} faces")
