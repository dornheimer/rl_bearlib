import math


class Vector:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return str(tuple(self))

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({!r}, {!r})".format(class_name, *self)

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __bool__(self):
        return bool(abs(self))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __add__(self, other):
        return type(self)(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return type(self)(self.x-other.x, self.y-other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        if isinstance(other, type(self)):
            return type(self)(self.x*other.x, self.y*other.y)
        elif isinstance(other, (int, float)):
            return type(self)(self.x*other, self.y*other)

    @property
    def direction(self):
        return math.atan(self.y / self.x)
