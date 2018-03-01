from abc import ABCMeta, abstractmethod

from src.globals import TILES


class Tile:
    def __init__(self, tile_type=None, *, color_lit='t_brown',
                 color_dark='t_black', char='#', blocks=True, opaque=None):
        if tile_type is None:
            self.color_lit = color_lit
            self.color_dark = color_dark
            self.char = char
            self.blocks = blocks
            self.opaque = blocks if opaque is None else opaque
            self.tile_type = 'custom'
        else:
            self.set_type(tile_type)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_type(self, tile_type):
        self.update(**TILES[tile_type])
        self.tile_type = tile_type

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(**{vars(self)})"


class BaseGenerator(metaclass=ABCMeta):
    """Base class for dungeon generation algorithms."""
    def __init__(self, game_map):
        self.game_map = game_map
        self.tiles = self._initialize()

    def _initialize(self, *, tile_type='wall'):
        """Fill game map space with clear tiles."""
        return [[Tile(tile_type)
                for y in range(self.game_map.height)]
                for x in range(self.game_map.width)]

    def carve(self, x, y):
        self.tiles[x][y].set_type('ground')

    def fill(self, x, y):
        self.tiles[x][y].set_type('wall')

    def assign_wall_tiles(self):
        for y in range(self.game_map.height-1):
            for x in range(self.game_map.width-1):
                tile = self.tiles[x][y]
                if not tile.tile_type == 'wall':
                    continue

                wall_tile = self.select_wall_tile(x, y)
                tile.set_type(wall_tile)

    def _check_adjacent_tiles(self, x, y, tile_type='wall', *, door=False):
        north = self.tile_is_type(x, y-1, tile_type, door=door)
        south = self.tile_is_type(x, y+1, tile_type, door=door)
        east = self.tile_is_type(x+1, y, tile_type, door=door)
        west = self.tile_is_type(x-1, y, tile_type, door=door)

        return north, south, east, west

    def select_wall_tile(self, x, y):
        north, south, east, west = self._check_adjacent_tiles(x, y, door=True)
        if all((north, south, east, west)):
            return 'wall'
        elif all((north, east, west)):
            return 'wall_nwe'
        elif all((north, south, east)):
            return 'wall_nse'
        elif all((north, south, west)):
            return 'wall_nsw'
        elif all((south, east, west)):
            return 'wall_swe'
        elif north and south:
            return 'wall_ns'
        elif north and east:
            return 'wall_ne'
        elif north and west:
            return 'wall_nw'
        elif south and east:
            return 'wall_se'
        elif south and west:
            return 'wall_sw'
        elif east and west:
            return 'wall_we'
        elif north:
            return 'wall_n'
        elif south:
            return 'wall_s'
        elif east:
            return 'wall_e'
        elif west:
            return 'wall_w'
        else:
            return 'wall_pillar'

    def tile_is_type(self, x, y, tile_type, *, door=False):
        """Check if tile at location is of a specific type.

        Setting door to True allows treating doors as wall tiles.
        """
        is_type = self.tiles[x][y].tile_type.startswith(tile_type)
        if door:
            return is_type or self.tiles[x][y].tile_type == 'door'
        return is_type

    @abstractmethod
    def generate(self):
        pass
