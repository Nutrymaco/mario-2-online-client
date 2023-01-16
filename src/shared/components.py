import pyglet
from pyglet.math import Vec2
from dataclasses import dataclass, astuple, field


def sign(value):
    return -1 if value < 0 else 1


@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0



class Velocity(Vec2):
    pass


@dataclass
class Transform:
    position: Vec2
    scale: Vec2

    def __iter__(self):
        return iter([self.position, self.scale])

@dataclass
class Collision:
    position: Point = field(default_factory=lambda: Point(0.0, 0.0))
    normal: Vec2 = field(default_factory=lambda: Vec2(0.0, 0.0))


class Collider:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def center(self):
        return Vec2(self.x + self.width / 2, self.y + self.height / 2)


    def intersect_aabb(self, collider):
        dx = collider.center.x - self.center.x
        px = self.width / 2 + collider.width / 2 - abs(dx)

        if px < 0:
            return None

        dy = collider.center.y - self.center.y
        py = self.height / 2 + collider.height / 2 - abs(dy)

        if py < 0:
            return None

        if px < py:
            sx = sign(dx)
            return Collision(
                position=Point(self.center.x + self.width / 2 * sx, collider.center.y),
                normal=Vec2(sx, 0)
            )
        else:
            sy = sign(dy)
            return Collision(
                position=Point(collider.center.x, self.center.y + self.height / 2 * sy),
                normal=Vec2(0, sy)
            )


class Label(pyglet.text.Label):
    pass


class Sprite(pyglet.sprite.Sprite):
    pass


    
# class Sprite(pyglet.sprite.Sprite):

#     @property
#     def center(self):
#         return Point(self.x + self.width / 2, self.y + self.height / 2)

#     def is_colliding_with(self, sprite):
#         return self.x < sprite.x + sprite.width and\
#             self.x + self.width > sprite.x and\
#             self.y < sprite.y + sprite.height and\
#             self.y + self.height > sprite.y

#     def intersect_aabb(self, sprite):
#         # 16 - 38 = -22
#         dx = sprite.center.x - self.center.x
#         # 5 + 16 - 22
#         px = self.width / 2 + sprite.width / 2 - abs(dx)

#         print('px', px)

#         if px < 0:
#             return None

#         dy = sprite.center.y - self.center.y
#         py = self.height / 2 + sprite.height / 2 - abs(dy)

#         print('py', py)

#         if py < 0:
#             return None

#         if px < py:
#             sx = sign(dx)
#             return Collision(
#                 position=Point(self.center.x + self.width / 2 * sx, sprite.center.y),
#                 normal=Vec2(x=sx)
#             )
#         else:
#             sy = sign(dy)
#             return Collision(
#                 position=Point(sprite.center.x, self.y + self.height / 2 * sy),
#                 normal=Vec2(y=sy)
#             )

#         # # Из центра надо считать
#         # # 0 - 33
#         # # 16 - 38 = 22
#         # dx = sprite.x - self.x
        
#         # print('player', self.x, self.width)
#         # print(sprite.x, sprite.width)
#         # # 20 / 2 => 10
#         # # 32 / 2 => 16
#         # px = self.width / 2 + sprite.width / 2 - abs(dx)

#         # print('px', px)

#         # if px <= 0:
#         #     return None

#         # # 33 - 33
#         # dy = sprite.y - self.y
#         # py = self.height / 2 + sprite.height / 2 - abs(dy)

#         # if py <= 0:
#         #     return None

#         # if px < py:
#         #     sx = sign(dx)
#         #     print('dx', dx)
#         #     return Collision(
#         #         position=Point(self.x + self.width / 2 * sx, sprite.y),
#         #         normal=Vector(x=sx)
#         #     )
#         #   # sx = sign(dx)
#         #   # collision.normal.x = sx
#         #   # collision.position.x = self.x + self.width / 2 * sx
#         #   # collision.position.y = sprite.y
#         # else:
#         #     sy = sign(dy)
#         #     return Collision(
#         #         position=Point(sprite.x, self.y + self.height / 2 * sy),
#         #         normal=Vector(y=sy)
#         #     )
          
#         #   collision.normal.y = sy
#         #   collision.position.x = sprite.x
#         #   collision.position.y = 
#         # return collision
