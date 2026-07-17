import bpy

from ..utils.collections import iter_mesh_objects


def apply_modifiers(collection, ignore_armature=True):
    """
    Apply object modifiers.
    """

    previous_active = bpy.context.view_layer.objects.active

    bpy.ops.object.select_all(action="DESELECT")

    for obj in iter_mesh_objects(collection):

        if len(obj.modifiers) == 0:
            continue

        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        for modifier in list(obj.modifiers):

            if (ignore_armature and modifier.type == "ARMATURE"):
                continue

            try:
                bpy.ops.object.modifier_apply(modifier=modifier.name)

            except RuntimeError:
                pass

        obj.select_set(False)

    bpy.context.view_layer.objects.active = previous_active