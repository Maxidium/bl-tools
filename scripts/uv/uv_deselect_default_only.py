import bpy

# Получаем все выделенные объекты
selected_objects = bpy.context.selected_objects

for obj in selected_objects:
    if obj.type == 'MESH':
        uv_layers = obj.data.uv_layers
        # Проверяем, есть ли UV-слои не 'UVMap'
        has_non_uvmap = any(uv.name != 'UVMap' for uv in uv_layers)
        # Если нет, снимаем выделение
        obj.select_set(has_non_uvmap)