bl_info = {
    "name": "QSR - Quick Script Runner",
    "author": "GPT",
    "version": (1, 0, 0),
    "blender": (5, 1, 0),
    "location": "View3D > N-Panel > QSR",
    "description": "Quick categorized script runner",
    "category": "Development",
}

import bpy

from .config import (
    CATEGORIES,
    CATEGORY_FOLDERS,
)
from .paths import category_dir

from .operators import classes as operator_classes
from .ui import classes as ui_classes


classes = (
    *operator_classes,
    *ui_classes,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.qsr_category = bpy.props.EnumProperty(
        name="Category",
        items=CATEGORIES,
        default="MESH",
    )

    for category in CATEGORY_FOLDERS:
        category_dir(category)


def unregister():

    del bpy.types.WindowManager.qsr_category

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
