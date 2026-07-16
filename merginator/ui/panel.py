import bpy


class MERGINATOR_PT_Main(bpy.types.Panel):
    bl_label = "Merginator"
    bl_idname = "MERGINATOR_PT_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Merginator"

    def draw(self, context):

        layout = self.layout
        settings = context.window_manager.merginator

        layout.prop(settings, "join_meshes")
        layout.prop(settings, "rename_objects")
        #layout.prop(settings, "triangulate")
        #layout.prop(settings, "select_result")

        layout.operator(
            "merginator.run",
            text="Merginate",
        )