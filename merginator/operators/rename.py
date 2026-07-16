import bpy

from ..utils.collections import iter_mesh_objects


def build_name(settings, prefix, index):
    """
    Build object or collection name.
    """

    if settings.use_collection_prefix:
        return f"{prefix}_{index:02d}"

    try:
        return settings.custom_name.format(i=index)

    except (KeyError, IndexError, ValueError):
        return f"{prefix}_{index:02d}"


def rename_collections(collection, settings):
    """
    Rename direct child collections.
    """

    for index, child_collection in enumerate(collection.children):

        child_collection.name = build_name(
            settings,
            collection.name,
            index,
        )


def rename_objects(collection, settings):
    """
    Rename mesh objects recursively.
    """

    for index, obj in enumerate(iter_mesh_objects(collection)):

        obj.name = build_name(
            settings,
            collection.name,
            index,
        )