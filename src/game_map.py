from collections import Sequence

from .map_generators.buildings import Buildings
from .map_generators.tunnel import Tunnel


class GameMap(Sequence):
    generators = {'tunnel':
                  (Tunnel, {'room_min_size': 4, 'room_max_size': 10}),
                  'buildings':
                  (Buildings, {'room_min_size': 4, 'room_max_size': 10})}

    def __init__(self, width, height, generator='tunnel'):
        self.width = width
        self.height = height
        self.generator = self.initialize_generator(generator)
        self.tiles = self.generator.generate()

    def initialize_generator(self, generator):
        generator, params = self.generators[generator]
        return generator(self, **params)

    def __getitem__(self, key):
        return self.tiles[key]

    def __len__(self):
        return self.width * self.height
