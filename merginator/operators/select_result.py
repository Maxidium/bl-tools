import bpy

from ..utils.collections import iter_mesh_objects


def select_objects(collection):
    """
    Select all mesh objects in collection.
    """

    bpy.ops.object.select_all(action='DESELECT')

    active = None

    for obj in iter_mesh_objects(collection):

        obj.select_set(True)

        if active is None:
            active = obj

    if active:
        bpy.context.view_layer.objects.active = active