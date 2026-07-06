bl_info = {
    "name": "Node Coord Info",
    "author": "Dev",
    "version": (1, 0, 8),
    "blender": (3, 0, 0),
    "location": "Shader Editor > Sidebar > Node Info",
    "description": "Previewing and Editing coordinates of Active Node and Selected Nodes",
    "warning": "",
    "wiki_url": "",
    "category": "Node Editor",
}

import bpy
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty

def get_active_node():
    space = bpy.context.space_data
    if space and space.type == 'NODE_EDITOR':
        tree = space.edit_tree
        if tree:
            return tree.nodes.active
    return None

def update_selected_nodes(context):
    wm = context.window_manager
    wm.selected_nodes.clear()
    space = context.space_data
    if space and space.type == 'NODE_EDITOR' and space.tree_type == 'ShaderNodeTree':
        tree = space.edit_tree
        if tree:
            for node in tree.nodes:
                if node.select:
                    item = wm.selected_nodes.add()
                    item.name = node.name


class NodeCoordInfoPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    show_selected_nodes_info: BoolProperty(
        name="Show Selected Nodes Info",
        default=True,
        description="Enable to show panel with info about selected nodes"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "show_selected_nodes_info")

class SelectedNodeItem(bpy.types.PropertyGroup):
    name: StringProperty()

class NODE_UL_selected_nodes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        node_name = item.name
        node = context.space_data.edit_tree.nodes.get(node_name) if context.space_data and context.space_data.edit_tree else None
        active_node = context.space_data.edit_tree.nodes.active if context.space_data and context.space_data.edit_tree else None

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            if active_node and node_name == active_node.name:
                row.alert = True
                row.label(text=node_name, icon='RADIOBUT_ON')
            else:
                row.label(text=node_name)
            if node:
                row.label(text=f"X: {node.location.x:.2f} Y: {node.location.y:.2f}")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='NODE')

class NODE_PT_active_node_info(bpy.types.Panel):
    bl_label = "Active Node Info"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Node Info'

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR' and space.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout
        node = get_active_node()

        if not node:
            layout.label(text="No active node", icon='ERROR')
            return

        layout.label(text=f"Name: {node.name}")
        layout.label(text=f"Type: {node.bl_idname}")
        layout.separator()
        layout.label(text=f"X: {node.location.x:.2f}")
        layout.label(text=f"Y: {node.location.y:.2f}")

class NODE_PT_selected_nodes_info(bpy.types.Panel):
    bl_label = "Selected Nodes Info"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Node Info'

    @classmethod
    def poll(cls, context):
        prefs_addon = bpy.context.preferences.addons.get(__name__)
        if not prefs_addon:
            return False
        prefs = prefs_addon.preferences

        space = context.space_data
        return prefs.show_selected_nodes_info and space and space.type == 'NODE_EDITOR' and space.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        update_selected_nodes(context)

        if not wm.selected_nodes:
            layout.label(text="No nodes selected", icon='INFO')
            return

        layout.label(text=f"Selected Nodes: {len(wm.selected_nodes)}")

        row = layout.row()
        row.template_list("NODE_UL_selected_nodes", "", wm, "selected_nodes", wm, "selected_nodes_index", rows=6)

class NODE_PT_active_node_edit(bpy.types.Panel):
    bl_label = "Edit Node Location"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Node Info'

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR' and space.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout
        node = get_active_node()

        if not node:
            layout.label(text="No active node", icon='ERROR')
            return

        layout.operator("node.move_nodes_to_center_from_active", text="Center All From Active", icon='GRID')
        layout.operator("node.move_selected_nodes_to_center_from_active", text="Center Selected From Active", icon='RESTRICT_SELECT_OFF')
        layout.separator()

        layout.label(text="Edit Location:")
        layout.prop(node, "location", index=0, text="X")
        layout.prop(node, "location", index=1, text="Y")

        layout.separator()
        row = layout.row(align=True)
        row.operator("node.copy_node_location", text="Copy", icon='COPYDOWN')
        row.operator("node.paste_node_location", text="Paste", icon='PASTEDOWN')
        row.separator()
        row.operator("node.reset_node_locations", text="Reset", icon='FILE_REFRESH')

