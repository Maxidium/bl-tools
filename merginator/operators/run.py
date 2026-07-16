import bpy


class MERGINATOR_OT_Run(bpy.types.Operator):
    bl_idname = "merginator.run"
    bl_label = "Merginate"
    bl_description = "Run Merginator"

    def execute(self, context):

        settings = context.window_manager.merginator

        self.report(
            {'INFO'},
            "Coming soon",
        )

        return {'FINISHED'}