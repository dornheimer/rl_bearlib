from bearlibterminal import terminal as blt

from src.globals import DIRECTIONS


def get_key(key):
    if key in (blt.TK_KP_8, blt.TK_UP, blt.TK_K):
        return {'move': DIRECTIONS.north}
    elif key in (blt.TK_KP_2, blt.TK_DOWN, blt.TK_J):
        return {'move': DIRECTIONS.south}
    elif key in (blt.TK_KP_4, blt.TK_LEFT, blt.TK_H):
        return {'move': DIRECTIONS.west}
    elif key in (blt.TK_KP_6, blt.TK_RIGHT, blt.TK_L):
        return {'move': DIRECTIONS.east}
    elif key in (blt.TK_KP_1, blt.TK_B):
        return {'move': DIRECTIONS.south_west}
    elif key in (blt.TK_KP_3, blt.TK_N):
        return {'move': DIRECTIONS.south_east}
    elif key in (blt.TK_KP_7, blt.TK_Z):
        return {'move': DIRECTIONS.north_west}
    elif key in (blt.TK_KP_9, blt.TK_U):
        return {'move': DIRECTIONS.north_east}
    elif key in (blt.TK_KP_5, blt.TK_SPACE):
        return {'wait': True}
    else:
        return {}


class Mouse:
    def update_position(self):
        self.x = blt.state(blt.TK_MOUSE_X)
        self.y = blt.state(blt.TK_MOUSE_Y)


class InputHandler:
    def __init__(self):
        self.mouse = Mouse()

    def handle_input(self, key):
        self.mouse.update_position()
        if blt.peek() != key:
            self.action = get_key(key)

    def process(self):
        key = blt.read()
        if key in (blt.TK_CLOSE, blt.TK_ESCAPE):
            return False
        self.handle_input(key)

        return True
