import bpy


class MerginatorProperties(bpy.types.PropertyGroup):
    pass


classes = (
    MerginatorProperties,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.merginator = bpy.props.PointerProperty(
        type=MerginatorProperties,
    )


def unregister():

    del bpy.types.WindowManager.merginator

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)