import bpy

from ..utils.collections import iter_mesh_objects


def build_name(settings, parent_collection, child_collection, index):
    """
    Build object or collection name.
    """

    if settings.use_auto_name:

        prefix = child_collection.name.removesuffix(
            f" - {parent_collection.name}"
        )

        return f"{parent_collection.name}_{prefix}"

    try:
        return settings.custom_name.format(i=index)

    except (KeyError, IndexError, ValueError):
        return f"{parent_collection.name}_{index:02d}"


def rename_collections(collection, settings):
    """
    Rename child collections.
    """

    for index, child_collection in enumerate(collection.children):

        child_collection.name = build_name(
            settings,
            collection,
            child_collection,
            index,
        )


def rename_objects(collection, settings):
    """
    Rename mesh objects inside child collections.
    """

    for child_collection in collection.children:

        for index, obj in enumerate(iter_mesh_objects(child_collection)):

            obj.name = build_name(
                settings,
                collection,
                child_collection,
                index,
            )