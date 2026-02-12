"""Blender 5.x: import peak mesh with annotations.

Combines:
  - Labeled empties at landmarks
  - 3D text objects for key features
  - Vertex colors for elevation bands

Usage: blender --python parbati/blender_5_annotated.py

Coordinate system matches parbati_mesh.py:
  Origin = center of peak extent (32.09°N, 77.73°E)
  X = east (meters), Y = north (meters), Z = elevation (meters)
"""
import bpy
import bmesh
import math
from mathutils import Vector

# ── Coordinate conversion ─────────────────────────────────────────────

CENTER_LAT = (31.99 + 32.19) / 2  # 32.09
CENTER_LON = (77.63 + 77.83) / 2  # 77.73
DEG_LAT_M = 111320.0
DEG_LON_M = 111320.0 * math.cos(math.radians(32.05))


def latlon_to_xy(lat, lon):
    """Convert lat/lon to local mesh coordinates (meters)."""
    x = (lon - CENTER_LON) * DEG_LON_M
    y = (lat - CENTER_LAT) * DEG_LAT_M
    return x, y


def find_surface_z(terrain_obj, x, y):
    """Raycast downward to find terrain elevation at (x, y)."""
    # Cast from high above, straight down
    origin = Vector((x, y, 10000))
    direction = Vector((0, 0, -1))
    # Convert to object local space
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
# type: 'summit', 'pass', 'glacier', 'ridge', 'place'

LANDMARKS = [
    ('Parvati Parbat\n6632 m',    32.0905, 77.7347, 6632, 'summit'),
    ('Pin Parvati Pass\n~5300 m', 32.070,  77.820,  5300, 'pass'),
    ('NW Ridge',                   32.110,  77.710,  None, 'ridge'),
    ('SE Ridge',                   32.070,  77.760,  None, 'ridge'),
    ('SW Face',                    32.075,  77.720,  None, 'glacier'),
    ('E Glacier',                  32.085,  77.770,  None, 'glacier'),
    ('N',  32.185, 77.730, None, 'cardinal'),
    ('S',  31.995, 77.730, None, 'cardinal'),
    ('E',  32.090, 77.825, None, 'cardinal'),
    ('W',  32.090, 77.635, None, 'cardinal'),
]

# Colors for annotation types
TYPE_COLORS = {
    'summit':   (1.0, 0.2, 0.2),    # red
    'pass':     (1.0, 0.8, 0.1),    # gold
    'glacier':  (0.3, 0.7, 1.0),    # ice blue
    'ridge':    (1.0, 0.5, 0.0),    # orange
    'place':    (1.0, 1.0, 1.0),    # white
    'cardinal': (0.8, 0.8, 0.8),    # light gray
}

# Elevation color ramp (elevation_m, R, G, B)
ELEV_COLORS = [
    (3900, 0.18, 0.32, 0.15),   # dark forest green
    (4200, 0.30, 0.45, 0.20),   # alpine meadow
    (4500, 0.55, 0.50, 0.35),   # brown rock
    (4800, 0.65, 0.60, 0.50),   # light rock
    (5200, 0.75, 0.72, 0.68),   # scree / grey
    (5600, 0.85, 0.85, 0.88),   # snow edge
    (6000, 0.92, 0.94, 0.96),   # snow
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
if "Cube" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)
if "Light" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)

# Import the OBJ
bpy.ops.wm.obj_import(
    filepath="/home/muchu/Darshan/research/develop/agentic/mayalucia/parbati/data/meshes/peak.obj"
)

# Find the terrain mesh
terrain = None
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        terrain = obj
        break

if terrain is None:
    raise RuntimeError("No mesh found after import")

# Ensure mesh data is accessible for raycasting
bpy.context.view_layer.update()

# ── 1. Vertex colors (elevation bands) ───────────────────────────────

print("Painting elevation bands...")
mesh = terrain.data

# Create vertex color layer
if "ElevationColor" not in mesh.color_attributes:
    mesh.color_attributes.new(name="ElevationColor", type='BYTE_COLOR', domain='CORNER')

color_layer = mesh.color_attributes["ElevationColor"]

# Paint each face corner based on vertex elevation
for poly in mesh.polygons:
    for loop_idx in poly.loop_indices:
        vert_idx = mesh.loops[loop_idx].vertex_index
        z = mesh.vertices[vert_idx].co.z
        r, g, b = elev_to_color(z)
        color_layer.data[loop_idx].color = (r, g, b, 1.0)

