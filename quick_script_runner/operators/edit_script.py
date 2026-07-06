import bpy
import os
import subprocess
import sys

from ..paths import category_dir


class QSR_OT_EditScript(bpy.types.Operator):
    bl_idname = "qsr.edit_script"
    bl_label = "Edit Script"
    bl_description = "Open the script in the default editor"

    category: bpy.props.StringProperty()
    script_name: bpy.props.StringProperty()

    def execute(self, context):

        script_path = os.path.join(
            category_dir(self.category),
            self.script_name,
        )

        if not os.path.isfile(script_path):
            self.report({'ERROR'}, "Script not found")
            return {'CANCELLED'}

        if sys.platform == "win32":
            os.startfile(script_path)

        elif sys.platform == "darwin":
            subprocess.Popen(["open", script_path])

        else:
            subprocess.Popen(["xdg-open", script_path])

        return {'FINISHED'}