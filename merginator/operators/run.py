import bpy

from .join import join_meshes

class MERGINATOR_OT_Run(bpy.types.Operator):
    bl_idname = "merginator.run"
    bl_label = "Merginate"
    bl_description = "Run Merginator"

    def execute(self, context):

        settings = context.window_manager.merginator
        collection = context.collection

        if collection is None:
            self.report(
                {'ERROR'},
                "No active collection",
            )
            return {'CANCELLED'}

        if settings.join_meshes:
            join_meshes(context,collection,)

        if settings.rename_objects:
            pass

        if settings.triangulate:
            pass

        if settings.select_result:
            pass


        # button

        self.report(
            {'INFO'},
            "Merginated!",
        )

        return {'FINISHED'}