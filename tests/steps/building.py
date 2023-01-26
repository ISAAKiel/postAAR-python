from behave import *

from src.script.algorithm.algorithm import findBuildings
from src.script.algorithm.rect import Rect

use_step_matcher("parse")


@step('die Punkte und Rechtecke aus dem Testordner "{folder}" wurden geladen')
def step_impl(context, folder):
    context.folder = folder

    points = dict()

    with open("./tests/test_data/" + folder + "/points.csv", 'r') as datafile:
        for line in datafile:
            if line.strip().startswith('#'):
                continue

            data = line.split(",")
            try:
                points[int(data[0])] = [float(data[1]), float(data[2])]
            except ValueError as i:
                pass

    rectangles = []

    with open("./tests/test_data/" + folder + "/rectangles.csv", 'r') as datafile:
        for line in datafile:
            if line.strip().startswith('#'):
                continue

            data = line.split(",")
            try:
                rectangle = Rect([int(corner) for corner in data[1:5]], points, 0, 0)
                rectangle.setId(int(data[0]))
                rectangles.append(rectangle)
            except ValueError as i:
                pass

    context.rectangles = rectangles

    if len(points) == 0:
        raise ValueError('Es gibt keine Punkte im Ordner ' + folder)

    if len(rectangles) == 0:
        raise ValueError('Es gibt keine Rechtecke im Ordner ' + folder)


@step("nach möglichen Gebäuden gesucht wird")
def step_impl(context):
    if not hasattr(context, "rectangles"):
        raise ValueError(u'Es müssen Rechtecke vorhanden sein')

    context.found_buildings = findBuildings(context.rectangles, number_of_computercores=1)


@step("werden alle möglichen Gebäude gefunden")
def step_impl(context):
    if not hasattr(context, "found_buildings"):
        raise ValueError(u'Es muss nach Gebäuden gesucht worden sein')

    found_buildings = []
    for found_building in context.found_buildings:
        found_buildings.append(found_building.room_ids)

    expected_buildings = []

    with open("./tests/test_data/" + context.folder + "/buildings.csv", 'r') as datafile:
        for line in datafile:
            if line.strip().startswith('#'):
                continue

            data = line.split(",")
            try:
                expected_buildings.append([int(rectangle) for rectangle in data])
            except ValueError as i:
                pass

    if len(expected_buildings) == 0:
        raise ValueError('Es gibt keine Gebäude im Ordner ' + context.folder)

    error = ""

    buildings_not_found = []
    for expected_building in expected_buildings:
        if not is_building_in_list(expected_building, found_buildings):
            buildings_not_found.append(expected_building)

    if len(buildings_not_found) > 0:
        error += "\nMissing buildings: " + str(buildings_not_found)

    extra_buildings_found = []
    for found_building in found_buildings:
        if not is_building_in_list(found_building, expected_buildings):
            extra_buildings_found.append(found_building)

    if len(extra_buildings_found) > 0:
        error += "\nExtra buildings: " + str(extra_buildings_found)

    if error:
        raise AssertionError("The list of constructed buildings " + str(found_buildings) + " is wrong!" + error)


def is_building_in_list(building, building_list):
    for b in building_list:
        if same_building(building, b):
            return True

    return False


def same_building(building, b):
    if len(building) != len(b):
        return False
    for r in b:
        if r not in building:
            return False
    return True
