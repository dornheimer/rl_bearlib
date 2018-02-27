from abc import ABCMeta, abstractmethod


class System(metaclass=ABCMeta):
    requires = []

    def __init__(self, ecs):
        self.ecs = ecs

    def __str__(self):
        return type(self).__name__

    @property
    def subscribed_entities(self):
        return self.ecs.manager.entities_with_components(*self.requires)

    def is_subscribed(self, entity):
        return entity in self.subscribed_entities

    @abstractmethod
    def run(self):
        pass


class MovementSystem(System):
    requires = ['Location', 'Velocity']

    def __init__(self, ecs, game_map):
        super().__init__(ecs)
        self.game_map = game_map

    def move(self, entity, dx, dy):
        loc = self.ecs.manager.entities[entity]['Location']
        vel = self.ecs.manager.entities[entity]['Velocity']
        vel.x, vel.y = dx, dy
        dest = loc + vel

        if self.game_map.is_blocked(dest.x, dest.y):
            return False
        if self.ecs.manager.entities_at_location(dest.x, dest.y):
            return False

        loc += vel
        return True

    def run(self):
        for s_e in self.subscribed_entities:
            if self.ecs.manager.has_component(s_e, 'Input'):
                actor_action = self.ecs.manager.entities[s_e]['Input'].action
            else:
                actor_action = self.ecs.manager.entities[s_e]['AI'].action
            if actor_action.get('move'):
                dx, dy = actor_action['move']
                self.move(s_e, dx, dy)


class PlayerSystem(System):
    requires = ['Player']

    @property
    def player(self):
        return self.subscribed_entities.pop()

    def move_player(self, player_action):
        dx, dy = player_action['move']
        self.ecs.active_systems['MovementSystem'].move(self.player, dx, dy)

    def run(self):
        input_component = self.ecs.manager.entities[self.player]['Input']
        player_action = input_component.action
        if player_action.get('move'):
            pass  # Handled by movement system
