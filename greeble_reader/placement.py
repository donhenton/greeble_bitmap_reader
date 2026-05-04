"""
Centered anchor placement logic.

reader12 change:
- Each map rectangle places exactly one object.
- The object is placed at the center of the rectangle.
- Rectangle size is treated as design/diagnostic information, not a scatter area.
- Clusters, rhythm, and density are owned by the map image/JSON itself.
- Rotations remain orthogonal only.
- Objects are grounded by world-space bounding-box bottom.
"""

import random
import math
import bpy
from mathutils import Vector

from .config import (
    PANEL_WIDTH,
    PANEL_HEIGHT,
    PANEL_THICKNESS,
    SCALE_RANGE_BY_TYPE,
)


ORTHOGONAL_ROTATIONS = [
    0.0,
    math.pi / 2.0,
    math.pi,
    3.0 * math.pi / 2.0,
]


def region_center_world(region, canvas, offset):
    """
    Convert the center of a JSON region rectangle into world coordinates.
    Image space: x right, y down.
    World space: x right, y up.
    """
    ox, oy, oz = offset

    cx = region["x"] + region["w"] / 2.0
    cy = region["y"] + region["h"] / 2.0

    wx = ox + (cx / canvas["width"] - 0.5) * PANEL_WIDTH
    wy = oy + (0.5 - cy / canvas["height"]) * PANEL_HEIGHT

    # Base sits on top of the physical panel.
    base_z = oz + PANEL_THICKNESS

    return wx, wy, base_z


def ground_object_to_z(obj, target_z):
    """
    Move object so the lowest world-space bounding-box point sits on target_z.
    This does not trust object origin placement.
    """
    bpy.context.view_layer.update()

    lowest_z = min((obj.matrix_world @ Vector(corner)).z for corner in obj.bound_box)
    obj.location.z += target_z - lowest_z

    bpy.context.view_layer.update()


def scatter_region(region, source_collection, output_collection, canvas, offset):
    """
    Historical function name retained so runner.py does not need to change.
    In reader12, this places one object at the region center.
    """
    region_type = region["type"]

    source_objects = list(source_collection.objects)
    source = random.choice(source_objects)

    new = source.copy()
    new.data = source.data.copy()

    scale_min, scale_max = SCALE_RANGE_BY_TYPE[region_type]
    s = random.uniform(scale_min, scale_max)
    new.scale = (s, s, s)

    new.rotation_euler = (0.0, 0.0, random.choice(ORTHOGONAL_ROTATIONS))

    wx, wy, base_z = region_center_world(region, canvas, offset)

    bpy.context.scene.collection.objects.link(new)
    bpy.context.view_layer.update()

    new.location = (wx, wy, base_z)
    bpy.context.view_layer.update()
    ground_object_to_z(new, base_z)

    output_collection.objects.link(new)
    bpy.context.scene.collection.objects.unlink(new)
