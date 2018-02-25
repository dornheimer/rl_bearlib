from collections import defaultdict
import logging
from uuid import uuid4


logger = logging.getLogger('roguelike')


class EntityManager:
    """
    entities: {entity: {component_type: component}}
    components: {component_type: {entities}}
    """
    def __init__(self):
        self.entities = defaultdict(dict)
        self.components = defaultdict(set)

    def create_entity(self):
        return str(uuid4())

    def destroy_entity(self, entity):
        for component_type in self.entities[entity]:
            self.components[component_type].remove(entity)
        del self.entities[entity]

    def clear_all(self):
        for e in self.entities:
            self.destroy_entity(e)

    def add_component(self, entity, component):
        self.entities[entity][component._type] = component
        self.components[component._type].add(entity)

    def compose_entity(self, entity, *components):
        for component in components:
            self.add_component(entity, component)

    def remove_component(self, entity, component):
        del self.entities[entity][component._type]
        self.components[component._type].remove(entity)

    def has_component(self, entity, component_type):
        return component_type in self.entities[entity]

    def entities_with_components(self, *component_types):
        entities = set(self.components[component_types[0]])
        for ct in component_types[1:]:
            entities.intersection_update(self.components[ct])
        return entities

    def entities_at_location(self, x, y):
        entities = self.entities_with_components('Location')
        for e in entities:
            loc = self.entities[e]['Location']
            if (loc.x, loc.y) == (x, y):
                return True
        return False


class EntityComponentSystem:
    """
    active_systems: {system_type: system_instance}
    """
    def __init__(self):
        self.manager = EntityManager()
        self.active_systems = {}

    def add_system(self, system, **kwargs):
        sys = system(self, **kwargs)
        self.active_systems[str(sys)] = sys
        logger.debug(f"{sys} added")

    def update(self):
        for system_type, system in self.active_systems.items():
            system.run()
