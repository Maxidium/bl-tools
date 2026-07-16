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


        # -------------------------------------------------
        # MAIN
        # -------------------------------------------------

        box = layout.box()
        box.label(text="Merginator")

        box.prop(settings,"join_meshes",)

        box.prop(settings, "rename")
        if settings.rename:
            rename_box = box.box()
            rename_box.prop(settings,"custom_name",)
            rename_box.prop(settings,"use_collection_prefix",)

        #box.prop(settings,"triangulate",)
        #box.prop(settings,"select_result",)

        box.operator("merginator.run",text="Merginate",)

        # -------------------------------------------------
        # UTILITIES
        # -------------------------------------------------

        utility_box = layout.box()

        utility_box.label(
            text="Utilities"
        )

        utility_box.operator(
            "merginator.group_materials",
            text="Group by Material",
        )

        utility_box.operator(
            "merginator.move_to_parent",
            text="Move Objects to Parent",
        )