import bpy

from ..utils import get_scripts
from ..operators.run_script import QSR_OT_RunScript
from ..operators.open_addon_folder import QSR_OT_OpenAddonFolder


class QSR_PT_MainPanel(bpy.types.Panel):
    bl_label = "QSR"
    bl_idname = "QSR_PT_main_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "QSR"

    def draw(self, context):

        layout = self.layout
        wm = context.window_manager

        # -------------------------------------------------
        # TOOLS
        # -------------------------------------------------

        row = layout.row(align=True)

        row.label(text="Tools")

        row.operator(
            QSR_OT_OpenAddonFolder.bl_idname,
            text="",
            icon="FILE_FOLDER",
        )

        layout.separator()

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        row = layout.row(align=True)

        row.prop(
            wm,
            "qsr_category",
            expand=True,
        )

        layout.separator()

        # -------------------------------------------------
        # SCRIPTS
        # -------------------------------------------------

        current_category = wm.qsr_category
        scripts = get_scripts(current_category)

        if not scripts:
            layout.label(text="No scripts found")
            return

        for script in scripts:

            op = layout.operator(
                QSR_OT_RunScript.bl_idname,
                text=script,
                icon="PLAY",
            )

            op.category = current_category
            op.script_name = script
