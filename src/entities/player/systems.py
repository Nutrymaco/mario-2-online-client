import ecs
from pyglet.math import Vec3, Mat4
from pyglet.window import key
from shared.components import Transform, Velocity, Collider
from shared.utils import first, Camera2D
from entities.block.components import Block
from .components import Player
from .events import JumpEvent

class PlayerMovement(ecs.System):

    def __init__(self, keyboard):
        super().__init__()
        self.keyboard = keyboard

    def process(self):
        for _, (player, vel) in self.world.get_components(Player, Velocity):
            vel.x = 0

            if self.keyboard.is_pressed(key.LEFT):
                vel.x = -player.movement_speed
            elif self.keyboard.is_pressed(key.RIGHT):
                vel.x = player.movement_speed


class PlayerJumping(ecs.System):
    event_types = [JumpEvent.type]

    def __init__(self, keyboard_input):
        super().__init__()
        
        @keyboard_input.event
        def on_key_press(symbol, modifiers):
            if symbol == key.UP:
                self.events.send(JumpEvent())


    def process(self):
        _, (player, vel) = first(self.world.get_components(Player, Velocity))

        for event in self.events.read():
            if event.type == JumpEvent.type:
                if not (player.jump_count >= 2 and player.is_jumping):
                    player.jump_count += 1
                    player.is_jumping = True
                    vel.y = player.jump_speed


class PlayerPosCalc(ecs.System):

    def process(self):
        for _, (_, transform, vel) in self.world.get_components(Player, Transform, Velocity):
            pos, _ = transform
            pos.x += vel.x
            pos.y += vel.y


class PlayerCollision(ecs.System):

    def process(self):
        _, (p_player, p_collider, p_transform, p_vel) = first(self.world.get_components(Player, Collider, Transform, Velocity))
        b_collider_list = [(b_entity, b_collider) for b_entity, (_, b_collider) in self.world.get_components(Block, Collider)]

        for b_entity, b_collider  in b_collider_list: 
            collision = p_collider.intersect_aabb(b_collider)

            print(collision)
            if collision:
                # [P]->[B]
                if collision.normal.x == 1:
                    p_transform.position.x = b_collider.x - p_collider.width
                # [B]<-[P]
                elif collision.normal.x == -1:
                    p_transform.position.x = b_collider.x + b_collider.width
                # [B]
                #  ↑
                # [P]
                elif collision.normal.y == 1:
                    p_transform.position.y = b_collider.y - p_collider.height
                    p_vel.y = 0
                # [P]
                #  ↓
                # [B]
                elif collision.normal.y == -1:
                    p_player.jump_count = 0
                    p_player.is_jumping = False
                    p_transform.position.y = b_collider.y + b_collider.height
                    p_vel.y = 0


class PlayerCollisionResolution(ecs.System):
    pass

class PlayerCamera(Camera2D, ecs.System):

    def __init__(self, window, map_size):
        super().__init__(window)
        self._map_size = map_size

    def process(self):
        _, (_, transform) = first(self.world.get_components(Player, Transform))
        pos, _ = transform
        map_width, map_height = self._map_size
        x = abs(max(self._window.width - map_width, min(0, self._window.width / 2 - pos.x)))
        y = abs(max(self._window.height - map_height, min(0, self._window.height / 2 - pos.y)))
        self.move_to(x, y)