import json
from collections import namedtuple


Directions = namedtuple('Directions',
                        ['north', 'south', 'east', 'west', 'north_east',
                         'north_west', 'south_east', 'south_west'])


DIRECTIONS = Directions((0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (-1, -1),
                        (1, 1), (-1, 1))


with open('config/tiles.json') as tile_data:
    TILES = json.load(tile_data)
