from behave import *

import src.script.algorithm.helper as hlp
import src.script.algorithm.algorithm as alg

use_step_matcher("parse")


@step('die Punkte aus dem Test- und Kontrollset "{filename}" wurden geladen')
def step_impl(context, filename):
    points = []
    control = {}

    with open("./testsets/" + filename, 'r') as datafile:
        for line in datafile:
            data = line.split(",")
            try:
                points.append([int(data[0]), float(data[1]), float(data[2])])

                part_of_rectangle = data[3].strip()
                if part_of_rectangle not in control:
                    control[part_of_rectangle] = TestRect()
                    control[part_of_rectangle].difference_to_ideal_rectangle = float(data[4])
                    control[part_of_rectangle].minimum_length_of_side = float(data[5])
                    control[part_of_rectangle].maximum_length_of_side = float(data[6])
                control[part_of_rectangle].corners.append(int(data[0]))

            except ValueError as i:
                pass

    context.points = points
    context.control = list(control.values())

    if len(points) == 0:
        raise ValueError('Es gibt keine Punkte in ' + filename)


@step('die erwarteten Rechtecke sollen eine maximale Differenz von "{difference_to_ideal_rectangle:g}" Prozent haben')
def step_impl(context, difference_to_ideal_rectangle):
    context.difference_to_ideal_rectangle = difference_to_ideal_rectangle/100


@step('die erwarteten Rechtecke sollen eine Seitenlänge zwischen "{minimum_length_of_side:g}" und "{maximum_length_of_side:g}" haben')
def step_impl(context, minimum_length_of_side, maximum_length_of_side):
    context.minimum_length_of_side = minimum_length_of_side
    context.maximum_length_of_side = maximum_length_of_side


@step("nach den Rechtecken gesucht wird")
def step_impl(context):
    if not hasattr(context, "points"):
        raise ValueError(u'Es müssen Punkte vorhanden sein')
    if not hasattr(context, "difference_to_ideal_rectangle"):
        raise ValueError(u'Es muss eine Differenz zum idealen Rechteck gegeben sein')
    if not hasattr(context, "minimum_length_of_side"):
        raise ValueError(u'Es muss eine minimale Länge gegeben sein')
    if not hasattr(context, "maximum_length_of_side"):
        raise ValueError(u'Es muss eine maximale Länge gegeben sein')

    windows = hlp.buildWindows(context.points, context.maximum_length_of_side)
    context.found_rectangles = alg.find_rects(windows, context.points, context.maximum_length_of_side, context.minimum_length_of_side, context.difference_to_ideal_rectangle, number_of_computercores=1, debug=False)


@step("werden nur die Rechtecke gefunden die zu den Werten passen")
def step_impl(context):
    if not hasattr(context, "found_rectangles"):
        raise ValueError(u'Es muss nach Rechtecken gesucht worden sein')
    if not hasattr(context, "control"):
        raise ValueError(u'Es müssen Kontrollwerte gegeben sein')

    rectangles_that_should_be_found = list(filter(
        lambda rectangle:
            rectangle.difference_to_ideal_rectangle <= context.difference_to_ideal_rectangle and
            rectangle.minimum_length_of_side >= context.minimum_length_of_side and
            rectangle.maximum_length_of_side <= context.maximum_length_of_side,
        context.control))

    for rectangle_that_should_be_found in rectangles_that_should_be_found:
        assert has_rectangle_been_found(context.found_rectangles, rectangle_that_should_be_found), "The rectangle " + str(rectangle_that_should_be_found) + " has not been found! (Found rectangles:" + str(context.found_rectangles) + ")"

    assert not len(rectangles_that_should_be_found) < len(context.found_rectangles), \
        "More rectangles found(" + str(len(context.found_rectangles)) + " than expected(" + str(len(rectangles_that_should_be_found)) + "):\n" + str(rectangles_that_should_be_found) + "\n" + str(context.found_rectangles)


def has_rectangle_been_found(found_rectangles, rectangle_that_should_be_found):
    ident = rectangle_that_should_be_found.corners.copy()
    ident.sort()
    ident = str(ident)
    for found_rectangle in found_rectangles:
        if found_rectangle.ident == ident:
            if same_rectangles(found_rectangle, rectangle_that_should_be_found.corners) or same_rectangles(found_rectangle, rectangle_that_should_be_found.corners, clockwise=False):
                return True
    return False


def same_rectangles(rectangle, corners, clockwise=True):
    shift = rectangle.corners.index(corners[0])
    for i, point in enumerate(corners):
        if not point == rectangle.corners[((shift+(i if clockwise else -i))+len(corners)) % len(corners)]:
            return False
    return True


class TestRect:
    def __init__(self):
        self.corners = []
        self.difference_to_ideal_rectangle = 0
        self.minimum_length_of_side = 0
        self.maximum_length_of_side = 0

    def __repr__(self):
        return str(self.corners) + "-" + str(self.difference_to_ideal_rectangle) + "-" + str(self.minimum_length_of_side) + "-" + str(self.maximum_length_of_side)