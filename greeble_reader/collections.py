"""
Collection helpers.
"""

import bpy


def require_collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        raise RuntimeError("Missing required collection: " + name)
    if len(col.objects) == 0:
        raise RuntimeError("Required collection is empty: " + name)
    return col


def create_or_clear_scene_child_collection(name):
    """
    Create or clear a collection linked directly under the scene collection.
    """
    existing = bpy.data.collections.get(name)
    if existing:
        for obj in list(existing.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

        # Ensure linked under scene collection.
        if existing.name not in [c.name for c in bpy.context.scene.collection.children]:
            try:
                bpy.context.scene.collection.children.link(existing)
            except RuntimeError:
                pass

        return existing

    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def create_or_clear_child_collection(name, parent_collection):
    """
    Create or clear a child collection under a supplied parent collection.
    """
    existing = bpy.data.collections.get(name)
    if existing:
        for obj in list(existing.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

        if existing.name not in [c.name for c in parent_collection.children]:
            try:
                parent_collection.children.link(existing)
            except RuntimeError:
                pass

        return existing

    col = bpy.data.collections.new(name)
    parent_collection.children.link(col)
    return col


def link_object_to_collection_only(obj, collection):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)
    collection.objects.link(obj)
