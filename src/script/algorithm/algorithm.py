import time
from multiprocessing import Pool

from .building import Building
from .helper import *
from .rect import Rect


def calcRectsInWindow (window, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference, distances):
    rects = set()

    for a in window:
        for b in window:
            if a == b:
                break

            dist_side_ab = distances[a][b]

            if minimal_length_of_side <= dist_side_ab <= maximal_length_of_side:
                for d in window:
                    if d == b or d == a:
                        break

                    dist_side_ad = distances[a][d]
                    
                    if minimal_length_of_side <= dist_side_ad <= maximal_length_of_side:
                        
                        for potential_c in window:
                            
                            dist_side_bc = distances[b][potential_c]
                            dist_side_dc = distances[d][potential_c]
                                
                            if (
                                minimal_length_of_side <= dist_side_bc <= maximal_length_of_side and 
                                minimal_length_of_side <= dist_side_dc <= maximal_length_of_side and

                                intersect(a, potential_c, b, d, posts)
                                ):


                                possible_rect = Rect([a, b, potential_c, d], posts, 0, 0)
                        
                                if possible_rect.isRectangle(maximal_bounding_area_difference):
                                    rects.add(possible_rect)
    return rects


def look_at_windows(windows, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference, distances):
    calculated_rects = []
    for window in windows:
        calculated_rects.append(calcRectsInWindow(window, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference, distances))

    found_rects = []
    for rects_in_window in calculated_rects:
        found_rects += rects_in_window

    return found_rects

def find_rects(windows, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference, number_of_computercores=4, debug=True):
    progress = ProgressReport()

    distances = calcDistance(windows, posts, maximal_length_of_side, minimal_length_of_side)

    calculated_rects = []
    if number_of_computercores > 1:
        with Pool(processes=number_of_computercores) as pool:

            window_pool = dict()
            for i in range(number_of_computercores):
                window_pool[i] = []
            for i in range(len(windows)):
                window_pool[i % number_of_computercores].append(windows[i])

            results = []
            for w in window_pool.values():
                results.append(pool.apply_async(look_at_windows, (w, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference, distances, )))

            current_calculated_windows = 0
            for result in results:
                calculated_rects.append(result.get())

                if debug:
                    current_calculated_windows += 1
                    progress.printProgress('Calculating rects', current_calculated_windows/len(windows))

            found_rects = []
            for rects_in_window in calculated_rects:
                found_rects += rects_in_window
    else:
        results = []
        current_calculated_windows = 0
        for w in windows:
            calculated_rects.append(calcRectsInWindow(w, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference, distances ))

            if debug:
                current_calculated_windows += 1
                progress.printProgress('Calculating rects', current_calculated_windows/len(windows))
    
        found_rects = []
        for rects_in_window in calculated_rects:
            found_rects += rects_in_window

    rectangles = list(set(found_rects))

    id = 0
    for rect in rectangles:
        rect.setId(id)
        id += 1

    return rectangles

def findBuildings(found_rects, posts=None, number_of_computercores=4):

    if number_of_computercores > 1:
        pool = Pool(processes=number_of_computercores)

        building_lists = []
        building_list = []
        divider = int(len(found_rects)/number_of_computercores) + 1
        i = 0
        for rect in found_rects:
            building_list.append(Building(rect))
            i += 1
            if i%divider == 0:
                building_lists.append(building_list)
                building_list = []
        
        results = []
        for building_list in building_lists:    
            results.append(pool.apply_async(construct_building, (building_list, found_rects,)))

        buildings = set()
        for result in results:
            for building in result.get():
                if len(building.rooms) > 1:
                    buildings.add(building)

    else:
        building_list = []
        for rect in found_rects:
            building_list.append(Building(rect))

        buildings = set()
        for building in construct_building(building_list, found_rects):
            if len(building.rooms) > 1:
                buildings.add(building)


    id = 0
    for building in buildings:
        building.setId(id)
        id += 1

    return buildings


def construct_building(buildings, found_rects):
    buildings = buildings
    progress = ProgressReport(step=0.1)
    b = 0
    while b < len(buildings):
        building = buildings[b]
        i = 0
        while i < len(found_rects):
            if not building.hasRoom(found_rects[i]) and building.is_connected_to(found_rects[i]) and building.touches(found_rects[i]):
                new_building = building.copy()
                new_building.addRoom(found_rects[i])
                if new_building not in buildings:
                    buildings.append(new_building)
                    buildings = list(set(buildings))
            i += 1
        b += 1

        progress.printProgress('Finding possible buildings ' + str(b) + "/" + str(len(buildings)), b / len(buildings))

    real_buildings = set()
    for building in buildings:
        if len(building.rooms) > 1 and not is_contained_in_other(building, buildings):
            real_buildings.add(building)

    return list(real_buildings)


def is_contained_in_other(building, buildings):
    for b in buildings:
        if is_part_of_building(building, b):
            return True
    return False


def is_part_of_building(b1, b2, strict=True):
    if len(b2.rooms) > len(b1.rooms):
        for r in b1.room_ids:
            if r not in b2.room_ids:
                return False
        return True
    return False
