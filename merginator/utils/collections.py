def get_mesh_objects(collection):
    """Return mesh objects in the collection."""

    return [
        obj
        for obj in collection.objects
        if obj.type == 'MESH'
    ]


def iter_mesh_objects(collection):
    """Yield mesh objects recursively."""

    for obj in collection.objects:
        if obj.type == 'MESH':
            yield obj

    for child in collection.children:
        yield from iter_mesh_objects(child)