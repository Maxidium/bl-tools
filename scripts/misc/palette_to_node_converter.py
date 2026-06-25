import bpy

NODEGROUP_PREFIX = "pal_"  # Префикс для Node Group

GRID_LAYOUT = True           # True = сетка, False = вертикально
NODES_PER_ROW = 10           # Кол-во нодов на одной линии
X_SPACING = 200              # Расстояние между нодами по X
Y_SPACING = 250              # Расстояние между нодами по Y

# Смещение от Group Output (все ноды слева)
X_OFFSET = -200               # смещение по X от Output влево
Y_OFFSET = 0                  # смещение по Y от Output (начало сверху)

# =========================
# Создание Node Group
# =========================

def palette_to_nodegroup(palette):
    """Создаёт Node Group из палитры с нодами слева от Output.
       Group Input над Group Output. Если группа уже есть — перезаписывает."""
    group_name = f"{NODEGROUP_PREFIX}{palette.name}"

    # Удаляем существующую группу, если есть
    if group_name in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[group_name])
        print(f"Removed existing Node Group: {group_name}")

    # Создаём новую группу
    node_group = bpy.data.node_groups.new(group_name, 'ShaderNodeTree')

    # Group Input и Output
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")
    input_node.location = (0, 200)    # над Output
    output_node.location = (0, 0)     # всегда в центре

    # Расчёт позиции RGB-нодов
    for i, col in enumerate(palette.colors):
        rgb_node = node_group.nodes.new("ShaderNodeRGB")
        rgb_node.outputs[0].default_value = (*col.color[:3], 1.0)

        if GRID_LAYOUT:
            row = i // NODES_PER_ROW
            col_idx = i % NODES_PER_ROW
            rgb_node.location = (X_OFFSET - col_idx * X_SPACING, Y_OFFSET - row * Y_SPACING)
        else:
            rgb_node.location = (X_OFFSET, Y_OFFSET - i * Y_SPACING)

        # Создаём выход
        socket_name = f"color_{i+1:02d}"
        node_group.interface.new_socket(
            name=socket_name,
            in_out='OUTPUT',
            socket_type='NodeSocketColor'
        )

        # Линк RGB → Output
        node_group.links.new(rgb_node.outputs[0], output_node.inputs[socket_name])

    print(f"Created Node Group: {group_name}")
    return node_group

# =========================
# Активная палитра
# =========================

active_palette = bpy.context.tool_settings.image_paint.palette

if active_palette:
    palette_to_nodegroup(active_palette)
else:
    print("No active palette found! Make sure a palette is active in the Palette editor.")