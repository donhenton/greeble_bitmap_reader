"""
Map loading and pairing.
"""

import os
import json


def find_json_maps(maps_dir):
    files = [f for f in os.listdir(maps_dir) if f.endswith(".json")]
    files.sort()
    if not files:
        raise RuntimeError("No JSON maps found in generated_maps.")
    return files


def choose_map(maps_dir, map_index):
    maps = find_json_maps(maps_dir)

    if map_index < 0 or map_index >= len(maps):
        raise RuntimeError("MAP_INDEX is out of range. Found " + str(len(maps)) + " map files.")

    json_name = maps[map_index]
    json_path = os.path.join(maps_dir, json_name)
    png_path = os.path.splitext(json_path)[0] + ".png"

    if not os.path.exists(png_path):
        raise RuntimeError("Missing matching PNG for " + json_name)

    return json_name, json_path, png_path


def load_map_json(json_path):
    with open(json_path, "r") as f:
        return json.load(f)
