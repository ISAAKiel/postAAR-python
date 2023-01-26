import json

from shapely import Polygon, MultiPolygon


class Building:
    def __init__(self, rect=None):
        self.id = -1
        self.room_ids = []
        self.rooms = set()
        self.posts = set()
        self.form = Polygon()
        if rect is not None:
            self.addRoom(rect)
        self.identity = str(self.room_ids)

    def copy(self):
        b = Building()
        for r in self.rooms:
            b.addRoom(r)
        return b

    def addRoom(self, rect):
        self.rooms.add(rect)
        for post in rect.corners:
            self.posts.add(post)
        self.room_ids = sorted([room.id for room in self.rooms])
        self.identity = str(self.room_ids)
        self.form = MultiPolygon([r.polygon for r in self.rooms])

    def setId(self, id):
        self.id = id

    def toJson(self):
        return ('{ "id": ' + str(self.id) + ', "rooms": [' + (", ".join(str(id) for id in self.room_ids))  + '] }')

    def hasRoom(self, rect):
        return rect.id in self.room_ids

    def is_connected_to(self, rect):
        connections = 0
        for corner in rect.corners:
            if corner in self.posts:
                connections += 1

        return connections >= 2

    def touches(self, rect):
        return self.form.touches(rect.polygon)

    def __eq__(self, other):
        return isinstance(other, Building) and self.identity == other.identity

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.identity)

    def __repr__(self):
        return '[' + str(self.id) + '->' + str(self.room_ids) + ']'
