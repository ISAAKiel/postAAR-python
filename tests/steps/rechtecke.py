from warnings import warn

from behave import *

import src.script.algorithm.helper as hlp
import src.script.algorithm.algorithm as alg

use_step_matcher("parse")


@step('die Punkte aus dem Test- und Kontrollset "{filename}" aus dem Ordner "{folder}" wurden geladen')
def step_impl(context, filename, folder):
    points = {}
    control = {}

    with open("./tests/test_data/" + folder + "/" + filename, 'r') as datafile:
        for line in datafile:
            data = line.split(",")
            try:
                points[int(data[0])] = [float(data[1]), float(data[2])]

                part_of_rectangle = data[3].strip()
                if part_of_rectangle not in control:
                    control[part_of_rectangle] = TestRect()
                    control[part_of_rectangle].difference_to_ideal_rectangle = float(data[4])
                    control[part_of_rectangle].minimum_length_of_side = float(data[5])
                    control[part_of_rectangle].maximum_length_of_side = float(data[6])
                control[part_of_rectangle].corners.append(int(data[0]))
                control[part_of_rectangle].build_ident()

            except ValueError as i:
                pass

    context.points = points
    context.control = list(control.values())

    if len(points) == 0:
        raise ValueError('Es gibt keine Punkte in ' + folder + "/" + filename)


@step('die Punkte und erwarteten Rechtecke aus dem Testordner "{folder}" wurden geladen')
def step_impl(context, folder):
    points = {}

    with open("./tests/test_data/" + folder + "/points.csv", 'r') as datafile:
        for line in datafile:
            if line.strip().startswith('#'):
                continue

            data = line.split(",")
            try:
                points[int(data[0])] = [float(data[1]), float(data[2])]
            except ValueError as i:
                pass

    context.points = points
    context.folder = folder

    control = []

    with open("./tests/test_data/" + folder + "/rectangles.csv", 'r') as datafile:
        for line in datafile:
            if line.strip().startswith('#'):
                continue

            data = line.split(",")
            try:
                rectangle = TestRect()
                rectangle.corners = [int(corner) for corner in data[1:5]]

                rectangle.difference_to_ideal_rectangle = float(data[5])
                rectangle.minimum_length_of_side = float(data[6])
                rectangle.maximum_length_of_side = float(data[7])

                rectangle.build_ident()

                control.append(rectangle)
            except ValueError as i:
                pass

    context.control = control

    if len(points) == 0:
        raise ValueError('Es gibt keine Punkte im Ordner ' + folder)


@step('die erwarteten Rechtecke sollen eine maximale Differenz von "{difference_to_ideal_rectangle:g}" Prozent haben')
def step_impl(context, difference_to_ideal_rectangle):
    context.difference_to_ideal_rectangle = difference_to_ideal_rectangle / 100


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
    context.found_rectangles = alg.find_rects(windows, context.points, context.maximum_length_of_side,
                                              context.minimum_length_of_side, context.difference_to_ideal_rectangle,
                                              number_of_computercores=1, debug=False)


@step("werden nur die Rechtecke gefunden die zu den Parametern passen")
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
        assert is_rectangle_in_list(context.found_rectangles, rectangle_that_should_be_found), "The rectangle " + str(
            rectangle_that_should_be_found) + " has not been found! (Found rectangles:" + str(
            context.found_rectangles) + ")"

    assert not len(rectangles_that_should_be_found) < len(context.found_rectangles), \
        "More rectangles found(" + str(len(context.found_rectangles)) + " than expected(" + str(
            len(rectangles_that_should_be_found)) + "):\n" + str(rectangles_that_should_be_found) + "\n" + str(
            context.found_rectangles)


@step("nach den Rechtecken mit den Parametern in der Liste gesucht wird")
def step_impl(context):
    if not hasattr(context, "points"):
        raise ValueError(u'Es müssen Punkte vorhanden sein')

    context.results = []

    for row in context.table:
        result = Result()
        result.maximum_length_of_side = float(row['Maximum'])
        result.minimum_length_of_side = float(row['Minimum'])
        result.max_difference_to_ideal_rectangle = float(row['Differenz']) / 100

        windows = hlp.buildWindows(context.points, result.maximum_length_of_side)
        result.found_rectangles = alg.find_rects(windows, context.points, result.maximum_length_of_side,
                                                 result.minimum_length_of_side,
                                                 result.max_difference_to_ideal_rectangle, number_of_computercores=1,
                                                 debug=False)

        context.results.append(result)


