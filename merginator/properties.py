import bpy


class MerginatorProperties(bpy.types.PropertyGroup):

    triangulate: bpy.props.BoolProperty(
        name="Triangulate",
        default=True,
    )

    join_meshes: bpy.props.BoolProperty(
        name="Join Meshes",
        default=True,
    )

    rename_objects: bpy.props.BoolProperty(
        name="Rename Objects",
        default=True,
    )

    select_result: bpy.props.BoolProperty(
        name="Select Result",
        default=True,
    )


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