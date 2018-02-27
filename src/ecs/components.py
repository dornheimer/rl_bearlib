class Component:
    @property
    def _type(self):
        return type(self).__name__

    def __repr__(self):
        return f"{self._type}(**{vars(self)})"


class Location(Component):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


class Physical(Component):
    def __init__(self, *, blocks=False):
        self.blocks = blocks


class Appearance(Component):
    def __init__(self, *, char='?', color='white'):
        self.char = char
        self.color = color


class Name(Component):
    def __init__(self, *, name):
        self.name = name


class Description(Component):
    def __init__(self, *, name):
        self.name = name


class Player(Component):
    pass


class Input(Component):
    def __init__(self, input_handler):
        self.input_handler = input_handler

    @property
    def action(self):
        return self.input_handler.action
