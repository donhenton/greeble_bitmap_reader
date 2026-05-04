"""
Entry point for greeble_reader12.

Open this file in Blender's Text Editor and run it.
The package folder must sit next to this file.

This version generates 5 examples from generated_maps into one parent scene collection and spaces them
on a 2 x 3 grid with one empty slot.
"""

import os
import sys
import bpy

START_MAP_INDEX = 0
EXAMPLE_COUNT = 10


def add_local_package_path():
    """
    Resolve imports from the active Blender text block filepath.
    This follows the project convention used throughout this Blender work.
    """
    text = getattr(bpy.context.space_data, "text", None)
    if text and text.filepath:
        base_dir = os.path.dirname(text.filepath)
    else:
        base_dir = os.path.dirname(bpy.data.filepath)

    if base_dir and base_dir not in sys.path:
        sys.path.append(base_dir)


def main():
    add_local_package_path()

    from greeble_reader.runner import run_reader_grid

    run_reader_grid(
        start_map_index=START_MAP_INDEX,
        example_count=EXAMPLE_COUNT,
    )


if __name__ == "__main__":
    main()
