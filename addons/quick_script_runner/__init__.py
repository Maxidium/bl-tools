bl_info = {
    "name": "QSR - Quick Script Runner",
    "author": "ChatGPT",
    "version": (1, 0, 0),
    "blender": (5, 1, 0),
    "location": "View3D > N-Panel > QSR",
    "description": "Quick categorized script runner",
    "category": "Development",
}

import bpy
import os
import runpy

# =========================================================
# CONFIG
# =========================================================

CATEGORIES = [
    ("MESH", "Mesh", ""),
    ("RIG", "Rig", ""),
    ("UV", "UV", ""),
    ("UTILITY", "Utility", ""),
    ("MISC", "Misc", ""),
]

CATEGORY_FOLDERS = {
    "MESH": "mesh",
    "RIG": "rig",
    "UV": "uv",
    "UTILITY": "utility",
    "MISC": "misc",
}


# =========================================================
# PATHS
# =========================================================

def addon_dir():
    return os.path.dirname(__file__)


def scripts_root():
    return os.path.join(addon_dir(), "scripts")


def category_dir(category):

    folder = CATEGORY_FOLDERS.get(category, "misc")

    path = os.path.join(
        scripts_root(),
        folder
    )

    os.makedirs(path, exist_ok=True)

    return path


# =========================================================
# SCRIPT LIST
# =========================================================

def get_scripts(category):

    path = category_dir(category)

    scripts = []

    for file in os.listdir(path):

        if file.endswith(".py"):
            scripts.append(file)

    scripts.sort()

    return scripts


# =========================================================
# OPERATOR
# =========================================================

class QSR_OT_RunScript(bpy.types.Operator):
    bl_idname = "qsr.run_script"
    bl_label = "Run Script"

    category: bpy.props.StringProperty()
    script_name: bpy.props.StringProperty()

    def execute(self, context):

        script_path = os.path.join(
            category_dir(self.category),
            self.script_name
        )

        if not os.path.isfile(script_path):
            self.report({'ERROR'}, "Script not found")
            return {'CANCELLED'}

        try:
            runpy.run_path(script_path, run_name="__main__")

            self.report(
                {'INFO'},
                f"Executed: {self.script_name}"
            )

        except Exception as e:

            self.report({'ERROR'}, str(e))
            print(f"[QSR ERROR] {e}")

            return {'CANCELLED'}

        return {'FINISHED'}


# =========================================================
# UI PANEL
# =========================================================

class QSR_PT_MainPanel(bpy.types.Panel):
    bl_label = "QSR"
    bl_idname = "QSR_PT_main_panel"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "QSR"

    def draw(self, context):

        layout = self.layout
        wm = context.window_manager

        # -------------------------------------------------
        # TOP CATEGORY TABS
        # -------------------------------------------------

        row = layout.row(align=True)

        row.prop(wm, "qsr_category", expand=True)

        layout.separator()

        # -------------------------------------------------
        # CURRENT CATEGORY SCRIPTS
        # -------------------------------------------------

        current_category = wm.qsr_category

        scripts = get_scripts(current_category)

        if not scripts:
            layout.label(text="No scripts found")
            return

        for script in scripts:

            op = layout.operator(
                QSR_OT_RunScript.bl_idname,
                text=script,
                icon='PLAY'
            )

            op.category = current_category
            op.script_name = script


# =========================================================
# REGISTER
# =========================================================

classes = (
    QSR_OT_RunScript,
    QSR_PT_MainPanel,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.qsr_category = bpy.props.EnumProperty(
        name="Category",
        items=CATEGORIES,
        default="MESH"
    )

    # Auto-create folders
    for category in CATEGORY_FOLDERS.keys():
        category_dir(category)


def unregister():

    del bpy.types.WindowManager.qsr_category

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
