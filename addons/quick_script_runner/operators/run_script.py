import os
import runpy

import bpy

from ..paths import category_dir


class QSR_OT_RunScript(bpy.types.Operator):
    bl_idname = "qsr.run_script"
    bl_label = "Run Script"

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

        try:
            runpy.run_path(
                script_path,
                run_name="__main__",
            )

            self.report(
                {'INFO'},
                f"Executed: {self.script_name}",
            )

        except Exception as e:

            self.report({'ERROR'}, str(e))
            print(f"[QSR ERROR] {e}")

            return {'CANCELLED'}

        return {'FINISHED'}
