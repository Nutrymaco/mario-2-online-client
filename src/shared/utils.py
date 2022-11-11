from pyglet.math import Vec3, Mat4

def first(coll):
    return next(item for item in coll)


class KeyboardInput:

    def __init__(self, window):
        self._pressed_keys = set()
        self._listeners_on_press = []
        self._listeners_on_release = []

        @window.event
        def on_key_press(symbol, modifiers):
            self._pressed_keys.add(symbol)
            for listener in self._listeners_on_press:
                listener(symbol, modifiers)

        @window.event
        def on_key_release(symbol, modifiers):
            self._pressed_keys.discard(symbol)
            for listener in self._listeners_on_release:
                listener(symbol, modifiers)
    

    def event(self, listener):
        if listener.__name__ == "on_key_press":
            self._listeners_on_press.append(listener)
        elif listener.__name__ == "on_key_release":
            self._listeners_on_release.append(listener)

    def is_pressed(self, key):
        return key in self._pressed_keys


class Camera2D:
    def __init__(self, window, start_pos=None):
        super().__init__()
        if start_pos is None:
            start_pos = (0.0, 0.0)
        self._window = window
        self.move_to(*start_pos)

    def move_to(self, x, y):
        position = Vec3(x, y, 0)
        self._window.view = Mat4.look_at(position, target=position + Vec3(0, 0, -1), up=Vec3(0, 1, 0))
