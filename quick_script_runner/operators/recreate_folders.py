import bpy

from ..paths import ensure_category_dirs


class QSR_OT_RecreateFolders(bpy.types.Operator):
    bl_idname = "qsr.recreate_folders"
    bl_label = "Recreate Folders"
    bl_description = "Recreate missing category folders"

    def execute(self, context):

        ensure_category_dirs()

        self.report(
            {'INFO'},
            "Category folders recreated",
        )

        return {'FINISHED'}