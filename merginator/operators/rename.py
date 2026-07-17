import bpy

from ..utils.collections import iter_mesh_objects


def format_object_name(settings, parent_collection, child_collection, index):
    """
    Build object name.
    """

    group = child_collection.name.removesuffix(
        f" - {parent_collection.name}"
    )

    if settings.name_mode == "AUTO":

        match settings.order_index:

            case "NONE":
                return f"{parent_collection.name}_{group}"

            case "BEFORE_COLLECTION":
                return f"{index:02d}_{parent_collection.name}_{group}"

            case "BEFORE_GROUP":
                return f"{parent_collection.name}_{index:02d}_{group}"

            case "AFTER_GROUP":
                return f"{parent_collection.name}_{group}_{index:02d}"

    try:
        return settings.custom_name.format(i=index)

    except (KeyError, IndexError, ValueError):
        return f"{parent_collection.name}_{index:02d}"


def rename_objects(collection, settings):
    """
    Rename mesh objects inside child collections.
    """

    index = 0

    for child_collection in collection.children:

        for obj in iter_mesh_objects(child_collection):

            obj.name = format_object_name(
                settings,
                collection,
                child_collection,
                index,
            )

            index += 1