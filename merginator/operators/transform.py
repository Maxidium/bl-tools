import bpy

from ..utils.collections import iter_mesh_objects


def apply_all_transforms(collection):
    """
    Apply all transforms to mesh objects.
    """

    previous_active = bpy.context.view_layer.objects.active

    bpy.ops.object.select_all(action="DESELECT")

    for obj in iter_mesh_objects(collection):

        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        bpy.ops.object.transform_apply(
            location=True,
            rotation=True,
            scale=True,
        )

        obj.select_set(False)

    bpy.context.view_layer.objects.active = previous_active