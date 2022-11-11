import pyglet
from pyglet.math import Vec2
from pytmx import *
from pytmx.util_pyglet import load_pyglet
from shared.components import Transform, Sprite, Collider
from shared.constants import SPRITE_SIZE_1x1
from .components import Block


def spawn_block(world, image, batch, x=0.0, y=0.0):
    block = world.create_entity()

    world.add_component(block, Block())
    world.add_component(block, Transform(position=Vec2(x, y), scale=Vec2(1.0, 1.0)))
    
    sprite = Sprite(image, x=x, y=y, batch=batch)

    world.add_component(block, sprite)
    world.add_component(block, Collider(x, y, sprite.width, sprite.height))

    return block


def generate_blueprint(width=64, height=64):
    return [
        "                       ",
        "    1     *            ",
        "         111           ",
        " 11     11111       *11",
        "111111 11111111  111111"
    ]


def create_level(world, batch, blueprint):
    row_count = len(blueprint)
    for row_index, _ in enumerate(blueprint):
        for col_index, cell in enumerate(blueprint[row_count - (row_index + 1)]):
            width, height = SPRITE_SIZE_1x1         
            offset_x = offset_y = 0

            if (col_index > 0):
                offset_x = 1

            if (row_index > 0):
                offset_y = 1

            pos_x = col_index * width + offset_x
            pos_y = row_index * height + offset_y

            if cell == "1":
                spawn_block(world, batch, (pos_x, pos_y))



class TiledMapRenderer():
    def __init__(self, world):
        self.world = world
        self.tm = load_pyglet('simple.tmx')
        self._batches = []
        self.create_sprites()

    def create_sprites(self):
        tw = self.tm.tilewidth
        th = self.tm.tileheight
        mw = self.tm.width
        mh = self.tm.height - 1

        for layer in self.tm.visible_layers:
            if isinstance(layer, TiledTileLayer):
                batch = pyglet.graphics.Batch()
                self._batches.append(batch)
                for x, y, image in layer.tiles():
                    y = mh - y
                    x = x * tw
                    y = y * th
                    spawn_block(self.world, image, batch, x, y) 
            elif isinstance(layer, TiledObjectGroup):
                pass

    def draw(self):
        for batch in self._batches:
            batch.draw()