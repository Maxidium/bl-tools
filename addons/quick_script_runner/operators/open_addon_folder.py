import bpy
import os
import subprocess
import sys

from ..paths import addon_dir


class QSR_OT_OpenAddonFolder(bpy.types.Operator):
    bl_idname = "qsr.open_addon_folder"
    bl_label = "Open Addon Folder"
    bl_description = "Open the add-on folder"

    def execute(self, context):

        path = addon_dir()

        if sys.platform == "win32":
            os.startfile(path)

        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])

        else:
            subprocess.Popen(["xdg-open", path])

        return {'FINISHED'}
