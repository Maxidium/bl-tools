import bpy
import os

from ..paths import category_dir
from ..utils import (create_file, open_path,)


class QSR_OT_NewScript(bpy.types.Operator):
    bl_idname = "qsr.new_script"
    bl_label = "New Script"
    bl_description = "Create a new script"

    category: bpy.props.StringProperty()

    script_name: bpy.props.StringProperty(
        name="Script Name",
        default="new_script.py",
    )

    def invoke(self, context, event):

        self.script_name = "new_script.py"

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):

        layout = self.layout

        layout.prop(
            self,
            "script_name",
        )

    def execute(self, context):

        filename = self.script_name.strip()

        if not filename:
            self.report({'ERROR'}, "Script name cannot be empty")
            return {'CANCELLED'}

        if not filename.endswith(".py"):
            filename += ".py"

        script_path = os.path.join(
            category_dir(self.category),
            filename,
        )

        if os.path.exists(script_path):
            self.report({'ERROR'}, "Script already exists")
            return {'CANCELLED'}

        create_file(script_path)
        
        open_path(script_path)

        self.report(
            {'INFO'},
            f"Created: {filename}",
        )

        return {'FINISHED'}