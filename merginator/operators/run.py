import bpy

from .join import join_meshes
from .rename import rename_objects
from .move_to_parent import move_objects_to_parent
from .move_to_parent import remove_empty_children
from .select_result import select_objects

class MERGINATOR_OT_Run(bpy.types.Operator):
    bl_idname = "merginator.run"
    bl_label = "Merginate"
    bl_description = "Run Merginator"

    def execute(self, context):

        settings = context.window_manager.merginator
        collection = context.collection

        if collection is None:
            self.report({'ERROR'},"No active collection",)
            return {'CANCELLED'}
        

        if settings.join_meshes:
            join_meshes(context,collection,)

        if settings.rename:
            rename_objects(collection,settings,)

        if settings.move_to_parent:
            move_objects_to_parent(collection)
            remove_empty_children(collection)

        if settings.select_result:
            select_objects(collection)


        self.report({'INFO'},"MERGINATED!",)

        return {'FINISHED'}