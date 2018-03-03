from bresenham import bresenham

from .elements import Circle


class FieldOfView:
    """Light up circular area around the origin.

    Uses simple ray casting algorithim. Artifacts increase with radius, but
    are hardly noticable if radius <= 4."""

    def __init__(self, game_map, radius=3):
        self.game_map = game_map
        self.radius = radius
        self.fov_map = self.initialize()
        self.last_area = set()
        self.last_origin = None

    def initialize(self):
        """Initialize completely dark FOV map."""
        return [[False for y in range(self.game_map.height)]
                for x in range(self.game_map.width)]

    def cast_rays(self, origin_x, origin_y):
        """Cast rays from the origin to each point on the border of the
        visible area (a circle).

        Rays are approximated with Bresenham.
        """
        visible_area = Circle(origin_x, origin_y, radius=self.radius)
        for dest_x, dest_y in visible_area.border:
                yield bresenham(origin_x, origin_y, dest_x, dest_y)

    def reset(self):
        for x, y in self.last_area:
            self.fov_map[x][y] = False

    def compute(self, origin_x, origin_y, light_walls=False):
        """Compute the FOV.

        Trace rays from the origin, light up visited tiles and stop at walls.
        Enabling light_walls includes walls in lit area.
        """
        # Do not recompute if origin did not move
        if (origin_x, origin_y) == self.last_origin:
            return
        self.reset()
        for ray in self.cast_rays(origin_x, origin_y):
            for x, y in ray:
                if self.is_out_of_bounds(x, y):
                    continue
                # Stop at wall tiles
                if self.game_map[x][y].is_type('wall', door=True):
                    if light_walls:
                        self.fov_map[x][y] = True
                        self.last_area.add((x, y))
                    break
                self.fov_map[x][y] = True
                self.last_area.add((x, y))
        self.last_origin = origin_x, origin_y

    def is_visible(self, x, y):
        return self.fov_map[x][y]

    def is_out_of_bounds(self, x, y):
        if x >= self.game_map.width or y >= self.game_map.height:
            return True
        if x < 0 or y < 0:
            return True
        return False
