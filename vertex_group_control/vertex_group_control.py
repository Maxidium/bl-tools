bl_info = {
    "name": "Vertex Group Control",
    "author": "Silverhand",
    "version": (1, 3),
    "blender": (3, 0, 0),
    "location": "View3D > N Panel > Tool",
    "category": "Object",
}

import bpy

# ---------------------------------------------------
# Copy All Groups from Active OBJ
# ---------------------------------------------------
class OBJECT_OT_copy_vertex_groups(bpy.types.Operator):
    bl_idname = "object.copy_vertex_groups_from_active"
    bl_label = "Copy All Groups from Active OBJ"
    bl_description = "Copy all vertex groups from active object to selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = context.active_object
        if not active or active.type != 'MESH':
            self.report({'WARNING'}, "Active object must be a mesh")
            return {'CANCELLED'}

        names = [g.name for g in active.vertex_groups]

        for obj in context.selected_objects:
            if obj == active or obj.type != 'MESH':
                continue
            for name in names:
                if name not in obj.vertex_groups:
                    obj.vertex_groups.new(name=name)
        return {'FINISHED'}

# ---------------------------------------------------
# Delete All Groups
# ---------------------------------------------------
class OBJECT_OT_delete_all_vertex_groups(bpy.types.Operator):
    bl_idname = "object.delete_all_vertex_groups"
    bl_label = "Delete All Groups"
    bl_description = "Delete all vertex groups from selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            obj.vertex_groups.clear()
        return {'FINISHED'}

# ---------------------------------------------------
# Assign to Active Group
# ---------------------------------------------------
class OBJECT_OT_assign_all_verts(bpy.types.Operator):
    bl_idname = "object.assign_all_verts_to_active_group"
    bl_label = "Assign to Active Group"
    bl_description = "Assign all vertices of selected meshes to active vertex group"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = context.active_object
        if not active or active.type != 'MESH':
            return {'CANCELLED'}

        group = active.vertex_groups.active
        if not group:
            self.report({'WARNING'}, "No active vertex group selected")
            return {'CANCELLED'}

        name = group.name

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            if name not in obj.vertex_groups:
                vg = obj.vertex_groups.new(name=name)
            else:
                vg = obj.vertex_groups[name]
            verts = [v.index for v in obj.data.vertices]
            vg.add(verts, 1.0, 'REPLACE')
        return {'FINISHED'}

# ---------------------------------------------------
# Remove from Active Group
# ---------------------------------------------------
class OBJECT_OT_remove_all_verts(bpy.types.Operator):
    bl_idname = "object.remove_all_verts_from_active_group"
    bl_label = "Remove from Active Group"
    bl_description = "Remove all vertices of selected meshes from active vertex group"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = context.active_object
        if not active or active.type != 'MESH':
            return {'CANCELLED'}

        group = active.vertex_groups.active
        if not group:
            self.report({'WARNING'}, "No active vertex group selected")
            return {'CANCELLED'}

        name = group.name

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            if name not in obj.vertex_groups:
                continue
            vg = obj.vertex_groups[name]
            verts = [v.index for v in obj.data.vertices]
            vg.remove(verts)
        return {'FINISHED'}

# ---------------------------------------------------
# Select Active Group Vertices
# ---------------------------------------------------
class OBJECT_OT_select_group_verts_safe(bpy.types.Operator):
    bl_idname = "object.select_group_verts_safe"
    bl_label = "Select Active Group Vertices"
    bl_description = "Safely select vertices of the active vertex group in Edit Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Active object must be a mesh")
            return {'CANCELLED'}

        group = obj.vertex_groups.active
        if not group:
            self.report({'WARNING'}, "No active vertex group selected")
            return {'CANCELLED'}

        # Сохраняем текущие выделения
        prev_selection = [o.select_get() for o in context.selected_objects]
        prev_active = context.view_layer.objects.active

        # Деактивируем все объекты кроме активного
        for o in context.selected_objects:
            o.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj

        # Переключаемся в Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Очистка выделения всех вершин
        bpy.ops.mesh.select_all(action='DESELECT')

        # Выбор вершин активной группы
        bpy.ops.object.vertex_group_select()

        # Возврат к предыдущему режиму (опционально)
        # bpy.ops.object.mode_set(mode='OBJECT')

        # Восстанавливаем выделения других объектов
        for o, sel in zip(context.selected_objects, prev_selection):
            o.select_set(sel)
        context.view_layer.objects.active = prev_active

        return {'FINISHED'}

# ---------------------------------------------------
# Assign Active with Cleanup
# ---------------------------------------------------
class OBJECT_OT_move_all_verts_to_active_group(bpy.types.Operator):
    bl_idname = "object.move_all_verts_to_active_group"
    bl_label = "Assign Active with Cleanup"
    bl_description = "Assign all vertices to active vertex group and remove them from all other groups"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = context.active_object
        if not active or active.type != 'MESH':
            return {'CANCELLED'}

        group = active.vertex_groups.active
        if not group:
            self.report({'WARNING'}, "No active vertex group selected")
            return {'CANCELLED'}

        active_name = group.name

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            verts = [v.index for v in obj.data.vertices]

            # Remove vertices from all other groups
            for vg in obj.vertex_groups:
                if vg.name != active_name:
                    vg.remove(verts)

            # Add vertices to active group
            if active_name not in obj.vertex_groups:
                vg = obj.vertex_groups.new(name=active_name)
            else:
                vg = obj.vertex_groups[active_name]
            vg.add(verts, 1.0, 'REPLACE')

        return {'FINISHED'}

# ---------------------------------------------------
# UI Panel
# ---------------------------------------------------
class VIEW3D_PT_vertex_group_control(bpy.types.Panel):
    bl_label = "Vertex Group Control"
    bl_idname = "VIEW3D_PT_vertex_group_control"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout

        # --------------------------
        # Block 1 - Global Actions
        # --------------------------
        layout.label(text="Global Actions:")
        layout.operator("object.copy_vertex_groups_from_active", icon='COPYDOWN')
        layout.operator("object.delete_all_vertex_groups", icon='TRASH')
        layout.separator()

        # --------------------------
        # Block 2 - Active Group Manipulations
        # --------------------------
        layout.label(text="Active Group Manipulations:")
        layout.operator("object.assign_all_verts_to_active_group", icon='VERTEXSEL')
        layout.operator("object.remove_all_verts_from_active_group", icon='X')
        layout.operator("object.select_group_verts", icon='RESTRICT_SELECT_OFF')
        layout.operator("object.move_all_verts_to_active_group", icon='SNAP_VERTEX')
        layout.separator()


# ---------------------------------------------------
# Register
# ---------------------------------------------------
classes = (
    OBJECT_OT_copy_vertex_groups,
    OBJECT_OT_delete_all_vertex_groups,
    OBJECT_OT_assign_all_verts,
    OBJECT_OT_remove_all_verts,
    OBJECT_OT_select_group_verts_safe,
    OBJECT_OT_move_all_verts_to_active_group,
    VIEW3D_PT_vertex_group_control,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()
