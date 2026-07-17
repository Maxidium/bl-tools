import bpy

from ..utils.collections import iter_mesh_objects


def collect_groups(collection):
    """
    Collect mesh objects grouped by material.

    Returns:
        {
            material: [objects],
            None: [objects without material]
        }
    """

    groups = {}

    for obj in iter_mesh_objects(collection):

        material = None

        if len(obj.material_slots) == 1:
            material = obj.material_slots[0].material

        groups.setdefault(material, []).append(obj)

    return groups


def get_target_collection(parent_collection, material):
    """
    Get or create collection for material group.
    """

    if material:
        name = f"{material.name} - {parent_collection.name}"
    else:
        name = "_NonSorted"


    for child in parent_collection.children:
        if child.name == name:
            return child


    new_collection = bpy.data.collections.new(name)

    parent_collection.children.link(new_collection)


    if material is None:
        new_collection.color_tag = 'COLOR_01'


    return new_collection


def move_to_collection(obj, target_collection):
    """
    Move object into target collection.
    """

    for collection in list(obj.users_collection):
        collection.objects.unlink(obj)


    target_collection.objects.link(obj)


def group_by_material(collection):
    """
    Group mesh objects by their material.
    """

    groups = collect_groups(collection)


    for material, objects in groups.items():

        target_collection = get_target_collection(collection,material,)


        for obj in objects:
            move_to_collection(obj,target_collection,)


class MERGINATOR_OT_GroupByMaterials(bpy.types.Operator):

    bl_idname = "merginator.group_by_materials"
    bl_label = "Group by Material"
    bl_description = "Create subcollections based on object materials"

    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        collection = (
            context
            .view_layer
            .active_layer_collection
            .collection
        )


        group_by_material(collection)


        self.report(
            {'INFO'},
            "Objects grouped by material"
        )


        return {'FINISHED'}