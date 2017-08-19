from enum import Enum
import random

from MTG import gameobject
from MTG import cards
from MTG import card
from MTG import permanent

class ZoneType(Enum):
    LIBRARY = 0
    HAND = 1
    BATTLEFIELD = 2
    GRAVEYARD = 3
    STACK = 4
    EXILE = 5
    # COMMAND = 6

class Zone():
    def __init__(self, controller=None, elements:list=None):
        if elements is None:
            self.elements = []
        else:
            self.elements = elements
            for ele in elements:
                ele.controller = controller
        self.controller = controller


    def __repr__(self):
        return 'zone.Zone %r len=%r\n%r' % (self.__class__.__name__,
                                            len(self), self.elements)
    def __len__(self):
        return len(self.elements)

    def __bool__(self):
        return bool(self.elements)

    def __getitem__(self, pos):
        return self.elements[pos]
        
    def add(self, obj):
        if type(obj) is str:  # convert string (card's name) to a Card object
            obj = cards.card_from_name(obj)

        if type(obj) is list:
            for o in obj:
                o.zone = self.zone_type
                if not isinstance(self, Stack):
                    assert isinstance(o, gameobject.GameObject)
                o.controller = self.controller
            self.elements.extend(obj)
            return


        if not isinstance(self, Stack):
            assert isinstance(obj, gameobject.GameObject)
            obj.controller = self.controller

        obj.zone = self.zone_type
        self.elements.append(obj)
        return obj
        


    def remove(self, obj):
        if type(obj) is list:
            return all([self.remove(o) for o in obj])

        try:
            self.elements.remove(obj)
            return True
        except ValueError:
            return False

    def filter(self, characteristics=None):
        found = []
        assert (characteristics is None 
                or type(characteristics) is gameobject.Characteristics)
        
        for ele in self:
            if ele.characteristics.satisfy(characteristics):
                found.append(ele)

        return found

    def get_card_by_name(self, name):
        cards = self.filter(gameobject.Characteristics(name=name))
        if cards:
            return cards[0]
        else:
            return None


    def pop(self, pos=-1):
        return self.elements.pop(pos)





class Battlefield(Zone):
    zone_type = ZoneType.BATTLEFIELD

    def add(self, obj):
        if type(obj) is str:  # convert string (card's name) to a Card object
            obj = cards.card_from_name(obj)
        obj.controller = self.controller

        if isinstance(obj, card.Card):  # convert card to Permanent
            obj = permanent.make_permanent(obj)
        else:
            obj.zone = self.zone_type
            self.elements.append(obj)
            obj.status = permanent.Status()  # reset status upon entering battlefield
    pass

class Stack(Zone):
    zone_type = ZoneType.STACK
    pass

class Hand(Zone):
    zone_type = ZoneType.HAND
    pass

class Graveyard(Zone):
    zone_type = ZoneType.GRAVEYARD
    pass

class Exile(Zone):
    zone_type = ZoneType.EXILE
    pass

class Library(Zone):
    zone_type = ZoneType.LIBRARY

    def shuffle(self):
        random.shuffle(self.elements)

    def __init__(self, controller=None, elements:list=None):
        super(Library, self).__init__(controller, elements)
        for ele in self.elements:
            ele.zone = ZoneType.LIBRARY
        self.shuffle()