class NODE_OT_move_selected_nodes_to_coords(bpy.types.Operator):
    bl_idname = "node.move_selected_nodes_to_coords"
    bl_label = "Move Selected Nodes to Coordinates"

    def execute(self, context):
        scene = context.scene
        props = scene.node_move_coords

        space = context.space_data
        if not (space and space.type == 'NODE_EDITOR'):
            self.report({'WARNING'}, "Not in node editor")
            return {'CANCELLED'}

        tree = space.edit_tree
        if not tree:
            self.report({'WARNING'}, "No node tree found")
            return {'CANCELLED'}

        selected_nodes = [node for node in tree.nodes if node.select]
        if not selected_nodes:
            self.report({'WARNING'}, "No nodes selected")
            return {'CANCELLED'}

        active = tree.nodes.active

        if active:
            # Рассчёт сдвига
            dx = props.x - active.location.x
            dy = props.y - active.location.y

            # Получаем все ноды, которые нужно сдвинуть:
            # Включаем активный + выделенные (чтобы не потерять)
            nodes_to_move = set(selected_nodes)
            nodes_to_move.add(active)

            # Дополнительно можно добавить ноды, связанные с активным через хвостики,
            # если надо, но в твоём случае, наверное, уже выделены.

            for node in nodes_to_move:
                node.location.x += dx
                node.location.y += dy

            self.report({'INFO'}, f"Moved {len(nodes_to_move)} nodes by delta ({dx:.2f}, {dy:.2f})")
            return {'FINISHED'}

        # Если нет активного, просто сдвигаем выделенные в указанную точку
        for node in selected_nodes:
            node.location.x = props.x
            node.location.y = props.y

        self.report({'INFO'}, f"Moved {len(selected_nodes)} selected nodes to ({props.x:.2f}, {props.y:.2f})")
        return {'FINISHED'}

class NodeMoveCoordsProperties(bpy.types.PropertyGroup):
    x: bpy.props.FloatProperty(name="X", default=0.0)
    y: bpy.props.FloatProperty(name="Y", default=0.0)


# --- Operators ---

class NODE_OT_move_nodes_to_center_from_active(bpy.types.Operator):
    bl_idname = "node.move_nodes_to_center_from_active"
    bl_label = "Move Nodes to Center From Active"

    def execute(self, context):
        space = context.space_data
        if space and space.type == 'NODE_EDITOR':
            tree = space.edit_tree
            active = tree.nodes.active
            if not active:
                self.report({'WARNING'}, "No active node")
                return {'CANCELLED'}

            center_x = active.location.x
            center_y = active.location.y

            for node in tree.nodes:
                if node != active:
                    node.location.x -= center_x
                    node.location.y -= center_y

            active.location.x = 0
            active.location.y = 0

            self.report({'INFO'}, "Nodes moved relative to active node")
            return {'FINISHED'}

        self.report({'WARNING'}, "Not in node editor")
        return {'CANCELLED'}

class NODE_OT_move_selected_nodes_to_center_from_active(bpy.types.Operator):
    bl_idname = "node.move_selected_nodes_to_center_from_active"
    bl_label = "Move Selected Nodes to Center From Active"

    def execute(self, context):
        space = context.space_data
        if space and space.type == 'NODE_EDITOR':
            tree = space.edit_tree
            active = tree.nodes.active
            if not active:
                self.report({'WARNING'}, "No active node")
                return {'CANCELLED'}

            selected_nodes = [node for node in tree.nodes if node.select]
            if not selected_nodes:
                self.report({'WARNING'}, "No nodes selected")
                return {'CANCELLED'}

            center_x = active.location.x
            center_y = active.location.y

            for node in selected_nodes:
                if node != active:
                    node.location.x -= center_x
                    node.location.y -= center_y

            # Поміщаємо активний у центр (0,0)
            active.location.x = 0
            active.location.y = 0

            self.report({'INFO'}, "Selected nodes moved relative to active node")
            return {'FINISHED'}

        self.report({'WARNING'}, "Not in node editor")
        return {'CANCELLED'}

