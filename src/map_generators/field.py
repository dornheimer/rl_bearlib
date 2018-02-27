from .base_generator import BaseGenerator


class Field(BaseGenerator):
    def __init__(self, game_map):
        super().__init__(game_map)
        self.tiles = self._initialize(tile_type='ground')

    def generate(self):
        for x in (0, self.game_map.width-1):
            for y in range(self.game_map.height):
                self.fill(x, y)

        for y in (0, self.game_map.height-1):
            for x in range(self.game_map.width):
                self.fill(x, y)

        self.assign_wall_tiles()
        return self.tiles
