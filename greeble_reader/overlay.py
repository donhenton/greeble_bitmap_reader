"""
Debug overlay creation.
"""

import bpy
from .config import PANEL_WIDTH, PANEL_HEIGHT, PANEL_THICKNESS, OVERLAY_CLEARANCE
from .collections import link_object_to_collection_only


def create_overlay(name, image_path, location, collection):
    x, y, z = location
    overlay_z = z + PANEL_THICKNESS + OVERLAY_CLEARANCE

    bpy.ops.mesh.primitive_plane_add(size=PANEL_WIDTH, location=(x, y, overlay_z))
    overlay = bpy.context.active_object
    overlay.name = name
    overlay.scale[1] = PANEL_HEIGHT / PANEL_WIDTH

    mat = bpy.data.materials.new(name=name + "_Mat")
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for node in list(nodes):
        nodes.remove(node)

    tex = nodes.new(type="ShaderNodeTexImage")
    tex.image = bpy.data.images.load(image_path)

    emission = nodes.new(type="ShaderNodeEmission")
    output = nodes.new(type="ShaderNodeOutputMaterial")

    links.new(tex.outputs["Color"], emission.inputs["Color"])
    links.new(emission.outputs["Emission"], output.inputs["Surface"])

    overlay.data.materials.append(mat)
    link_object_to_collection_only(overlay, collection)
    return overlay
