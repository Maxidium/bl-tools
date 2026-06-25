import bpy

def create_objects_on_all_bones(object_type='CUBE', object_size=(0.2, 0.2, 0.2), use_rotation=True):
    armature = bpy.context.object  # Берём активный объект
    if not armature or armature.type != 'ARMATURE':
        print("Выделите объект-арматуру!")
        return
    
    if bpy.context.object.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')
    
    pose_bones = armature.pose.bones
    if not pose_bones:
        print("Арматура не содержит костей!")
        return

    bpy.ops.object.mode_set(mode='OBJECT')  # Возвращаемся в Object Mode
    
    for bone in pose_bones:
        location = armature.matrix_world @ bone.head  # Получаем мировые координаты основания кости

        if object_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1, location=location)
        elif object_type == 'MONKEY':
            bpy.ops.mesh.primitive_monkey_add(size=1, location=location)
        else:
            print(f"Неизвестный тип объекта: {object_type}")
            continue
        
        obj = bpy.context.object
        obj.scale = (
            object_size[0] / 2 if object_type == 'CUBE' else object_size[0],
            object_size[1] / 2 if object_type == 'CUBE' else object_size[1],
            object_size[2] / 2 if object_type == 'CUBE' else object_size[2]
        )

        obj.name = f"rig_{bone.name}"

        if use_rotation:
            # Применяем поворот кости к объекту
            bone_matrix = armature.matrix_world @ bone.matrix
            obj.rotation_mode = 'QUATERNION'
            obj.rotation_quaternion = bone_matrix.to_quaternion()

# Использование
object_type = 'MONKEY'  # 'CUBE' или 'MONKEY'
object_size = (0.15, 0.15, 0.15)  # Размеры объектов
use_rotation = True  # Учитывать ли поворот костей
create_objects_on_all_bones(object_type, object_size, use_rotation)
