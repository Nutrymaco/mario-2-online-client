import pyglet
from pyglet.math import Vec2
from shared.components import Transform, Velocity, Sprite, Collider
# from entities.label.utils import spawn_label
from .components import Player


def spawn_player(world, batch, x=0.0, y=0.0):
    player = world.create_entity()

    world.add_component(player, Player())
    world.add_component(player, Transform(position=Vec2(x, y), scale=Vec2(1.0, 1.0)))
    world.add_component(player, Velocity())

    sprite = Sprite(
        pyglet.resource.image("assets/mario/0.png"),
        batch=batch,
        x=x,
        y=y
    )

    world.add_component(player, sprite)
    world.add_component(player, Collider(x, y, sprite.width, sprite.height))

    # spawn_label(world, batch, )

    return player
