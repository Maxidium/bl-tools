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
from ..operators.recreate_folders import QSR_OT_RecreateFolders
from ..operators.rename_script import QSR_OT_RenameScript
from ..operators.open_config import QSR_OT_OpenConfig

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

        box = layout.box()

        row = box.row(align=True)

        row.operator(
            QSR_OT_OpenScriptsFolder.bl_idname,
            text="Scripts Directory",
            icon="FILE_FOLDER",
        )

        row.separator(factor=0.8)

        row.operator(
            QSR_OT_RecreateFolders.bl_idname,
            text="",
            icon="FILE_REFRESH",
        )

        row.separator(factor=0.8)

        op = row.operator(
            QSR_OT_NewScript.bl_idname,
            text="",
            icon="FILE_NEW",
        )
        op.category = wm.qsr_category

        op = row.operator(
            QSR_OT_AddScript.bl_idname,
            text="",
            icon="IMPORT",
        )
        op.category = wm.qsr_category

        row.separator(factor=0.8)

        row.operator(
            QSR_OT_OpenConfig.bl_idname,
            text="",
            icon="PREFERENCES",
        )        

        layout.separator()

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        box = layout.box()

        row = box.row(align=True)
        row.prop(
            wm,
            "qsr_category",
            expand=True,
        )

        # -------------------------------------------------
        # SCRIPTS
        # -------------------------------------------------
        
        current_category = wm.qsr_category
        scripts = get_scripts(current_category)

        if scripts is None:
            box.label(
                text="Category folder is missing",
                icon="ERROR",
            )
            return

        if not scripts:
            box.label(
                text="No scripts found",
                icon="INFO",
            )
            return

        col = box.column(align=True)

        for script in scripts:

            row = col.row(align=True)

            op = row.operator(
                QSR_OT_RunScript.bl_idname,
                text=script_label(script),
                icon="PLAY",
            )
            op.category = current_category
            op.script_name = script

            row.separator(factor=0.8)

            op = row.operator(
                QSR_OT_RenameScript.bl_idname,
                text="",
                icon="FILE_TEXT",
            )
            op.category = current_category
            op.script_name = script            

            row.separator(factor=0.8)

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