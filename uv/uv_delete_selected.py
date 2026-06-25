import bpy

# Get selected objects
selected_objects = bpy.context.selected_objects

# Loop through selected objects
for obj in selected_objects:
    # Check if object has UV maps
    if obj.data.uv_layers:
        # Remove all UV maps
        while obj.data.uv_layers:
            obj.data.uv_layers.remove(obj.data.uv_layers[0])
