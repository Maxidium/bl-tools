import bpy
import os

from ..paths import category_dir
from ..utils import delete_file


class QSR_OT_DeleteScript(bpy.types.Operator):
    bl_idname = "qsr.delete_script"
    bl_label = "Delete Script"
    bl_description = "Delete selected script"

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

        delete_file(script_path)

        self.report(
            {'INFO'},
            "Script deleted",
        )

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(
            self,
            event,
        )

    def draw(self, context):
        self.layout.label(text=f"Delete '{self.script_name}'?")