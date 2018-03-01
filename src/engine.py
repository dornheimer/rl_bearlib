import bearlibterminal.terminal as blt
import logging

from .fov import FieldOfView
from .game_map import GameMap
from .ecs.components import (Location, Appearance, Physical, Player, Input,
                             Velocity)
from .ecs.systems import MovementSystem, PlayerSystem
from .ecs.ecs import EntityComponentSystem
from .input import InputHandler
from .message_log import MessageLog


logger = logging.getLogger('roguelike')


class GameEngine:
    def __init__(self):
        self.window_width = 80
        self.window_height = 50
        self.map_width = 60
        self.map_height = self.window_height
        self.panel_width = self.window_width - self.map_width
        self.panel_height = self.window_height

        self.input_handler = InputHandler()
        self.message_log = MessageLog(x=self.map_width+1,
                                      y=self.panel_height-20,
                                      width=self.panel_width-1,
                                      height=20)

        self.initialize_blt()
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
        self.ecs = EntityComponentSystem(message_log=self.message_log)
        self.ecs.add_system(MovementSystem, game_map=self.game_map)
        self.ecs.add_system(PlayerSystem)

    def initialize_entities(self):
        logger.debug("initializing entities")
        self.player = self.ecs.manager.create_entity()
        self.ecs.manager.compose_entity(
            self.player,
            Player(),
            Physical(blocks=True),
            Appearance(char='@', color='t_magenta'),
            Location(self.map_width/2, self.map_height/2),
            Velocity(0, 0),
            Input(self.input_handler))

    def generate_world(self):
        logger.debug("generating world")
        self.game_map = GameMap(width=self.map_width,
                                height=self.map_height,
                                generator='tunnel')
        self.fov = FieldOfView(self.game_map)

    def play(self):
        playing = True
        while playing:
            if blt.has_input():
                playing = self.input_handler.process()
                self.main_game_loop()

        blt.close()

    def main_game_loop(self):
        blt.clear()
        self.render_map()
        self.render_entities()
        self.ecs.update()
        self.render_panel()
        blt.refresh()

    def render_map(self):
        player_loc = self.ecs.manager.entities[self.player]['Location']
        self.fov.compute(player_loc.x, player_loc.y, light_walls=True)
        for x, column in enumerate(self.game_map):
            for y, tile in enumerate(column):
                if self.fov.is_visible(x, y):
                    blt.print(x, y, '[color={}]{}'.format(
                        tile.color_lit, tile.char))
                    self.game_map[x][y].explored = True
                elif self.game_map[x][y].explored:
                    blt.print(x, y, '[color={}]{}'.format(
                        tile.color_dark, tile.char))

    def render_entities(self):
        renderables = self.ecs.manager.entities_with_components('Location',
                                                                'Appearance')

        for r in renderables:
            location = self.ecs.manager.entities[r]['Location']
            appearance = self.ecs.manager.entities[r]['Appearance']
            blt.print(location.x, location.y,
                      '[color={}]{}'.format(appearance.color, appearance.char))

    def render_panel(self):
        self.display_message_log()

    def display_message_log(self):
        lines = 0
        for message in self.message_log:
            current_line = self.message_log.y + lines
            blt.puts(x=self.message_log.x,
                     y=current_line,
                     s=f"[color={message.color}]{message.text}",
                     width=self.message_log.width,
                     height=self.message_log.height,
                     align=blt.TK_ALIGN_LEFT)
            lines += message.lines


def main():
    game = GameEngine()
    game.play()


if __name__ == "__main__":
    main()
