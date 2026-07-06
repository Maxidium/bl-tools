import bpy

from ..utils import (
    get_scripts,
    script_label,
)

from ..operators.run_script import QSR_OT_RunScript
from ..operators.open_scripts_folder import QSR_OT_OpenScriptsFolder
from ..operators.add_script import QSR_OT_AddScript
from ..operators.edit_script import QSR_OT_EditScript
from ..operators.delete_script import QSR_OT_DeleteScript
from ..operators.new_script import QSR_OT_NewScript

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

        row.operator(
            QSR_OT_OpenScriptsFolder.bl_idname,
            text="Open Scripts Folder",
            icon="FILE_FOLDER",
        )

        op = row.operator(
            QSR_OT_AddScript.bl_idname,
            text="Add script",
            icon="ADD",
        )

        op.category = wm.qsr_category

        op = row.operator(
            QSR_OT_NewScript.bl_idname,
            text="",
            icon="FILE_NEW",
        )

        op.category = wm.qsr_category

        layout.separator()

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        layout.label(text="Category")
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

            row = layout.row(align=True)

            op = row.operator(
                QSR_OT_RunScript.bl_idname,
                text=script_label(script),
                icon="PLAY",
            )

            op.category = current_category
            op.script_name = script

            op = row.operator(
                QSR_OT_EditScript.bl_idname,
                text="",
                icon="GREASEPENCIL",
            )

            op.category = current_category
            op.script_name = script

            op = row.operator(
                QSR_OT_DeleteScript.bl_idname,
                text="",
                icon="TRASH",
            )

            op.category = current_category
            op.script_name = script
