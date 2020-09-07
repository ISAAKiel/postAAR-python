class Building:
    def __init__(self, rect):
        self.rooms = set()
        self.rooms.add(rect)
        self.ident = str([rect])

    def addRoom(self, rect):
        self.rooms.add(rect)
        self.ident = str(sorted(self.rooms))

    def hasRoom(self, rect):
        return rect in self.rooms

    def __eq__(self, other):
        return isinstance(other, Building) and self.ident == other.ident

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.ident)