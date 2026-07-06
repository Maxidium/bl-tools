import bpy
import subprocess
import sys
import os

from ..paths import scripts_root


class QSR_OT_OpenScriptsFolder(bpy.types.Operator):
    bl_idname = "qsr.open_scripts_folder"
    bl_label = "Open Scripts Folder"
    bl_description = "Open current scripts folder"

    def execute(self, context):

        path = scripts_root()

        if sys.platform == "win32":
            os.startfile(path)

        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])

        else:
            subprocess.Popen(["xdg-open", path])

        return {'FINISHED'}