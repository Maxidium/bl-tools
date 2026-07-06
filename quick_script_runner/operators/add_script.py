import bpy
import os

from bpy_extras.io_utils import ImportHelper

from ..paths import category_dir
from ..utils import copy_file


class QSR_OT_AddScript(bpy.types.Operator, ImportHelper):
    bl_idname = "qsr.add_script"
    bl_label = "Add Script"
    bl_description = "Add a Python script to the current category"

    filename_ext = ".py"

    filter_glob: bpy.props.StringProperty(
        default="*.py",
        options={'HIDDEN'},
    )

    category: bpy.props.StringProperty()

    def execute(self, context):

        destination = os.path.join(
            category_dir(self.category),
            os.path.basename(self.filepath),
        )

        if os.path.exists(destination):
            self.report({'ERROR'}, "Script already exists")
            return {'CANCELLED'}

        copy_file(self.filepath,destination,)

        self.report(
            {'INFO'},
            "Script added",
        )

        return {'FINISHED'}