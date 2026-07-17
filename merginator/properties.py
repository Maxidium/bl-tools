import bpy


class MerginatorProperties(bpy.types.PropertyGroup):

    # ------------------------------------------------------------
    # Join
    # ------------------------------------------------------------

    join_meshes: bpy.props.BoolProperty(
        name="Join Meshes",
        default=True,
    )

    # ------------------------------------------------------------
    # Rename
    # ------------------------------------------------------------

    rename: bpy.props.BoolProperty(
        name="Rename",
        default=True,
    )

    name_mode: bpy.props.EnumProperty(
        name="Naming",
        items=[
            ("AUTO", "Auto Name", "Generate names automatically"),
            ("CUSTOM", "Custom Name", "Use a custom naming pattern"),
        ],
        default="AUTO",
    )

    order_index: bpy.props.EnumProperty(
        name="Order Index",
        items=[
            ("NONE", "Disabled", "Do not add an order index"),
            ("BEFORE_COLLECTION", "Before Collection", "00_body_car_paint"),
            ("BEFORE_GROUP", "Before Group", "body_00_car_paint"),
            ("AFTER_GROUP", "After Group", "body_car_paint_00"),
        ],
        default="NONE",
    )

    custom_name: bpy.props.StringProperty(
        name="Custom Name",
        default="submesh_{i:02d}_LOD_1",
    )

    # ------------------------------------------------------------
    # Misc / Result
    # ------------------------------------------------------------

    move_to_parent: bpy.props.BoolProperty(
        name="Move To Parent",
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