@step("werden nur die Rechtecke gefunden die zu den Parametern in der Liste passen")
def step_impl(context):
    if not hasattr(context, "control"):
        raise ValueError(u'Es müssen Kontrollwerte gegeben sein')

    for result in context.results:
        expected_rectangles = list(filter(
            lambda rectangle:
            rectangle.difference_to_ideal_rectangle <= result.max_difference_to_ideal_rectangle and
            rectangle.minimum_length_of_side >= result.minimum_length_of_side and
            rectangle.maximum_length_of_side <= result.maximum_length_of_side,
            context.control))

        for expected_rectangle in expected_rectangles:
            if not is_rectangle_in_list(result.found_rectangles, expected_rectangle):
                if not value_at_border(expected_rectangle, result):
                    raise AssertionError("The rectangle " + str(expected_rectangle) + " has not been found!\n" + str(result))
                else:
                    warn("The rectangle " + str(expected_rectangle) + " has not been found!\n" + str(result))

        if len(expected_rectangles) < len(result.found_rectangles):
            more = subtract(result.found_rectangles, expected_rectangles)
            for extra_rectangle in more:
                match = get_rectangle_in_list(context.control, extra_rectangle)
                if match is None or match.difference_to_ideal_rectangle - result.max_difference_to_ideal_rectangle > 0.01:
                    raise AssertionError("Found unexpected rectangle:" + str(extra_rectangle) + "\n" + str(
                        expected_rectangles) + "\n" + str(result))


def value_at_border(rectangle, result):
    if abs(rectangle.difference_to_ideal_rectangle - result.max_difference_to_ideal_rectangle) < 0.01:
        return True
    if abs(rectangle.minimum_length_of_side - result.minimum_length_of_side) < 0.01:
        return True
    if abs(rectangle.maximum_length_of_side - result.maximum_length_of_side) < 0.01:
        return True
    return False


def subtract(list1, list2):
    rest = []
    for rectangle_to_remove in list1:
        if not is_rectangle_in_list(list2, rectangle_to_remove):
            rest.append(rectangle_to_remove)
    return rest


def is_rectangle_in_list(list_of__rectangles, rectangle):
    return get_rectangle_in_list(list_of__rectangles, rectangle) is not None


def get_rectangle_in_list(list_of__rectangles, rectangle):
    for rectangle_in_list in list_of__rectangles:
        if rectangle_in_list.ident == rectangle.ident:
            if same_rectangles(rectangle_in_list, rectangle) or same_rectangles(rectangle_in_list, rectangle,
                                                                                clockwise=False):
                return rectangle_in_list
    return None


def same_rectangles(rectangle1, rectangle2, clockwise=True):
    shift = rectangle1.corners.index(rectangle2.corners[0])
    for i, point in enumerate(rectangle2.corners):
        if not point == rectangle1.corners[
            ((shift + (i if clockwise else -i)) + len(rectangle2.corners)) % len(rectangle2.corners)]:
            return False
    return True


class Result:
    def __init__(self):
        self.max_difference_to_ideal_rectangle = 0
        self.minimum_length_of_side = 0
        self.maximum_length_of_side = 0
        self.found_rectangles = []

    def __repr__(self):
        return "Result for " + str(self.max_difference_to_ideal_rectangle * 100) + "% " + str(
            self.minimum_length_of_side) + "<->" + str(self.maximum_length_of_side) + ": " + str(self.found_rectangles)


class TestRect:
    def __init__(self):
        self.corners = []
        self.difference_to_ideal_rectangle = 0
        self.minimum_length_of_side = 0
        self.maximum_length_of_side = 0

        self.ident = ""

    def build_ident(self):
        ident = self.corners.copy()
        ident.sort()
        self.ident = str(ident)

    def __repr__(self):
        return str(self.corners) + "-" + str(self.difference_to_ideal_rectangle) + "-" + str(
            self.minimum_length_of_side) + "-" + str(self.maximum_length_of_side)


