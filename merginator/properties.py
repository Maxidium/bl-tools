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

    use_collection_prefix: bpy.props.BoolProperty(
        name="Use Collection Prefix",
        default=False,
    )

    custom_name: bpy.props.StringProperty(
        name="Custom Name",
        default="submesh_{i:02d}_LOD_1",
    )

    triangulate: bpy.props.BoolProperty(
        name="Triangulate",
        default=False,
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