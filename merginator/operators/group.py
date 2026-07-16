import bpy


def collect_groups(collection):
    """
    Collect mesh objects grouped by material.
    
    Returns:
        dict:
            {
                material: [objects],
                None: [objects without material]
            }
    """

    groups = {}

    for obj in collection.objects:

        if obj.type != 'MESH':
            continue

        material = None

        if len(obj.material_slots) == 1:
            material = obj.material_slots[0].material

        groups.setdefault(material, []).append(obj)

    return groups


def get_target_collection(parent_collection, material):
    """
    Get or create subcollection for material group.
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
        new_collection.color_tag = 'COLOR_01' # Red


    return new_collection


def move_to_collection(obj, target_collection):
    """
    Move object to target collection.
    """

    current_collections = list(obj.users_collection)

    for collection in current_collections:
        collection.objects.unlink(obj)


    if obj.name not in target_collection.objects:
        target_collection.objects.link(obj)



def group_by_material(collection):
    """
    Group mesh objects into collections by material.
    """

    groups = collect_groups(collection)


    for material, objects in groups.items():

        target_collection = get_target_collection(collection,material,)


        for obj in objects:

            move_to_collection(obj,target_collection,)


class MERGINATOR_OT_GroupMaterials(bpy.types.Operator):

    bl_idname = "merginator.group_materials"
    bl_label = "Group by Material"
    bl_description = "Group mesh objects into collections by material"

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