import json

class Building:
    def __init__(self, rect=None):
        self.rooms = set()
        if rect is not None:
            self.rooms.add(rect)
            self.ident = str([rect])

    def addRoom(self, rect):
        self.rooms.add(rect)
        self.ident = str(sorted(self.rooms))

    def setId(self, id):
        self.id = id

    def toJson(self):
        return ('{ "id": ' + str(self.id) + ', "rooms": [' + (", ".join(str(rectangle.id) for rectangle in self.rooms))  + '] }')

    def hasRoom(self, rect):
        return rect in self.rooms

    def __eq__(self, other):
        return isinstance(other, Building) and self.ident == other.ident

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.ident)