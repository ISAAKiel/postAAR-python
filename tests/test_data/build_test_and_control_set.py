# Zum Erstellen eines Punkt-, Rechteck- und Gebäudesets

# Name des Sets. Wird allen Dateien vorangestellt, i.e x.points.csv, x.rectangles.csv, x.buildings.csv
set_name = "rectangle_square_over_square_1-3"

# Die Liste der Punkte.
# Format ist [id, x, y]
points = [[0, 0, 0], [1, 0, 1], [2, 1, 1], [3, 1, 0], [4, 1, -1], [5, 0, -1], [6, -1, -1], [7, -1, 0], [8, -1, 1], [9, 0, 2], [10, 2, 0], [11, 0, -2], [12, -2, 0]]

# Die Liste der Rechtecke.
# Ecken im oder gegen Uhrzeigersinn. Format ist [id, point-id, point-id, point-id, point-id]
rectangles = [[0, 0, 1, 2, 3], [1, 0, 3, 4, 5], [2, 0, 5, 6, 7], [3, 0, 7, 8, 1], [4, 7, 8, 2, 3], [5, 6, 7, 3, 4], [6, 6, 8, 1, 5], [7, 5, 1, 2, 4], [8, 2, 4, 6, 8], [9, 1, 3, 5, 7], [10, 0, 4, 11, 6], [11, 0, 6, 12, 8], [12, 0, 8, 9, 2], [13, 0, 2, 10, 4], [14, 6, 12, 9, 2], [15, 11, 6, 2, 10], [16, 11, 12, 8, 4], [17, 4, 8, 9, 10], [18, 9, 10, 11, 12]]

# Die Liste der Gebäude.
# Können aus unterschiedlich vielen Rechtecken bestehen. Format ist [rectangle-id, rectangle-id, ...]
buildings = [[0, 1, 2, 3], [0, 1, 6], [2, 3, 7], [3, 0, 5], [1, 2, 4], [4, 5], [6, 7], [10, 11, 12, 13], [10, 13, 14], [11, 12, 15], [12, 13, 16], [10, 11, 17], [14, 15], [16, 17]]

import os
import math
from shapely.geometry import Polygon

def get_side_lengths(x_points, y_points):
    shortest = 999999
    longest = 0

    for i in range(4):
        length = math.sqrt(math.pow(x_points[i]-x_points[i+1], 2) + math.pow(y_points[i]-y_points[i+1], 2))
        if length < shortest:
            shortest = length
        if length > longest:
            longest = length

    return shortest, longest

try:
    os.mkdir(set_name)
except FileExistsError as error:
    pass

with open(set_name + "/points.csv", 'w') as f:
    print("# " + str(points), file=f)
    print("id,x,y", file=f)
    for point in points:
        print(str(point[0]) + "," + str(point[1]) + "," + str(point[2]), file=f)

with open(set_name + "/rectangles.csv", 'w') as f:
    print("# " + str(rectangles), file=f)
    print("id,corner-point-id,corner-point-id,corner-point-id,corner-point-id,difference_to_perfect_rect,shortest_side_length,longest_side_length", file=f)
    for rectangle in rectangles:
        rectangle_polygon = Polygon([
            next(point for point in points if point[0] == rectangle[1])[1:],
            next(point for point in points if point[0] == rectangle[2])[1:],
            next(point for point in points if point[0] == rectangle[3])[1:],
            next(point for point in points if point[0] == rectangle[4])[1:]
        ])
        difference_to_perfect_rect = int((1-(rectangle_polygon.area / rectangle_polygon.minimum_rotated_rectangle.area))*100)/100
        x, y = rectangle_polygon.exterior.coords.xy
        shortest_side_length, longest_side_length = get_side_lengths(x, y)

        print(str(rectangle[0]) + "," + str(rectangle[1]) + "," + str(rectangle[2]) + "," + str(rectangle[3]) + "," + str(rectangle[4]) + "," + f'{difference_to_perfect_rect:.2f}' + "," + f'{shortest_side_length:.4f}' + "," + f'{longest_side_length:.4f}', file=f)

    with open(set_name + "/buildings.csv", 'w') as f:
        print("# " + str(buildings), file=f)
        print("rectangle-id, rectangle-id, ...", file=f)
        for building in buildings:
            print(",".join([str(r) for r in building]), file=f)