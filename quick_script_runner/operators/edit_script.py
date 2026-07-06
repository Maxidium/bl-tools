import bpy
import os

from ..paths import category_dir
from ..utils import open_path


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

        open_path(script_path)

        return {'FINISHED'}