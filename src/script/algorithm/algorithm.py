import time
from multiprocessing import Pool, Manager

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

    if debug:
        print('Calculating distance-matrix: ', end='')
    distances = calcDistance(windows, posts, maximal_length_of_side, minimal_length_of_side)
    if debug:
        number_of_values = 0
        for d in distances.values():
            number_of_values += len(d)
        print(str(number_of_values) + " values")

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
        with Pool(processes=number_of_computercores) as pool:

            progress = ProgressReport()

            buildings_to_check = []
            for rect in found_rects:
                buildings_to_check.append(Building(rect))

            buildings = buildings_to_check
            with Manager() as manager:
                found_rects1 = manager.list(found_rects)
                while len(buildings_to_check) > 0:

                    building_pools = dict()
                    for i in range(number_of_computercores):
                        building_pools[i] = []
                    for i in range(len(buildings_to_check)):
                        building_pools[i % number_of_computercores].append(buildings_to_check[i])

                    results = []
                    for pod in building_pools.values():
                        results.append(pool.apply_async(eeeh, (pod, found_rects, )))

                    new_buildings = set()
                    all_old = set()
                    for result in results:
                        new, old = result.get()
                        new_buildings |= new
                        all_old |= old
                    new_buildings = list(new_buildings)

                    buildings_to_check = manager.list(new_buildings)

                    buildings += all_old

                    progress.printProgress('(' + str(len(buildings[-1].rooms)) + ') Locking at possible buildings ' + str(len(buildings_to_check)) + ' of ' + str(len(buildings)), (len(buildings)-len(buildings_to_check)) / len(buildings))

            real_buildings_first_pass = set()
            for building in buildings:
                if len(building.rooms) > 1:
                    real_buildings_first_pass.add(building)

            progress.printProgress('Checking for duplicate buildings ' + str(len(real_buildings_first_pass)), 1)

            real_buildings = set()
            for building in real_buildings_first_pass:
                if not is_contained_in_other(building, buildings):  # TODO: multithreading
                    real_buildings.add(building)

            buildings = list(real_buildings)
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
    progress = ProgressReport(step=5.)
    percent = 0
    b = 0
    new_buildings = set()
    while b < len(buildings):
        building = buildings[b]
        i = 0
        building.part_of_bigger = False
        while i < len(found_rects):
            if not building.hasRoom(found_rects[i]) and building.is_connected_to(found_rects[i]) and building.touches(found_rects[i]):
                new_building = building.copy()
                new_building.addRoom(found_rects[i])
                if new_building.is_valid() and new_building not in new_buildings:
                    new_buildings.add(new_building)
                    building.part_of_bigger = True
            i += 1
        b += 1
        if b == len(buildings):
            buildings += list(new_buildings)
            new_buildings = set()

        percent = b / (len(new_buildings) + len(buildings))
        if progress.will_print(percent):
            progress.printProgress('(' + str(len(building.rooms)) + ')Finding possible buildings ' + str(b) + "/" + str(len(buildings) + len(new_buildings)), percent)

    real_buildings_first_pass = set()
    for building in buildings:
        if len(building.rooms) > 1 and not building.part_of_bigger:
            real_buildings_first_pass.add(building)

    real_buildings = set()
    for building in real_buildings_first_pass:
        if not is_contained_in_other(building, buildings):
            real_buildings.add(building)

    return list(real_buildings)


def eeeh(buildings, found_rects):
    new_buildings = set()
    possible_real_buildings = set()
    for b in buildings:
        current_result = buildings_from_building(b, found_rects)
        new_buildings |= current_result
        if len(current_result) <= 0:
            possible_real_buildings.add(b)
    return new_buildings, possible_real_buildings


def buildings_from_building(building, found_rects):
    new_buildings = set()
    for r in found_rects:
        if not building.hasRoom(r) and building.is_connected_to(r) and building.touches(r):
            new_building = building.copy()
            new_building.addRoom(r)
            if len(new_building.rooms) > len(building.rooms) and new_building.is_valid() and new_building not in new_buildings:
                new_buildings.add(new_building)
    return new_buildings


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
