from shapely.geometry import Polygon
from shapely import affinity
from numpy import arange

def create_all_rotations(rect, distance_step, rotation_degree=10):
    rotations = []

    rotation = 0
    distance = 0
    while rotation > -360:
        new_rect = affinity.rotate(rect, rotation, 'center')
        new_rect = affinity.translate(new_rect, distance)
        rotations.append(new_rect)

        rotation -= rotation_degree
        distance += distance_step

    return rotations


def create_rectangle(xsize, ysize):
    return Polygon([[0, 0], [0, ysize], [xsize, ysize], [xsize, 0]])


def create_permutations_of_trapezoid(xsize, ysize, base_difference):
    trapezoids = []

    start = 0.0
    move = 0.1
    while start <= base_difference:
        trapezoids.append(Polygon([[0, 0], [xsize*start, ysize], [xsize*(1-base_difference)+xsize*start, ysize], [xsize, 0]]))
        start += move

    return trapezoids


def create_permutations_of_rhombus(xsize, ysize):
    rhombi = []

    start = 0.1
    move = 0.1
    while start <= 1.0:
        rhombi.append(Polygon([[0, 0], [xsize*start, ysize], [xsize+xsize*start, ysize], [xsize, 0]]))
        start += move

    return rhombi


def write_to_file(name, polygon_list):
    with open(name, 'w') as f:
        print("id,shape_id,difference_to_perfect_rect,x,y", file=f)
        pid = 0
        rid = 0
        for rect in polygon_list:
            x, y = rect.exterior.coords.xy
            for i in range(4):
                print(str(pid) + "," + str(rid) + "," + f'{int((rect.area / rect.minimum_rotated_rectangle.area)*10000)/10000:.4f}' + "," + f'{x[i]:.4f}' + "," + f'{y[i]:.4f}', file=f)
                pid += 1
            rid += 1


if __name__ == '__main__':

    shapes = []
    start_position_y = 0

    sizes = [2, 5, 10]
    sizes.sort()
    distance_between_shapes = sizes[-1]*2.5

    # rectangles
    for i, x in enumerate(sizes):
        for y in sizes[i:]:
            shapes.extend(create_all_rotations(affinity.translate(create_rectangle(x, y), yoff=start_position_y), distance_between_shapes))
            start_position_y += distance_between_shapes

    write_to_file("test_shape_rectangle.csv", shapes)
    shapes = []
    start_position_y = 0

    # trapezoids
    for i, x in enumerate(sizes):
        for y in sizes[i:]:
            for base_difference in arange(0.1, 1.0, 0.1):
                for trapezoid in create_permutations_of_trapezoid(x, y, base_difference):
                    shapes.extend(create_all_rotations(affinity.translate(trapezoid, yoff=start_position_y), distance_between_shapes))
                    start_position_y += distance_between_shapes

            write_to_file("test_shape_trapezoid_" + str(x) + "_" + str(y) + ".csv", shapes)
            shapes = []
            start_position_y = 0

    # rhombi
    for i, x in enumerate(sizes):
        for y in sizes[i:]:
            for trapezoid in create_permutations_of_rhombus(x, y):
                shapes.extend(create_all_rotations(affinity.translate(trapezoid, yoff=start_position_y), distance_between_shapes))
                start_position_y += distance_between_shapes

            write_to_file("test_shape_rombus_" + str(x) + "_" + str(y) + ".csv", shapes)
            shapes = []
            start_position_y = 0
