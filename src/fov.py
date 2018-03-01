from bresenham import bresenham

from .elements import Rect, Vector


class FieldOfView:
    def __init__(self, game_map, viewing_distance=3):
        self.game_map = game_map
        self.viewing_distance = viewing_distance
        self.fov_map = self.initialize()
        self.last_area = None
        self.last_origin = None

    def initialize(self):
        return [[False for y in range(self.game_map.height)]
                for x in range(self.game_map.width)]

    def cast_rays(self, origin_x, origin_y):
        #distance = Vector ??
        visible_area = Rect.from_center(origin_x,
                                        origin_y,
                                        self.viewing_distance,
                                        self.viewing_distance)
        self.last_area = visible_area
        for dest_x, dest_y in visible_area.border:
            yield bresenham(origin_x, origin_y, dest_x, dest_y)

    def reset(self):
        if self.last_area is None:
            return
        for x in range(self.last_area.x1, self.last_area.x2+1):
            for y in range(self.last_area.y1, self.last_area.y2+1):
                self.fov_map[x][y] = False

    def compute(self, origin_x, origin_y, light_walls=False):
        if (origin_x, origin_y) == self.last_origin:
            return
        self.reset()
        for ray in self.cast_rays(origin_x, origin_y):
            for x, y in ray:
                if self.game_map[x][y].is_type('wall', door=True):
                    if light_walls:
                        self.fov_map[x][y] = True
                    break
                self.fov_map[x][y] = True
        self.last_origin = origin_x, origin_y

    def is_visible(self, x, y):
        return self.fov_map[x][y]
