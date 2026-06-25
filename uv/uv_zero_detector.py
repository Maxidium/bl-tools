import bpy

# Настройки
use_preselection = True  
# True - найти на основе выбранных
# False - найти во всей сцене

def select_meshes_without_uv(use_preselection=False):
    if not use_preselection:
        # Снимаем выделение со всех объектов
        bpy.ops.object.select_all(action='DESELECT')

    # Список объектов, которые нужно оставить выделенными
    objects_to_keep = []

    # Проходим по всем объектам в сцене
    for obj in bpy.data.objects:
        # Проверяем, является ли объект мешем
        if obj.type == 'MESH':
            # Проверяем, есть ли у меша UV-слои
            if not obj.data.uv_layers:
                if use_preselection:
                    # Если объект уже выделен, добавляем его в список для выделения
                    if obj.select_get():
                        objects_to_keep.append(obj)
                else:
                    # Добавляем в список для выделения
                    objects_to_keep.append(obj)

    # Снимаем выделение со всех объектов
    bpy.ops.object.select_all(action='DESELECT')

    # Выделяем только объекты без UV из списка
    for obj in objects_to_keep:
        obj.select_set(True)

    # Убедимся, что в режиме объекта
    bpy.context.view_layer.objects.active = None

# Запуск функции
select_meshes_without_uv(use_preselection)