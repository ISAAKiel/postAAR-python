from shapely.geometry import Polygon
import json

class Rect:
    def __init__(self, corners, posts, diff_sides_max, diff_diagonals):
        self.corners = corners.copy()
        corners.sort()
        self.ident = str(corners)

        rect_points = []
        for point in self.corners:
            rect_points.append((posts[point][1], posts[point][2]))
        self.polygon = Polygon(rect_points)
        self.diff_sides_max = diff_sides_max
        self.diff_diagonals = diff_diagonals

    def setId(self, id):
        self.id = id

    def isRectangle(self, minimum_difference):
        return (self.polygon.area / self.polygon.minimum_rotated_rectangle.area) > (1-minimum_difference)

    def toJson(self):
        return ('{ "id": ' + str(self.id) + ', "corners": ' + json.dumps(self.corners) + ', "diff_sides_max": ' + str(self.diff_sides_max) + ', "diff_diagonals": ' + str(self.diff_diagonals) + ' }')

    def __eq__(self, other):
        return isinstance(other, Rect) and self.ident == other.ident

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.ident)

    def __lt__(self, other):
        return self.ident < other.ident

    def __repr__(self):
        return '' + str(self.corners) + ', ' + str(self.ident)