"""
Top-level reader orchestration.
"""

import os

from .paths import get_maps_dir
from .maps import choose_map, load_map_json, find_json_maps
from .scene import create_panel
from .overlay import create_overlay
from .collections import (
    require_collection,
    create_or_clear_scene_child_collection,
    create_or_clear_child_collection,
)
from .placement import scatter_region
from .config import COLLECTION_BY_TYPE
from .grid import grid_position


PARENT_COLLECTION_NAME = "Generated_Example_Grid"


def run_single_example(map_index, example_index, source_collections, maps_dir, parent_collection):
    map_file, json_path, png_path = choose_map(maps_dir, map_index)
    map_data = load_map_json(json_path)

    map_base = os.path.splitext(map_file)[0]
    example_name = "Example_" + str(example_index + 1).zfill(2) + "_" + map_base
    output_collection = create_or_clear_child_collection(example_name, parent_collection)

    offset = grid_position(example_index)

    create_panel(example_name + "_Target_Panel", offset, output_collection)
    create_overlay(example_name + "_Overlay_Map", png_path, offset, output_collection)

    for region in map_data["regions"]:
        region_type = region["type"]
        if region_type not in source_collections:
            continue

        scatter_region(
            region=region,
            source_collection=source_collections[region_type],
            output_collection=output_collection,
            canvas=map_data["canvas"],
            offset=offset,
        )

    print("Generated example:", example_name)


def run_reader_grid(start_map_index=0, example_count=5):
    maps_dir = get_maps_dir()
    maps = find_json_maps(maps_dir)

    if start_map_index < 0:
        raise RuntimeError("START_MAP_INDEX must be 0 or greater.")

    if start_map_index + example_count > len(maps):
        raise RuntimeError(
            "Not enough maps. Requested "
            + str(example_count)
            + " starting at "
            + str(start_map_index)
            + ", but only found "
            + str(len(maps))
            + "."
        )

    parent_collection = create_or_clear_scene_child_collection(PARENT_COLLECTION_NAME)

    source_collections = {
        region_type: require_collection(collection_name)
        for region_type, collection_name in COLLECTION_BY_TYPE.items()
    }

    for i in range(example_count):
        run_single_example(
            map_index=start_map_index + i,
            example_index=i,
            source_collections=source_collections,
            maps_dir=maps_dir,
            parent_collection=parent_collection,
        )

    print("Generated", example_count, "grid examples in collection:", PARENT_COLLECTION_NAME)
