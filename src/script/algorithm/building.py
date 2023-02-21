import json

from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union


class Building:
    def __init__(self, rect=None):
        self.id = -1
        self.room_ids = []
        self.rooms = set()
        self.posts = set()
        self.form = Polygon()
        if rect is not None:
            self.addRoom(rect)
        self.identity = frozenset(self.room_ids)
        self.hash = hash(self.identity)

    def copy(self):
        b = Building()
        b.rooms = set(self.rooms)
        b.posts = set(self.posts)

        b.room_ids = self.room_ids
        b.identity = self.identity
        b.hash = self.hash
        b.form = self.form

        return b

    def addRoom(self, rect):
        self.rooms.add(rect)
        self.posts |= rect.corner_set

        self.room_ids = sorted([room.id for room in self.rooms])
        self.identity = frozenset(self.room_ids)
        self.hash = hash(self.identity)
        self.form = unary_union([self.form, rect.polygon])

    def is_valid(self):
        return self.form.is_valid and isinstance(self.form, Polygon) and len(list(self.form.interiors)) == 0

    def setId(self, id):
        self.id = id

    def toJson(self):
        return ('{ "id": ' + str(self.id) + ', "rooms": [' + (", ".join(str(id) for id in self.room_ids))  + '] }')

    def hasRoom(self, rect):
        return rect.id in self.room_ids

    def is_connected_to(self, rect):
        return len(self.posts & rect.corner_set) >= 2

    def touches(self, rect):
        return self.form.touches(rect.polygon)

    def __eq__(self, other):
        return isinstance(other, Building) and self.identity == other.identity

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.hash

    def __repr__(self):
        return '[' + str(self.id) + '->' + str(self.room_ids) + ']'
