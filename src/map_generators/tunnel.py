import random as rd

from .base_generator import BaseGenerator
from .helper import RectangularMixin
from src.elements import Rect


class Tunnel(BaseGenerator, RectangularMixin):
    """
    Create rectangular rooms at random locations in the dungeon and connect
    them.
    """
    def __init__(self, game_map, room_min_size, room_max_size):
        super().__init__(game_map)
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.rooms = []
        self.max_rooms = 50

    def place_doors(self, room, num_doors=None):
        valid_doors = []
        for x, y in room.border:
            if not self.tiles[x][y].tile_type == 'ground':
                continue
            if not (room.y1+1 < y < room.y2-1 or room.x1+1 < x < room.x2-1):
                continue
            north, south, east, west = self._check_adjacent_tiles(x, y, 'wall')
            door_h = not (north and south) and (east and west)
            door_v = (north and south) and not (east and west)
            if door_h or door_v:
                valid_doors.append((x, y))

        num_doors = len(valid_doors) if num_doors is None else num_doors
        doors_to_create = min(num_doors, len(valid_doors))

        rd.shuffle(valid_doors)
        for n in range(doors_to_create):
            door_x, door_y = valid_doors.pop()
            self.tiles[door_x][door_y].set_type('door')

    def generate(self):
        """
        The location and size of a room are chosen randomly and it will only
        be created if it does not overlap with previously created rooms.
        Rooms will always connect to their previous room.
        """
        num_rooms = 0
        for r in range(self.max_rooms):
            w = rd.randint(self.room_min_size, self.room_max_size)
            h = rd.randint(self.room_min_size, self.room_max_size)
            x = rd.randint(1, self.game_map.width-w-2)
            y = rd.randint(1, self.game_map.height-h-2)

            new_room = Rect(x, y, w, h)
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                if num_rooms != 0:
                    prev_room = self.rooms[num_rooms-1]
                    self.connect_rooms(new_room, prev_room)

                self.rooms.append(new_room)
                num_rooms += 1

        for r in self.rooms:
            self.place_doors(r)
        self.assign_wall_tiles()
        return self.tiles