# Create a material that uses vertex colors
mat_elev = bpy.data.materials.new(name="ElevationBands")
mat_elev.use_nodes = True
nodes = mat_elev.node_tree.nodes
links = mat_elev.node_tree.links
nodes.clear()

# Vertex color node → Principled BSDF → Output
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

# Add as second material slot (satellite texture stays as first)
terrain.data.materials.append(mat_elev)

# ── 2. Labeled empties at landmarks ──────────────────────────────────

print("Placing landmarks...")

# Create a collection for annotations
if "Annotations" not in bpy.data.collections:
    anno_col = bpy.data.collections.new("Annotations")
    bpy.context.scene.collection.children.link(anno_col)
else:
    anno_col = bpy.data.collections["Annotations"]

for name, lat, lon, known_elev, ltype in LANDMARKS:
    x, y = latlon_to_xy(lat, lon)
    z = find_surface_z(terrain, x, y)
    if z is None:
        z = known_elev if known_elev else 5000
    else:
        # Use known elevation if we have it (SRTM may underestimate)
        if known_elev and known_elev > z:
            z = known_elev

    # Create empty
    empty = bpy.data.objects.new(name.replace('\n', ' '), None)
    empty.location = (x, y, z + 150)  # offset above surface
    empty.empty_display_type = 'PLAIN_AXES' if ltype == 'summit' else 'SPHERE'
    empty.empty_display_size = 300 if ltype == 'cardinal' else 150
    empty.show_name = True
    anno_col.objects.link(empty)

# ── 3. 3D text for summit ────────────────────────────────────────────

print("Adding summit text...")
sx, sy = latlon_to_xy(32.0905, 77.7347)
sz = find_surface_z(terrain, sx, sy)
if sz is None:
    sz = 6570

# Summit marker (vertical line)
curve_data = bpy.data.curves.new('SummitPole', type='CURVE')
curve_data.dimensions = '3D'
spline = curve_data.splines.new('POLY')
spline.points.add(1)  # 2 points total
spline.points[0].co = (0, 0, 0, 1)
spline.points[1].co = (0, 0, 500, 1)
curve_data.bevel_depth = 15
pole = bpy.data.objects.new('SummitPole', curve_data)
pole.location = (sx, sy, sz)
anno_col.objects.link(pole)

# Summit text
font_data = bpy.data.curves.new('SummitText', type='FONT')
font_data.body = "PARVATI PARBAT\n6632 m"
font_data.size = 150
font_data.align_x = 'CENTER'
font_data.extrude = 10
text_obj = bpy.data.objects.new('SummitLabel', font_data)
text_obj.location = (sx, sy, sz + 550)
# Face the text toward the camera (rotate to stand upright)
text_obj.rotation_euler = (math.radians(90), 0, 0)
anno_col.objects.link(text_obj)

# Color the text red
mat_text = bpy.data.materials.new(name="SummitTextMat")
mat_text.diffuse_color = (1.0, 0.2, 0.1, 1.0)
text_obj.data.materials.append(mat_text)

# ── 4. Sun light from NW ─────────────────────────────────────────────

sun_data = bpy.data.lights.new(name="MountainSun", type='SUN')
sun_data.energy = 3.0
sun_data.color = (1.0, 0.95, 0.9)
sun_obj = bpy.data.objects.new("MountainSun", sun_data)
# NW at 45° altitude
sun_obj.rotation_euler = (math.radians(45), math.radians(-15), math.radians(-45))
bpy.context.scene.collection.objects.link(sun_obj)

# ── Viewport setup ────────────────────────────────────────────────────

# Select terrain and frame
terrain.select_set(True)
bpy.context.view_layer.objects.active = terrain

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.clip_end = 100000
                space.shading.type = 'MATERIAL'
                space.overlay.show_extras = True       # show empty names
                space.overlay.show_text = True
        for region in area.regions:
            if region.type == 'WINDOW':
                with bpy.context.temp_override(area=area, region=region):
                    bpy.ops.view3d.view_selected()
                break
        break

print("Done. Annotations in 'Annotations' collection.")
print("Switch materials: select terrain → Material Properties → slot 1 (satellite) or 2 (elevation bands)")
