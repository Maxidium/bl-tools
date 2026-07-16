bl_info = {
    "name": "Merginator",
    "author": "Maxidium",
    "version": (2, 0, 0),
    "blender": (5, 1, 0),
    "location": "N-Panel > Merginator",
    "description": "Recursive mesh merge utility",
    "category": "Object",
}

import bpy

from . import properties

from .operators import classes as operator_classes
from .ui import classes as ui_classes


classes = (
    *operator_classes,
    *ui_classes,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    properties.register()


def unregister():

    properties.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()