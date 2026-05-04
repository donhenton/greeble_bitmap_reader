"""
Scene object creation.
"""

import bpy
from .config import PANEL_WIDTH, PANEL_HEIGHT, PANEL_THICKNESS
from .collections import link_object_to_collection_only


def create_panel_material():
    """
    Neutral panel material that should not hide the colored/debug objects.
    """
    mat = bpy.data.materials.get("MAT_Generated_Panel_Neutral")
    if mat is None:
        mat = bpy.data.materials.new("MAT_Generated_Panel_Neutral")

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for node in list(nodes):
        nodes.remove(node)

    principled = nodes.new(type="ShaderNodeBsdfPrincipled")
    principled.inputs["Base Color"].default_value = (0.28, 0.28, 0.30, 1.0)
    principled.inputs["Roughness"].default_value = 0.72

    output = nodes.new(type="ShaderNodeOutputMaterial")
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])

    return mat


def create_panel(name, location, collection):
    """
    Create a real box panel instead of a zero-thickness plane.

    The panel is centered on location in X/Y.
    Its bottom is at location.z.
    Its top is at location.z + PANEL_THICKNESS.
    """
    x, y, z = location
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, y, z + PANEL_THICKNESS / 2.0),
    )
    panel = bpy.context.active_object
    panel.name = name
    panel.dimensions = (PANEL_WIDTH, PANEL_HEIGHT, PANEL_THICKNESS)
    bpy.context.view_layer.update()
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    panel.data.materials.append(create_panel_material())

    link_object_to_collection_only(panel, collection)
    return panel


def panel_top_z(offset):
    return offset[2] + PANEL_THICKNESS
