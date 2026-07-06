import bpy

from ..paths import scripts_root
from ..utils import open_path


class QSR_OT_OpenScriptsFolder(bpy.types.Operator):
    bl_idname = "qsr.open_scripts_folder"
    bl_label = "Open Scripts Folder"
    bl_description = "Open scripts folder"

    def execute(self, context):

        open_path(scripts_root(),)

        return {'FINISHED'}