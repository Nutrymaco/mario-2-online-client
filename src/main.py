import ecs
import pyglet
from pyglet.window import key
from shared.systems import Gravity, TransformUpdateSync
from shared.components import Sprite
from shared.constants import FPS, BG_COLOR, SPRITE_SIZE_1x1
from shared.utils import KeyboardInput
from entities.player.utils import spawn_player
from entities.player.systems import (
    PlayerMovement,
    PlayerJumping,
    PlayerPosCalc,
    PlayerCollision,
    PlayerCamera
)
from entities.block.systems import TiledRenderer
from entities.block.utils import spawn_block, generate_blueprint, create_level


def run(args=None):
    window = pyglet.window.Window(width=500, height=500)
    pyglet.gl.glClearColor(*BG_COLOR)
    batch = pyglet.graphics.Batch()
    keyboard = KeyboardInput(window)

    world = ecs.World()

    # create_level(world, batch, generate_blueprint())
    player = spawn_player(world, batch, x=100.0, y=200.0);

    
    # # world.add_system_set(PlayerSystemSet())
    # # tm_renderer = TiledMapRenderer(world)
    tiled_renderer = TiledRenderer(world)
    # # world.add_system(tiled_renderer)
    # # world.add_system(Camera()


    world.add_system(Gravity())
    world.add_system(PlayerCamera(window, (640, 1280)))
    world.add_system(PlayerMovement(keyboard))
    world.add_system(PlayerJumping(keyboard))
    world.add_system(PlayerPosCalc())

    # # Transform
    world.add_system(TransformUpdateSync())
    # # world.add_system(TransformPropagation())
    
    world.add_system(PlayerCollision())


    # world.add_system(ServerSync())
    # <- coin, point, etc ->

    # button_image = pyglet.image.load("start_button.png")
    # button = pyglet.gui.PushButton(0.0, 300.0, button_image, button_image, batch=batch)

    # Restart
    # @keyboard_input.event
    # def on_key_press(symbol, modifiers):
    #     if symbol == key.R:
    #         sprite = world.component_for_entity(player, Sprite)
    #         sprite.x = 200.0
    #         sprite.y = 200.0


    @window.event
    def on_draw():
        window.clear()
        batch.draw()

        # with camera:
        #     batch.draw()
        # tm_renderer.draw()
        tiled_renderer.process()

    def update(dt):
        world.process()
        world.update_events()

    pyglet.clock.schedule_interval(update, 1.0 / FPS)
    pyglet.app.run()



if __name__ == "__main__":
    import sys
    sys.exit(run(sys.argv[1:]) or 0)
