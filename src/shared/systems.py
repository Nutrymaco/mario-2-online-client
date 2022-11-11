import ecs
import pyglet
from pyglet.window import key
from .components import Transform, Velocity, Sprite, Collider
from .constants import GRAVITY, SPRITE_SIZE_1x1


class Gravity(ecs.System):

    def process(self):
        for _, vel in self.world.get_component(Velocity):
            vel.y -= GRAVITY


class TransformPropagation(ecs.System):

    def process(self):
        for entity, transform in self.world.get_component(Transform):
            if tranform.parent:
                pass


class TransformUpdateSync(ecs.System):

    def process(self):
        for entity, transform in self.world.get_component(Transform):
            pos, _ = transform

            # if label := self.world.try_component(entity, Label):
            #   label.x = pos.x
            #   label.y = pos.y

            if sprite := self.world.try_component(entity, Sprite):
                sprite.x = pos.x
                sprite.y = pos.y
                
            if collider := self.world.try_component(entity, Collider):
                collider.x = pos.x
                collider.y = pos.y
