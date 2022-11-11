import pyglet
from shared.components import Transform


def spawn_label(world, batch, parent):
    entity = world.create_entity()

    transform = Transform.with_local_position(0.0, 32.0)

    transform.position.local_x = 32.0

    world.add_component(entity, Transform(parent=parent))

    world.add_component(
        entity,
        pyglet.text.Label(text, batch=batch)
    )
    return entity