import ecs
import pyglet
from pytmx import *
from pytmx.util_pyglet import load_pyglet
from .utils import spawn_block


class TiledRenderer(ecs.System):
    def __init__(self, world):
        super().__init__()
        self.world = world
        self.tm = load_pyglet('simple.tmx')
        self._batches = []
        self._sprites = []
        self.create_sprites()

    def create_sprites(self):
        tw = self.tm.tilewidth
        th = self.tm.tileheight
        mw = self.tm.width
        mh = self.tm.height - 1

        print(self.tm.width * self.tm.tilewidth)
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
                for obj in layer:
                    pass

    def process(self):
        for batch in self._batches:
            batch.draw()
        # self.clock.tick()