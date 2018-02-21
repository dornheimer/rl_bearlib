from abc import ABCMeta, abstractmethod


class System(metaclass=ABCMeta):
    requires = []

    def __init__(self, ecs):
        self.ecs = ecs

    def __str__(self):
        return type(self).__name__

    def has_entity(self, entity):
        return entity in self.get_entities()

    def get_entities(self):
        entities = []
        for e in self.ecs.manager.entities:
            matching = all([self.ecs.manager.has_component(e, c)
                            for c in self.requires])
            if matching:
                entities.append(e)
        return entities

    @abstractmethod
    def run(self):
        pass


class MovementSystem(System):
    requires = ['Location']

    def __init__(self, ecs, game_map):
        super().__init__(ecs)
        self.game_map = game_map

    def move(self, entity, dx, dy):
        loc = self.ecs.manager.entities[entity]['Location']
        dest_x = loc.x + dx
        dest_y = loc.y + dy

        if self.game_map.is_blocked(dest_x, dest_y): #or self.ecs.manager.entities_at_location(dest_x, dest_y):
            return False

        loc.x += dx
        loc.y += dy
        return True

    def run(self):
        pass


class PlayerSystem(System):
    requires = ['Player']

    def __init__(self, ecs, input_handler):
        super().__init__(ecs)
        self.input_handler = input_handler

    def move_player(self, player):
        if self.input_handler.action.get('move'):
            print(self.input_handler.action)
            dx, dy = self.input_handler.action['move']
            self.ecs.active_systems['MovementSystem'].move(player, dx, dy)

    def run(self):
        player = self.get_entities()[0]
        self.move_player(player)
