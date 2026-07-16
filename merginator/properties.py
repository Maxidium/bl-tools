import bpy


class MerginatorProperties(bpy.types.PropertyGroup):

    triangulate: bpy.props.BoolProperty(
        name="Triangulate",
        default=True,
    )

    quad_method: bpy.props.EnumProperty(
        name="Quad Method",
        items=[
            ('FIXED', "Fixed", ""),
            ('FIXED_ALTERNATE', "Fixed Alternate", ""),
            ('BEAUTY', "Beauty", ""),
            ('SHORTEST_DIAGONAL', "Shortest Diagonal", ""),
            ('LONGEST_DIAGONAL', "Longest Diagonal", ""),
        ],
        default='BEAUTY',
    )

    ngon_method: bpy.props.EnumProperty(
        name="N-gon Method",
        items=[
            ('CLIP', "Clip", ""),
            ('BEAUTY', "Beauty", ""),
        ],
        default='BEAUTY',
    )

    keep_normals: bpy.props.BoolProperty(
        name="Keep Normals",
        default=True,
    )

    use_custom_naming: bpy.props.BoolProperty(
        name="Custom Naming",
        default=False,
    )

    use_collection_prefix: bpy.props.BoolProperty(
        name="Use Collection Name as Prefix",
        default=False,
    )

    custom_name: bpy.props.StringProperty(
        name="Custom Name",
        default="submesh_{i:02d}_LOD_1",
    )

    select_all: bpy.props.BoolProperty(
        name="Select All",
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