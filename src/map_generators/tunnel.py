import random as rd

from .base_generator import BaseGenerator
from .helper import RectangularMixin
from .components import Rect


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
            x = rd.randint(0, self.game_map.width-w-1)
            y = rd.randint(0, self.game_map.height-h-1)

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

        return self.tiles
