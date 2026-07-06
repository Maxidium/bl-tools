import bpy
import os
import sys
import subprocess

from ..paths import addon_dir


class QSR_OT_OpenConfig(bpy.types.Operator):
    bl_idname = "qsr.open_config"
    bl_label = "Open Config"
    bl_description = "Open config.py"

    def execute(self, context):

        path = os.path.join(addon_dir(), "config.py")

        if not os.path.isfile(path):
            self.report({'ERROR'}, "config.py not found")
            return {'CANCELLED'}

        if sys.platform == "win32":
            os.startfile(path)

        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])

        else:
            subprocess.Popen(["xdg-open", path])

        return {'FINISHED'}