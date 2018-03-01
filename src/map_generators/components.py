class Rect:
    """
    Rectangle representing a room in the dungeon.
    """
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.x1}, {self.y1}, {self.x2}, {self.y2})"

    @property
    def center(self):
        """Calculate center coordinates of a rectangle."""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    @property
    def border(self):
        border = []
        for y in (self.y1, self.y2):
            for x in range(self.x1, self.x2+1):
                border.append((x, y))

        for x in (self.x1, self.x2):
            for y in range(self.y1, self.y2+1):
                border.append((x, y))

        return border

    def intersect(self, other):
        """
        Return True if this rectangle intersects with another one.
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    @classmethod
    def from_center(cls, center_x, center_y, w, h):
        x = int(center_x - w)
        y = int(center_y - h)
        new_w = int(w * 2)
        new_h = int(h * 2)
        print("visible_area computed")
        return cls(x, y, new_w, new_h)
