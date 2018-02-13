import bearlibterminal.terminal as blt

from .game_map import GameMap


class GameEngine:
    def __init__(self):
        self.window_width = 80
        self.window_height = 50
        self.map_width = 60
        self.map_height = 50

        self.initialize_blt()
        self.generate_world()

    def initialize_blt(self):
        blt.open()
        blt.set(
            "window: size={}x{}, title='roguelike-bearlib';"
            "".format(
                str(self.window_width),
                str(self.window_height)))
        blt.clear()
        blt.refresh()
        #blt.color_from_name('white')

    def generate_world(self):
        self.game_map = GameMap(width=self.map_width,
                                height=self.map_height,
                                generator='buildings')

    def run(self):
        while blt.read() != blt.TK_CLOSE:
            self.process_one_tick()

        blt.close()

    def process_one_tick(self):
        blt.clear()
        self.render_map()
        blt.refresh()

    def render_map(self):
        for x, column in enumerate(self.game_map):
            for y, tile in enumerate(column):
                blt.print(x, y, '[color={}]{}'.format(tile.color, tile.char))


def main():
    game = GameEngine()
    game.run()


if __name__ == "__main__":
    main()
