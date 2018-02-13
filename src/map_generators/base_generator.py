from abc import ABCMeta, abstractmethod


class Tile:
    def __init__(self, *, color='white', char='#', blocks=True, opaque=None):
        self.color = color
        self.char = char
        self.blocks = blocks
        self.opaque = blocks if opaque is None else opaque

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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
        return [[Tile() for y in range(self.game_map.height)]
                        for x in range(self.game_map.width)]

    def carve(self, x, y):
        self.tiles[x][y].update(blocks=False,
                                opaque=False,
                                color='green',
                                char='.')

    def fill(self, x, y):
        self.tiles[x][y].update(blocks=True,
                                color='white',
                                char='#')

    @abstractmethod
    def generate(self):
        pass