class NODE_OT_copy_node_location(bpy.types.Operator):
    bl_idname = "node.copy_node_location"
    bl_label = "Copy Node Location"

    def execute(self, context):
        node = get_active_node()
        if not node:
            self.report({'WARNING'}, "No active node")
            return {'CANCELLED'}

        x, y = node.location.x, node.location.y
        bpy.context.window_manager.clipboard = f"{x};{y}"
        self.report({'INFO'}, f"Copied location: {x:.2f};{y:.2f}")
        return {'FINISHED'}

class NODE_OT_paste_node_location(bpy.types.Operator):
    bl_idname = "node.paste_node_location"
    bl_label = "Paste Node Location"

    def execute(self, context):
        node = get_active_node()
        if not node:
            self.report({'WARNING'}, "No active node")
            return {'CANCELLED'}

        clipboard = bpy.context.window_manager.clipboard.strip()
        if not clipboard:
            self.report({'ERROR'}, "Clipboard is empty")
            return {'CANCELLED'}

        try:
            x_str, y_str = clipboard.split(';')
            node.location.x = float(x_str)
            node.location.y = float(y_str)
            self.report({'INFO'}, f"Pasted location: {x_str};{y_str}")
            return {'FINISHED'}
        except Exception:
            self.report({'ERROR'}, f"Invalid clipboard data: {clipboard}")
            return {'CANCELLED'}

class NODE_OT_reset_node_locations(bpy.types.Operator):
    bl_idname = "node.reset_node_locations"
    bl_label = "Reset Node Location(s)"

    def execute(self, context):
        space = context.space_data
        if space and space.type == 'NODE_EDITOR':
            tree = space.edit_tree
            if not tree:
                self.report({'WARNING'}, "No node tree found")
                return {'CANCELLED'}

            selected_nodes = [node for node in tree.nodes if node.select]
            active = tree.nodes.active

            if selected_nodes:
                for node in selected_nodes:
                    node.location.x = 0
                    node.location.y = 0
                self.report({'INFO'}, f"Reset location for {len(selected_nodes)} selected node(s)")
                return {'FINISHED'}

            elif active:
                active.location.x = 0
                active.location.y = 0
                self.report({'INFO'}, "Reset location for active node")
                return {'FINISHED'}

            self.report({'WARNING'}, "No active or selected nodes found")
            return {'CANCELLED'}

        self.report({'WARNING'}, "Not in node editor")
        return {'CANCELLED'}

class NODE_PT_move_nodes_to_coords(bpy.types.Panel):
    bl_label = "Move Nodes to Coordinates"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Node Info'

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space and space.type == 'NODE_EDITOR' and space.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.node_move_coords

        layout.prop(props, "x")
        layout.prop(props, "y")
        layout.operator("node.move_selected_nodes_to_coords", icon='EMPTY_ARROWS')


classes = (
    NodeCoordInfoPreferences,
    SelectedNodeItem,
    NODE_UL_selected_nodes,
    NODE_PT_active_node_info,
    NODE_PT_selected_nodes_info,
    NODE_PT_active_node_edit,
    NODE_PT_move_nodes_to_coords,
    NODE_OT_move_nodes_to_center_from_active,
    NODE_OT_move_selected_nodes_to_center_from_active,
    NODE_OT_copy_node_location,
    NODE_OT_paste_node_location,
    NODE_OT_reset_node_locations,
    NODE_OT_move_selected_nodes_to_coords,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.selected_nodes = CollectionProperty(type=SelectedNodeItem)
    bpy.types.WindowManager.selected_nodes_index = IntProperty()

    bpy.utils.register_class(NodeMoveCoordsProperties)
    bpy.types.Scene.node_move_coords = bpy.props.PointerProperty(type=NodeMoveCoordsProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.selected_nodes
    del bpy.types.WindowManager.selected_nodes_index

    del bpy.types.Scene.node_move_coords
    bpy.utils.unregister_class(NodeMoveCoordsProperties)

if __name__ == "__main__":
    register()
