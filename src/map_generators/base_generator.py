from abc import ABCMeta, abstractmethod

from src.globals import TILES


class Tile:
    tile_types = TILES

    def __init__(self, tile_type=None, *, color='t_brown', char='#',
                 blocks=True, opaque=None):
        if tile_type is None:
            self.color = color
            self.char = char
            self.blocks = blocks
            self.opaque = blocks if opaque is None else opaque
        else:
            self.set_type(tile_type)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_type(self, tile_type):
        self.update(**Tile.tile_types[tile_type])

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(**{vars(self)})"


class BaseGenerator(metaclass=ABCMeta):
    """Base class for dungeon generation algorithms."""
    def __init__(self, game_map):
        self.game_map = game_map
        self.tiles = self._initialize()

    def _initialize(self):
        """Fill map space with blocked tiles."""
        return [[Tile('wall') for y in range(self.game_map.height)]
                              for x in range(self.game_map.width)]

    def carve(self, x, y):
        self.tiles[x][y].set_type('ground')

    def fill(self, x, y):
        self.tiles[x][y].set_type('wall')

    @abstractmethod
    def generate(self):
        pass
