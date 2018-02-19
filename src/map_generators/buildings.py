import random as rd

from .components import Rect
from .base_generator import BaseGenerator
from .helper import RectangularMixin


class Buildings(BaseGenerator, RectangularMixin):
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
                self.place_doors(new_room)
                self.rooms.append(new_room)

        self.assign_wall_tiles()
        return self.tiles

    def place_doors(self, room):
        # Prevent doorway in corners or too close to the edge
        valid_doors = []
        for x, y in room.border:
            if room.y1+1 < y < room.y2-1 or room.x1+1 < x < room.x2-1:
                valid_doors.append((x, y))
        door_x, door_y = rd.choice(valid_doors)
        self.tiles[door_x][door_y].set_type('door')
