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

        # --------------------------------------------------
        # Utilities
        # --------------------------------------------------

        box = layout.box()
        row = box.row(align=True)

        row.operator("merginator.group_by_materials",icon="OUTLINER_OB_GROUP_INSTANCE",)
        row.separator(factor=0.8)
        row.operator("merginator.move_to_parent",text="Flatten Collections",icon="AREA_JOIN_UP",)

        # --------------------------------------------------
        # Pipeline
        # --------------------------------------------------

        layout.separator()

        box = layout.box()

        box.prop(settings,"join_meshes",)

        box.prop(settings, "rename")

        if settings.rename:
            rename_box = box.box()

            row = rename_box.row()
            row.prop(settings, "name_mode", expand=True)

            if settings.name_mode == "AUTO":
                rename_box.prop(settings, "order_index",text="Index")
            else:
                rename_box.prop(settings, "custom_name",text="Pattern")

        box.prop(settings, "move_to_parent", text="Flatten Collection")
        box.prop(settings, "select_result")

        # --------------------------------------------------
        # Run
        # --------------------------------------------------

        layout.operator("merginator.run",text="Merginate",)