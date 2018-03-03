from collections import Sequence
import logging

from .map_generators.buildings import Buildings
from .map_generators.tunnel import Tunnel
from .map_generators.field import Field


logger = logging.getLogger('roguelike')


class GameMap(Sequence):
    """Generate the game map using one of the available generators."""

    generators = {'tunnel':
                  (Tunnel, {'room_min_size': 4, 'room_max_size': 10}),
                  'buildings':
                  (Buildings, {'room_min_size': 4, 'room_max_size': 10}),
                  'field':
                  (Field, {})}

    def __init__(self, width, height, generator='tunnel'):
        self.width = width
        self.height = height
        self.generator = self.initialize_generator(generator)
        self.tiles = self.generator.generate()

        logger.debug(f"sucessfully built map (generator: {generator})")

    def initialize_generator(self, generator):
        """Use generator to initialize tiles."""
        generator, params = self.generators[generator]
        return generator(self, **params)

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocks

    def __getitem__(self, key):
        return self.tiles[key]

    def __len__(self):
        return self.width * self.height
