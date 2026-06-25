import bpy

# Имя для переименования активной UV карты
new_uv_name = "UVMap"

# Параметр для удаления неактивных UV карт (True/False)
delete_non_active_uvs = True

# Функция для работы с активной UV картой и удалением неактивных UV карт
def rename_active_uv_and_delete_non_active(obj, new_name, delete_non_active):
    # Убедитесь, что объект является мешем и имеет UV карты
    if obj.type == 'MESH' and obj.data.uv_layers:
        active_uv = obj.data.uv_layers.active

        if active_uv:
            # Переименовать активную UV карту
            active_uv.name = new_name
            
            # Удалить неактивные UV карты, если параметр установлен в True
            if delete_non_active:
                non_active_uvs = [uv for uv in obj.data.uv_layers if uv != active_uv]
                for uv in non_active_uvs:
                    obj.data.uv_layers.remove(uv)

# Получить все выделенные объекты
selected_objects = bpy.context.selected_objects

# Обработать каждый выделенный объект
for obj in selected_objects:
    rename_active_uv_and_delete_non_active(obj, new_uv_name, delete_non_active_uvs)
