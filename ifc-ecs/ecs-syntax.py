from uuid import uuid4, UUID
from abc import abstractmethod
from json import dumps, loads

def is_uuid(id: str):
    try:
        UUID(hex = id)
    except ValueError:
        return False
    return True


class Component(dict):
    """
    A Component is a set of key-value pairs associated with a particular entity

    All components must have two keys: entity_id which is the entity the component applies to, and id, the of the component itself
    """

    def __init__(self, entity_id: str, id: str = None) -> None:
        """
        Not that is_uuid will raise
        """
        super(Component, self).__init__()
        if not is_uuid(entity_id):
            raise ValueError(f"{entity_id} is a badly formed UUID")
        if not is_uuid(id):
            raise ValueError(f"{id} is a badly formed UUID")
            
        self.__setitem__('entity_id', entity_id)
        if id is None:
            self.__setitem__('id', uuid4())
        else:
            self.__setitem__('id', id)
    
    @staticmethod
    def from_dict(data: dict):
        if 'id' not in data or 'entity_id' not in data:
            raise KeyError("A component must have an 'entity_id' and 'id' key")
        if not is_uuid(data['entity_id']):
            raise ValueError(f"{data['entity_id']} is a badly formed UUID")
        if not is_uuid(data['id']):
            raise ValueError(f"{data['id']} is a badly formed UUID")
        
        # now we know data is a fine dict

        c = Component(data['entity_id'], data['id'])
        for k,v in data.items():
            c[k] = v
        
        return c

    
    def __setitem__(self, __key, __value) -> None:
        if __key in ("entity_id", "id"):
            if not is_uuid(__value):
                raise ValueError("'entity_id' and 'id' must be UUIDs")
        return super().__setitem__(__key, __value)

    def __delitem__(self, __key) -> None:
        if __key in ("entity_id", "id"):
            raise KeyError("Cannot remove 'entity_id' or 'id' from a Component")
        return super().__delitem__(__key)
    
    def clear(self) -> None:
        id = self['id']
        entity_id = self['entity_id']
        result = super().clear()
        self['id'] = id
        self['entity_id'] = entity_id
        return result
    
class ECSContainer:
    """
    A ECSContainer represents a backing store for a collection of Components.
 
    Concrete subclasses implement the core methods of Repository, which
    intentionally mirror standard HTTP verbs, including idempotency expectations.
    """

    def __init__(self):
        pass

    @staticmethod
    def new_id():
        return str(uuid4())

    @abstractmethod
    def has_id(self, id) -> bool:
        """
        Returns a boolean whether the ECSContainer contains id. 
        """

    @abstractmethod
    def get(self, entity: str):
        """
        Fetches the components associated with entity id.

        In an HTTP implementation, maps to GET /ecs/:id
        """

    @abstractmethod
    def put(self, component: Component):
        """
        Add a new component. If the component id already exists, it replaces it.

        In an HTTP implementation, maps to PUT /ecs/:id
        where :id is retrieved from the bindings.
        """


class InMemoryECSContainer:
    """
    An in-memory container of ECS data.

    The data is stored as a dictionary of entities. Each entity is stored as a dictionary of components, and returned as a list/generator of components.
    """
    def __init__(self, json: str):
        self.entities = {}
        if json is not None:
            components = loads(json)
            for c in components: # need to check that the json is in fact a list of objects
                self.put(Component.from_dict(c))

    def has_id(self, entity_id: str) -> bool:
        return entity_id in self.entities.keys()
    
    def get(self, entity_id):
        return list(self.entities.get(entity_id, {}).values())

    def get_value(self, entity_id, key):
        for c in self.entities[entity_id].values():
            if key in c:
                return c[key]
        #raise KeyError(f"No property {key} is associated with entity {entity_id} in this Container.")
        return None
        
    def put(self, component):
        if not self.has_id(component['entity_id']):
            self.entities[component['entity_id']] = {}
        self.entities[component['entity_id']][component['id']] = component
    
    def get_components(self) -> list:
        components = []
        for entity_components in self.entities.values():
            components.extend(entity_components.values())
        return components
    
    def to_json(self) -> str:
        return dumps( self.get_components )


if __name__ == "__main__":
    json = '''
    [
        {"id": "19726919-6885-4809-9553-bf10cf127a05",
        "entity_id": "ac2a92c0-a34c-43e7-862d-fa91d850a35d",
        "height": 3500,
        "width": 4523},
        {"id": "540bdbcb-d7c7-41f4-a7bc-85cf47cded00",
        "entity_id": "ac2a92c0-a34c-43e7-862d-fa91d850a35d",
        "colour": "blue"},
        {"id": "a7b0afcd-57d6-45ec-8e59-0e011f2dc217",
        "entity_id": "324ff06b-5419-4b03-9a3e-857fb53ffc5f",
        "height": 5000,
        "width": 10000},
        {"id": "4a3dfc8b-bf2a-4aa2-9c0d-0437f6db08a5",
        "entity_id": "324ff06b-5419-4b03-9a3e-857fb53ffc5f",
        "colour": "green"}
    ]'''

    container = InMemoryECSContainer(json)

    print(container.get_components())
    print('----')
    print(container.get('ac2a92c0-a34c-43e7-862d-fa91d850a35d'))
    print('----')
    print(container.get('324ff06b-5419-4b03-9a3e-857fb53ffc5f'))

    print(f"ac2a92c0...: height: {container.get_value('ac2a92c0-a34c-43e7-862d-fa91d850a35d', 'height')}, width: {container.get_value('ac2a92c0-a34c-43e7-862d-fa91d850a35d', 'width')}")
    print(f"ac2a92c0...: colour: {container.get_value('ac2a92c0-a34c-43e7-862d-fa91d850a35d', 'colour')}")
    print(f"ac2a92c0...: weigth: {container.get_value('ac2a92c0-a34c-43e7-862d-fa91d850a35d', 'weight')}")