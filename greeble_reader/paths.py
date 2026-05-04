"""
Path helpers.
"""

import os
import bpy


def get_blend_dir():
    blend_path = bpy.data.filepath
    if not blend_path:
        raise RuntimeError("Save the .blend file before running this script.")
    return os.path.dirname(blend_path)


def get_maps_dir():
    maps_dir = os.path.join(get_blend_dir(), "generated_maps")
    if not os.path.isdir(maps_dir):
        raise RuntimeError("Could not find generated_maps folder next to the .blend file.")
    return maps_dir
