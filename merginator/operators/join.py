import bpy

from ..utils.collections import get_mesh_objects


def join_meshes(context, collection):
    """
    Recursively join mesh objects inside child collections.
    """

    for child_collection in collection.children[:]:

        # Process nested collections first.
        join_meshes(
            context,
            child_collection,
        )

        mesh_objects = get_mesh_objects(
            child_collection,
        )

        if not mesh_objects:
            continue

        if len(mesh_objects) == 1:
            remove_child_collections(
                child_collection,
            )
            continue

        join_objects(
            context,
            mesh_objects,
        )

        remove_child_collections(
            child_collection,
        )


def join_objects(context, objects):
    """
    Join mesh objects into a single object.
    """

    bpy.ops.object.select_all(
        action='DESELECT',
    )

    for obj in objects:
        obj.select_set(True)

    context.view_layer.objects.active = objects[0]

    bpy.ops.object.join()


def remove_child_collections(collection):
    """
    Remove all nested child collections.
    """

    for child_collection in collection.children[:]:
        bpy.data.collections.remove(
            child_collection,
        )