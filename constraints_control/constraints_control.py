bl_info = {
    "name": "Constraints Control Panel",
    "author": "Max",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > N Panel > Tool",
    "description": "Enable/Disable, Apply or Delete Constraints",
    "category": "Object",
}

import bpy


# ---------------- ENABLE / DISABLE ----------------

class OBJECT_OT_toggle_constraints(bpy.types.Operator):
    bl_idname = "object.toggle_constraints"
    bl_label = "Enable / Disable Constraints"
    bl_description = "Toggle Constraints on selected objects"

    def execute(self, context):

        # Определяем текущее состояние (если хотя бы один включён — будем выключать)
        any_enabled = False
        for obj in context.selected_objects:
            for c in obj.constraints:
                if c.enabled:
                    any_enabled = True
                    break

        new_state = not any_enabled

        for obj in context.selected_objects:
            for c in obj.constraints:
                c.enabled = new_state

        return {'FINISHED'}


# ---------------- APPLY ----------------

class OBJECT_OT_apply_constraints(bpy.types.Operator):
    bl_idname = "object.apply_constraints"
    bl_label = "Apply Constraints"
    bl_description = "Apply and remove all Constraints from selected objects"

    def execute(self, context):

        depsgraph = context.evaluated_depsgraph_get()

        for obj in context.selected_objects:

            if obj.constraints:

                # Получаем объект с применёнными constraints
                eval_obj = obj.evaluated_get(depsgraph)

                # Применяем трансформации
                obj.matrix_world = eval_obj.matrix_world

                # Удаляем constraints
                for c in obj.constraints[:]:
                    obj.constraints.remove(c)

        return {'FINISHED'}


# ---------------- DELETE ----------------

class OBJECT_OT_delete_constraints(bpy.types.Operator):
    bl_idname = "object.delete_constraints"
    bl_label = "Delete Constraints"
    bl_description = "Delete all Constraints from selected objects"

    def execute(self, context):
        for obj in context.selected_objects:
            for c in obj.constraints[:]:
                obj.constraints.remove(c)

        return {'FINISHED'}


# ---------------- UI PANEL ----------------

class VIEW3D_PT_constraints_panel(bpy.types.Panel):
    bl_label = "Constraints Control"
    bl_idname = "VIEW3D_PT_constraints_control"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.toggle_constraints", icon='HIDE_OFF')
        layout.operator("object.apply_constraints", icon='CHECKMARK')
        layout.operator("object.delete_constraints", icon='TRASH')


# ---------------- REGISTER ----------------

classes = (
    OBJECT_OT_toggle_constraints,
    OBJECT_OT_apply_constraints,
    OBJECT_OT_delete_constraints,
    VIEW3D_PT_constraints_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()