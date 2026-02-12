"""Blender 5.x: import expanded valley mesh and set up viewport.

Usage: blender --python parbati/blender_5_expanded.py
"""
import bpy

# Remove default objects
for name in ["Cube", "Light", "Camera"]:
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

# Import the expanded OBJ (Blender 4.0+ API)
bpy.ops.wm.obj_import(
    filepath="/home/muchu/Darshan/research/develop/agentic/mayalucia/parbati/data/meshes/expanded.obj"
)

# Select the terrain mesh
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    else:
        obj.select_set(False)

# Set viewport clip distance, material preview, and frame selection
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.clip_end = 200000
                space.shading.type = 'MATERIAL'
        for region in area.regions:
            if region.type == 'WINDOW':
                with bpy.context.temp_override(area=area, region=region):
                    bpy.ops.view3d.view_selected()
                break
        break
