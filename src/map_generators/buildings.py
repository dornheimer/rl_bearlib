import random as rd

from .components import Rect
from .base_generator import BaseGenerator


class Buildings(BaseGenerator):
    def __init__(self, game_map, room_min_size, room_max_size):
        super().__init__(game_map)
        self.tiles = self._initialize(tile_type='ground')
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.max_rooms = 10
        self.rooms = []
        self.distance = 3

    def generate(self):
        for r in range(self.max_rooms):
            w = rd.randint(self.room_min_size, self.room_max_size)
            h = rd.randint(self.room_min_size, self.room_max_size)
            x = rd.randint(1, self.game_map.width-w-2)
            y = rd.randint(1, self.game_map.height-h-2)
            new_room = Rect(x, y, w, h)

            x_dist, y_dist = x-self.distance, y-self.distance,
            w_dist, h_dist = w+self.distance*2, h+self.distance*2
            area_around_room = Rect(x_dist, y_dist, w_dist, h_dist)

            for other_room in self.rooms:
                if area_around_room.intersect(other_room):
                    break
            else:
                self.create_room_walls(new_room)
                self.rooms.append(new_room)

        self.assign_wall_tiles()
        return self.tiles

    def create_room_walls(self, room):
        """Block tiles along the borders of the rectangle and create door."""
        wall_tiles = []
        for y in (room.y1, room.y2):
            for x in range(room.x1, room.x2+1):
                self.fill(x, y)
                wall_tiles.append((x, y))

        for x in (room.x1, room.x2):
            for y in range(room.y1, room.y2+1):
                self.fill(x, y)
                wall_tiles.append((x, y))

        # Prevent doorway in corners or too close to the edge
        valid_doors = []
        for wt in wall_tiles:
            if wt[0] in (room.x1, room.x2):
                if room.y1+1 < wt[1] < room.y2-1:
                    valid_doors.append(wt)
            elif wt[1] in (room.y1, room.y2):
                if room.x1+1 < wt[0] < room.x2-1:
                    valid_doors.append(wt)
        door_x, door_y = rd.choice(valid_doors)
        self.tiles[door_x][door_y].set_type('door')
