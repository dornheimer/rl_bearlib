import bearlibterminal.terminal as blt
import logging

from .game_map import GameMap
from .ecs.components import Location, Appearance, Physical, Player, Input
from .ecs.systems import MovementSystem, PlayerSystem
from .ecs.ecs import EntityComponentSystem
from .input import InputHandler


logger = logging.getLogger('roguelike')


class GameEngine:
    def __init__(self):
        self.window_width = 80
        self.window_height = 50
        self.map_width = 60
        self.map_height = 50

        self.initialize_blt()
        self.input_handler = InputHandler()
        self.generate_world()
        self.initialize_ecs()
        self.initialize_entities()

    def initialize_blt(self):
        logger.debug("initializing bearlibterminal")
        blt.open()
        blt.set(
            "window: size={}x{}, title='roguelike-bearlib';"
            "".format(
                str(self.window_width),
                str(self.window_height)))
        blt.clear()
        blt.refresh()
        blt.bkcolor('t_black')

    def initialize_ecs(self):
        logger.debug("initializing entity component system")
        self.ecs = EntityComponentSystem()
        self.ecs.add_system(MovementSystem, game_map=self.game_map)
        self.ecs.add_system(PlayerSystem, input_handler=self.input_handler)

    def initialize_entities(self):
        logger.debug("initializing entities")
        self.player = self.ecs.manager.create_entity()
        self.ecs.manager.compose_entity(
            self.player,
            Player(),
            Physical(blocks=True),
            Appearance(char='@', color='t_magenta'),
            Location(self.map_width/2, self.map_height/2),
            Input(self.input_handler))

    def generate_world(self):
        logger.debug("generating world")
        self.game_map = GameMap(width=self.map_width,
                                height=self.map_height,
                                generator='tunnel')

    def play(self):
        playing = True
        while playing:
            playing = self.input_handler.process()
            self.main_game_loop()

        blt.close()

    def main_game_loop(self):
        blt.clear()
        self.ecs.update()
        self.render_map()
        self.render_entities()
        blt.refresh()

    def render_map(self):
        for x, column in enumerate(self.game_map):
            for y, tile in enumerate(column):
                blt.print(x, y, '[color={}]{}'.format(tile.color, tile.char))

    def render_entities(self):
        entities = self.ecs.manager.entities_with_components('Appearance',
                                                             'Location')
        for e in entities:
            location = self.ecs.manager.entities[e]['Location']
            appearance = self.ecs.manager.entities[e]['Appearance']
            blt.print(location.x, location.y,
                      '[color={}]{}'.format(appearance.color, appearance.char))


def main():
    game = GameEngine()
    game.play()


if __name__ == "__main__":
    main()
