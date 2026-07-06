import bpy
import os

from ..paths import category_dir
from ..config import SCRIPT_EXTENSION
from ..utils import rename_file


class QSR_OT_RenameScript(bpy.types.Operator):
    bl_idname = "qsr.rename_script"
    bl_label = "Rename Script"
    bl_description = "Rename selected script"

    category: bpy.props.StringProperty()
    script_name: bpy.props.StringProperty()

    new_name: bpy.props.StringProperty(
        name="New Name",
        default="",
    )

    def invoke(self, context, event):

        name = self.script_name.removesuffix(SCRIPT_EXTENSION)
        self.new_name = name

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):

        layout = self.layout
        layout.prop(self, "new_name")

    def execute(self, context):

        filename = self.new_name.strip()

        if not filename:
            self.report({'ERROR'}, "Name cannot be empty")
            return {'CANCELLED'}

        if not filename.endswith(SCRIPT_EXTENSION):
            filename += SCRIPT_EXTENSION

        old_path = os.path.join(
            category_dir(self.category),
            self.script_name,
        )

        new_path = os.path.join(
            category_dir(self.category),
            filename,
        )

        if not os.path.isfile(old_path):
            self.report({'ERROR'}, "Script not found")
            return {'CANCELLED'}

        if os.path.exists(new_path):
            self.report({'ERROR'}, "Script already exists")
            return {'CANCELLED'}

        rename_file(old_path, new_path)

        self.report({'INFO'}, f"Renamed to: {filename}")

        return {'FINISHED'}