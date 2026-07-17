import bpy


class MerginatorProperties(bpy.types.PropertyGroup):

    join_meshes: bpy.props.BoolProperty(
        name="Join Meshes",
        default=True,
    )

    rename: bpy.props.BoolProperty(
        name="Rename",
        default=True,
    )

    custom_name: bpy.props.StringProperty(
        name="Pattern",
        default="submesh_{i:02d}_LOD_1",
    )

    use_auto_name: bpy.props.BoolProperty(
        name="Use Auto Name",
        default=False,
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