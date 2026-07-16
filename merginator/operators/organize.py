import bpy

from ..utils.collections import iter_mesh_objects


def move_objects_to_parent(collection):
    """
    Move all mesh objects from child collections
    into the active collection.

    Empty child collections are removed.
    """

    objects = list(iter_mesh_objects(collection))


    # Move objects
    for obj in objects:

        # Already in parent collection
        if collection in obj.users_collection:
            continue

        for old_collection in list(obj.users_collection):
            old_collection.objects.unlink(obj)

        collection.objects.link(obj)


    # Remove empty child collections
    remove_empty_children(collection)



def remove_empty_children(collection):
    """
    Remove empty child collections recursively.
    """

    for child in list(collection.children):

        remove_empty_children(child)


        if (
            len(child.objects) == 0
            and len(child.children) == 0
        ):
            bpy.data.collections.remove(child)



class MERGINATOR_OT_MoveToParent(bpy.types.Operator):

    bl_idname = "merginator.move_to_parent"
    bl_label = "Move Objects to Parent"
    bl_description = "Move all objects into the active collection"

    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        collection = (
            context
            .view_layer
            .active_layer_collection
            .collection
        )

        move_objects_to_parent(collection)

        self.report({'INFO'},"Objects moved to parent collection")

        return {'FINISHED'}